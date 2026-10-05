from __future__ import annotations

from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Font


HEADERS = [
    "Ticket ID", "Request / DRSS", "Well", "Rig", "Contract",
    "Start Date", "Final Date", "Job ID", "Discount %",
    "Expected Discount", "JST Discount", "Accounting Total", "JST Total",
    "Validation", "Warnings", "Reason", "Action"
]


def build_validation_workbook(results, output_path: str | Path) -> Path:
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    wb = Workbook()
    ws = wb.active
    ws.title = "Validation Queue"
    ws.append(HEADERS)

    for cell in ws[1]:
        cell.font = Font(bold=True)

    for item in results:
        v = item.get("validation")
        if v is None:
            ws.append([
                item["ticket_id"], None, None, None, None, None, None, None,
                None, None, None, None, None, item["status"], None,
                item.get("reason"), "Review"
            ])
            continue

        rate = v.reference.get("expected_discount_percent")
        before = v.jst.grand_total_before_discount
        expected = round(before * rate / 100, 2) if rate is not None and before is not None else None
        request = v.accounting.request_number or v.jst.request_number
        start = v.jst.start_date or v.accounting.start_date
        final = v.jst.final_date or v.accounting.final_date
        action = "Approve" if v.status == "VALID" else ("Reject" if v.status == "INVALID" else "Review")

        ws.append([
            item["ticket_id"], request, v.jst.well_name or v.accounting.well_name,
            v.jst.rig_short_name or v.accounting.rig_short_name,
            v.accounting.contract_no or v.jst.contract_no,
            start, final, v.jst.job_number, rate, expected,
            v.jst.discount_amount, v.accounting.grand_total_after_discount,
            v.jst.grand_total_after_discount, v.status,
            "; ".join(v.warnings), "; ".join(v.reasons), action
        ])

    ws.freeze_panes = "A2"
    ws.auto_filter.ref = ws.dimensions
    for column in ws.columns:
        width = min(max(len(str(cell.value or "")) for cell in column) + 2, 40)
        ws.column_dimensions[column[0].column_letter].width = width

    wb.save(output_path)
    return output_path
