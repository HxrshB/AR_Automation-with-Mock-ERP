# Phase 1 Test Results

Date: 2026-09-28

## Mock queue integration

- Mock Epicor login: PASS
- Mock user queue retrieval: PASS
- Attachment discovery: PASS
- OCR processing: PASS
- Document type detection: PASS
- Field extraction: PASS
- Discount master lookup: PASS
- Validation: PASS
- Excel generation: PASS

Sample ticket `MOCK-3000461274` produced `VALID`.

Extracted/report fields include:

- Request/DRSS: `3000461274`
- Well: `ABJF-107`
- Rig: `SP-110`
- Contract: `6600045940`
- Start Date: `2026-07-19`
- Final Date: `2026-07-23`
- Configured discount: `14.70%`
- Expected discount: `SAR 18,798.07`
- JST discount: `SAR 18,798.07`
- Final total: `SAR 109,079.95`

## Business-rule tests

- Exact discount: PASS
- Discount difference <= SAR 0.99: PASS; validation remains VALID and warning is generated
- Discount difference >= SAR 1.00: PASS; validation becomes INVALID
- Changing Start/Final Date does not change validation status: PASS
