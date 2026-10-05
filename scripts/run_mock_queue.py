from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.epicor import MockEpicorClient
from app.excel_report import build_validation_workbook
from app.queue_processor import process_user_queue

client = MockEpicorClient(ROOT / "data" / "mock_epicor_queue.json")
client.login("demo_user", "demo-password")
results = process_user_queue(client, "demo_user", ROOT / "data" / "mock_erp.json")
output = build_validation_workbook(results, ROOT / "output" / "mock_validation_queue.xlsx")

for item in results:
    print(item["ticket_id"], item["status"], item.get("reason", ""))
print(f"Excel report: {output}")
