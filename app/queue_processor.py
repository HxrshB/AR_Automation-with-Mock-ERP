from __future__ import annotations

import json
from pathlib import Path

from .epicor import EpicorClient
from .extractor import detect_document_type, extract_fields
from .ocr import ocr_pdf
from .validator import validate


def load_discount_rates(path: str | Path) -> dict[str, float]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    return {str(k): float(v) for k, v in data.get("discount_rates", {}).items()}


def _find_documents(attachments):
    accounting = None
    jst = None
    for attachment in attachments:
        doc_type = (attachment.document_type or "").lower()
        if doc_type == "accounting" or "account" in attachment.name.lower():
            accounting = attachment
        elif doc_type == "jst" or "jst" in attachment.name.lower() or "service" in attachment.name.lower():
            jst = attachment
    return accounting, jst


def process_user_queue(client: EpicorClient, username: str, rates_path: str | Path):
    rates = load_discount_rates(rates_path)
    results = []

    for ticket in client.get_user_queue(username):
        attachments = client.get_attachments(ticket.ticket_id)
        accounting_attachment, jst_attachment = _find_documents(attachments)

        if not accounting_attachment or not jst_attachment:
            results.append({
                "ticket_id": ticket.ticket_id,
                "status": "REVIEW",
                "reason": "Required Accounting and/or JST attachment is missing.",
                "validation": None,
            })
            continue

        accounting_pages = ocr_pdf(accounting_attachment.path)
        jst_pages = ocr_pdf(jst_attachment.path)

        if detect_document_type(accounting_pages) != "accounting":
            raise ValueError(f"Ticket {ticket.ticket_id}: Accounting attachment type could not be confirmed.")
        if detect_document_type(jst_pages) != "jst":
            raise ValueError(f"Ticket {ticket.ticket_id}: JST attachment type could not be confirmed.")

        accounting = extract_fields(accounting_pages, "accounting")
        jst = extract_fields(jst_pages, "jst")
        validation = validate(accounting, jst, rates)

        results.append({
            "ticket_id": ticket.ticket_id,
            "status": validation.status,
            "reason": "; ".join(validation.reasons),
            "validation": validation,
        })

    return results
