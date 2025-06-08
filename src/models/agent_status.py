from enum import Enum

class AgentStatus(str, Enum):
    INSTALLING = "installing"
    RUNNING = "running"
    PAUSED = "paused"
    SHUTDOWN = "shutdown"
    ERROR = "error"