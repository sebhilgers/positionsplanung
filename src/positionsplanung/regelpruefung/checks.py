# checks.py

from enum import Enum
from typing import Optional

class Status(str, Enum):
    OK = "OK"
    WARNUNG = "WARNUNG"
    NICHT_ERFUELLT = "NICHT_ERFUELLT"
    NICHT_BEWERTET = "NICHT_BEWERTET"

class RuleResult:
    def __init__(
        self,
        regel_id: str,
        titel: str,
        status: Status,
        meldung: str,
        empfehlung: str = "",
    ) -> None:
        self.regel_id = regel_id
        self.titel = titel
        self.status = status
        self.meldung = meldung
        self.empfehlung = empfehlung

    def as_dict(self) -> dict:
        return {
            "regel_id": self.regel_id,
            "titel": self.titel,
            "status": self.status.value,
            "meldung": self.meldung,
            "empfehlung": self.empfehlung,
        }