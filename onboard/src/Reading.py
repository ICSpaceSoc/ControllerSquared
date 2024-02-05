from dataclasses import dataclass

@dataclass(frozen=True)
class Reading:
    sensor: str
    raw: float
    filt: float
    timestamp: float