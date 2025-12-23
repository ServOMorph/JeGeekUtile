from dataclasses import dataclass, asdict
from typing import Optional, Dict
import threading

@dataclass
class Zone:
    name: str
    x: int
    y: int
    width: Optional[int] = None
    height: Optional[int] = None

    def to_dict(self):
        return asdict(self)

    def get_center(self) -> tuple[int, int]:
        if self.width and self.height:
            return (self.x + self.width // 2, self.y + self.height // 2)
        return (self.x, self.y)

class ZoneManager:
    def __init__(self):
        self._zones: Dict[str, Zone] = {}
        self._lock = threading.Lock()

    def set_zone(self, name: str, x: int, y: int, width: Optional[int] = None, height: Optional[int] = None) -> Zone:
        with self._lock:
            zone = Zone(name=name, x=x, y=y, width=width, height=height)
            self._zones[name] = zone
            return zone

    def get_zone(self, name: str) -> Optional[Zone]:
        with self._lock:
            return self._zones.get(name)

    def list_zones(self):
        with self._lock:
            return [z.to_dict() for z in self._zones.values()]

    def delete_zone(self, name: str) -> bool:
        with self._lock:
            if name in self._zones:
                del self._zones[name]
                return True
            return False

zone_manager = ZoneManager()
