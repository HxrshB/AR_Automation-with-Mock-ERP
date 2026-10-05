from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal


TicketStatus = Literal["PENDING", "APPROVED", "REJECTED"]


@dataclass
class EpicorAttachment:
    name: str
    path: Path
    document_type: str | None = None


@dataclass
class EpicorTicket:
    ticket_id: str
    callout_number: str | None
    created_by: str
    status: TicketStatus = "PENDING"
    attachments: list[EpicorAttachment] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)
