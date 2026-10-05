from __future__ import annotations

import json
from pathlib import Path

from .client import EpicorClient
from .models import EpicorAttachment, EpicorTicket


class MockEpicorClient(EpicorClient):
    """Local Epicor stand-in used until the real Epicor interface is available."""

    def __init__(self, config_path: str | Path):
        self.config_path = Path(config_path)
        self.logged_in_user: str | None = None
        self._tickets: dict[str, EpicorTicket] = {}
        self._load()

    def _load(self) -> None:
        data = json.loads(self.config_path.read_text(encoding="utf-8"))
        base = self.config_path.parent
        for item in data.get("tickets", []):
            attachments = [
                EpicorAttachment(
                    name=a["name"],
                    path=(base / a["path"]).resolve(),
                    document_type=a.get("document_type"),
                )
                for a in item.get("attachments", [])
            ]
            ticket = EpicorTicket(
                ticket_id=str(item["ticket_id"]),
                callout_number=item.get("callout_number"),
                created_by=item.get("created_by", ""),
                status=item.get("status", "PENDING"),
                attachments=attachments,
                metadata=item.get("metadata", {}),
            )
            self._tickets[ticket.ticket_id] = ticket

    def login(self, username: str, password: str) -> bool:
        # Mock only: never persist the password.
        self.logged_in_user = username
        return bool(username and password)

    def _require_login(self) -> None:
        if not self.logged_in_user:
            raise RuntimeError("Mock Epicor client is not logged in.")

    def get_user_queue(self, username: str) -> list[EpicorTicket]:
        self._require_login()
        return [
            t for t in self._tickets.values()
            if t.created_by == username and t.status == "PENDING"
        ]

    def get_ticket(self, ticket_id: str) -> EpicorTicket:
        self._require_login()
        try:
            return self._tickets[str(ticket_id)]
        except KeyError as exc:
            raise KeyError(f"Ticket {ticket_id} was not found.") from exc

    def get_attachments(self, ticket_id: str):
        return self.get_ticket(ticket_id).attachments

    def approve_ticket(self, ticket_id: str, comment: str = "") -> None:
        ticket = self.get_ticket(ticket_id)
        ticket.status = "APPROVED"
        ticket.metadata["action_comment"] = comment

    def reject_ticket(self, ticket_id: str, comment: str) -> None:
        if not comment.strip():
            raise ValueError("A rejection reason is required.")
        ticket = self.get_ticket(ticket_id)
        ticket.status = "REJECTED"
        ticket.metadata["action_comment"] = comment
