from dataclasses import dataclass, field
from typing import List


@dataclass
class AppConfig:
    screenURL_List: List[str] = field(default_factory=list)
    APIBaseURL: str = ""
    SocketBaseURL: str = ""
    AutoLoadSceneIndex: int = -1
    AutoReset: bool = False
    AutoResetHour: int = 2
    AutoResetMinute: int = 0