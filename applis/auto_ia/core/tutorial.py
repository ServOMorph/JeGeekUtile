from dataclasses import dataclass, asdict, field
from typing import Optional, List
import threading
import logging

logger = logging.getLogger(__name__)

@dataclass
class TutorialStep:
    id: str
    zone: str
    message: str
    required_action: str
    hint: Optional[str] = None
    status: str = "pending"

    def to_dict(self):
        return asdict(self)

@dataclass
class Tutorial:
    id: str
    title: str
    description: str
    steps: List[TutorialStep] = field(default_factory=list)
    current_index: int = 0
    active: bool = False

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "steps": [s.to_dict() for s in self.steps],
            "current_index": self.current_index,
            "active": self.active
        }

    def get_current_step(self) -> Optional[TutorialStep]:
        if 0 <= self.current_index < len(self.steps):
            return self.steps[self.current_index]
        return None

    def is_completed(self) -> bool:
        return self.current_index >= len(self.steps)

class TutorialManager:
    def __init__(self):
        self._current_tutorial: Optional[Tutorial] = None
        self._lock = threading.Lock()

    def load_tutorial(self, tutorial: Tutorial) -> None:
        with self._lock:
            self._current_tutorial = tutorial
            logger.info(f"TUTORIAL_LOADED id={tutorial.id} steps={len(tutorial.steps)}")

    def start_tutorial(self) -> bool:
        with self._lock:
            if self._current_tutorial:
                self._current_tutorial.active = True
                self._current_tutorial.current_index = 0
                for step in self._current_tutorial.steps:
                    step.status = "pending"
                logger.info(f"TUTORIAL_STARTED id={self._current_tutorial.id}")
                return True
            return False

    def stop_tutorial(self) -> bool:
        with self._lock:
            if self._current_tutorial:
                self._current_tutorial.active = False
                logger.info(f"TUTORIAL_STOPPED id={self._current_tutorial.id}")
                return True
            return False

    def check_action(self, action_type: str, zone_name: Optional[str] = None) -> bool:
        with self._lock:
            if not self._current_tutorial or not self._current_tutorial.active:
                return False

            current_step = self._current_tutorial.get_current_step()
            if not current_step:
                return False

            if current_step.status != "pending":
                return False

            logger.info(f"TUTORIAL_STEP_CHECKED step={current_step.id} expected_zone={current_step.zone} received_action={action_type} received_zone={zone_name}")

            if action_type == "click_zone" and zone_name == current_step.zone:
                current_step.status = "completed"
                self._current_tutorial.current_index += 1
                logger.info(f"TUTORIAL_STEP_COMPLETED step={current_step.id} zone={zone_name}")

                if self._current_tutorial.is_completed():
                    self._current_tutorial.active = False
                    logger.info(f"TUTORIAL_COMPLETED id={self._current_tutorial.id}")

                return True
            else:
                logger.info(f"TUTORIAL_STEP_MISMATCH expected={current_step.zone} received={zone_name}")

            return False

    def get_status(self) -> dict:
        with self._lock:
            if not self._current_tutorial:
                return {"status": "no_tutorial"}

            return {
                "status": "ok",
                "tutorial": self._current_tutorial.to_dict()
            }

tutorial_manager = TutorialManager()
