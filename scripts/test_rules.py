from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.schemas import InvoiceData
from app.validator import validate

rates = {"6600045940": 14.7}


def doc(discount, total_after=None, start="2026-07-19", final="2026-07-23"):
    return InvoiceData(
        request_number="3000461274", drss_number="3000461274", job_number="86221",
        well_name="ABJF-107", rig_short_name="SP-110", contract_no="6600045940",
        grand_total_before_discount=127878.02,
        discount_amount=discount,
        grand_total_after_discount=round(127878.02-discount, 2) if total_after is None else total_after,
        start_date=start, final_date=final,
    )

accounting = doc(18798.07, total_after=109079.95)

# Exact discount
r = validate(accounting, doc(18798.07, total_after=109079.95), rates)
assert r.status == "VALID" and not r.warnings

# <= 0.99 discount discrepancy: warning, but still VALID when all other checks pass
accounting_tolerated = doc(18798.07, total_after=109079.52)
r = validate(accounting_tolerated, doc(18798.50, total_after=109079.52), rates)
assert r.status == "VALID" and r.warnings

# >= 1.00 discount discrepancy: INVALID
accounting_invalid = doc(18798.07, total_after=109078.95)
r = validate(accounting_invalid, doc(18799.07, total_after=109078.95), rates)
assert r.status == "INVALID"

# Dates do not participate in validation
r = validate(accounting, doc(18798.07, total_after=109079.95, start="2099-01-01", final="2099-01-02"), rates)
assert r.status == "VALID"

print("All Phase 1 business-rule tests passed.")
