from __future__ import annotations

from abc import ABC, abstractmethod

from .models import EpicorTicket


class EpicorClient(ABC):
    """Interface for Epicor operations.

    The application depends on this interface, not on Epicor-specific HTTP/UI details.
    A real Epicor REST/BAQ implementation can replace the mock client later.
    """

    @abstractmethod
    def login(self, username: str, password: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    def get_user_queue(self, username: str) -> list[EpicorTicket]:
        raise NotImplementedError

    @abstractmethod
    def get_ticket(self, ticket_id: str) -> EpicorTicket:
        raise NotImplementedError

    @abstractmethod
    def get_attachments(self, ticket_id: str):
        raise NotImplementedError

    @abstractmethod
    def approve_ticket(self, ticket_id: str, comment: str = "") -> None:
        raise NotImplementedError

    @abstractmethod
    def reject_ticket(self, ticket_id: str, comment: str) -> None:
        raise NotImplementedError
