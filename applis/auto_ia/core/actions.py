from . import mouse_controller
from . import keyboard_clipboard
from .zones import zone_manager
from .tutorial import tutorial_manager
from dataclasses import dataclass, asdict
from typing import Optional
import threading
import time
import uuid
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

@dataclass
class Action:
    id: str
    type: str
    params: dict
    status: str
    created_at: float
    source: str = "unknown"
    priority: int = 0
    label: Optional[str] = None
    started_at: Optional[float] = None
    finished_at: Optional[float] = None
    error: Optional[str] = None

    def to_dict(self):
        return asdict(self)

class ActionQueue:
    def __init__(self):
        self._actions = []
        self._lock = threading.Lock()

    def add_action(self, action_type: str, params: dict, source: str = "unknown", priority: int = 0, label: Optional[str] = None) -> str:
        with self._lock:
            action = Action(
                id=str(uuid.uuid4()),
                type=action_type,
                params=params,
                status="pending",
                created_at=time.time(),
                source=source,
                priority=priority,
                label=label
            )
            self._actions.append(action)
            logger.info(f"ACTION_ADDED id={action.id[:8]} type={action_type} source={source} priority={priority} label={label}")
            return action.id

    def get_next_pending(self) -> Optional[Action]:
        with self._lock:
            for action in self._actions:
                if action.status == "pending":
                    return action
            return None

    def list_actions(self, status_filter: Optional[str] = None):
        with self._lock:
            if status_filter:
                return [a.to_dict() for a in self._actions if a.status == status_filter]
            return [a.to_dict() for a in self._actions]

    def update_action_status(self, action_id: str, status: str, error: Optional[str] = None):
        with self._lock:
            for action in self._actions:
                if action.id == action_id:
                    old_status = action.status
                    action.status = status
                    if status == "running":
                        action.started_at = time.time()
                    elif status in ["done", "error"]:
                        action.finished_at = time.time()
                    if error:
                        action.error = error

                    log_msg = f"STATUS_CHANGE id={action_id[:8]} {old_status}→{status} type={action.type}"
                    if error:
                        logger.error(f"{log_msg} error={error}")
                    else:
                        logger.info(log_msg)
                    break

class ActionWorker:
    def __init__(self, queue: ActionQueue, min_delay_seconds: float = 0.15, max_actions_per_minute: int = 200):
        self.queue = queue
        self.running = False
        self.paused = False
        self.thread = None
        self.min_delay_seconds = min_delay_seconds
        self.max_actions_per_minute = max_actions_per_minute
        self.actions_timestamps = []

    def start(self):
        if not self.running:
            self.running = True
            self.paused = False
            self.thread = threading.Thread(target=self._run_loop, daemon=True)
            self.thread.start()
            logger.info("WORKER_STARTED")

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join(timeout=2)
        logger.info("WORKER_STOPPED")

    def pause(self):
        self.paused = True
        logger.info("WORKER_PAUSED")

    def resume(self):
        self.paused = False
        logger.info("WORKER_RESUMED")

    def get_status(self) -> str:
        if not self.running:
            return "stopped"
        if self.paused:
            return "paused"
        return "running"

    def _check_rate_limit(self) -> bool:
        now = time.time()
        self.actions_timestamps = [ts for ts in self.actions_timestamps if now - ts < 60]
        return len(self.actions_timestamps) < self.max_actions_per_minute

    def _run_loop(self):
        while self.running:
            if self.paused:
                time.sleep(0.5)
                continue

            action = self.queue.get_next_pending()
            if action:
                if not self._check_rate_limit():
                    self.queue.update_action_status(action.id, "rate_limited", "Dépassement max_actions_per_minute")
                    logger.warning(f"RATE_LIMITED id={action.id[:8]} max={self.max_actions_per_minute}/min")
                    time.sleep(1)
                    continue

                self.queue.update_action_status(action.id, "running")
                try:
                    result = execute_action({"type": action.type, "params": action.params})
                    if result["status"] == "ok":
                        self.queue.update_action_status(action.id, "done")
                    else:
                        self.queue.update_action_status(action.id, "error", result["message"])
                except Exception as e:
                    self.queue.update_action_status(action.id, "error", str(e))

                self.actions_timestamps.append(time.time())
                time.sleep(self.min_delay_seconds)
            else:
                time.sleep(0.5)

action_queue = ActionQueue()
action_worker = ActionWorker(action_queue, min_delay_seconds=0.15, max_actions_per_minute=200)

def execute_action(action: dict) -> dict:
    try:
        action_type = action.get("type")
        params = action.get("params", {})

        if action_type == "mouse_click":
            x = params.get("x")
            y = params.get("y")
            button = params.get("button", "left")
            mouse_controller.click(x, y, button)
            return {"status": "ok", "message": f"Clic {button} à ({x}, {y})"}

        elif action_type == "mouse_move":
            x = params.get("x")
            y = params.get("y")
            duration = params.get("duration")
            mouse_controller.move_to(x, y, duration)
            return {"status": "ok", "message": f"Déplacement vers ({x}, {y})"}

        elif action_type == "mouse_scroll":
            amount = params.get("amount")
            mouse_controller.scroll(amount)
            return {"status": "ok", "message": f"Scroll de {amount}"}

        elif action_type == "clipboard_copy":
            text = params.get("text")
            keyboard_clipboard.copy_text(text)
            return {"status": "ok", "message": f"Texte copié: {text[:50]}..."}

        elif action_type == "clipboard_paste":
            text = keyboard_clipboard.paste_text()
            return {"status": "ok", "message": f"Texte collé: {text[:50]}..."}

        elif action_type == "keyboard_write":
            text = params.get("text")
            keyboard_clipboard.write_text(text)
            return {"status": "ok", "message": f"Texte écrit: {text[:50]}..."}

        elif action_type == "keyboard_press":
            keys = params.get("keys", [])
            keyboard_clipboard.press_keys(keys)
            return {"status": "ok", "message": f"Touches pressées: {'+'.join(keys)}"}

        elif action_type == "click_zone":
            zone_name = params.get("zone")
            button = params.get("button", "left")
            zone = zone_manager.get_zone(zone_name)
            if not zone:
                return {"status": "error", "message": f"Zone '{zone_name}' non trouvée"}
            x, y = zone.get_center()
            mouse_controller.click(x, y, button)
            tutorial_manager.check_action("click_zone", zone_name)
            return {"status": "ok", "message": f"Clic {button} sur zone '{zone_name}' ({x}, {y})"}

        else:
            return {"status": "error", "message": f"Type d'action inconnu: {action_type}"}

    except Exception as e:
        return {"status": "error", "message": str(e)}
