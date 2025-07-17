# test_gsheet.py
from helpers import connect_google_sheet

sheet = connect_google_sheet()
sheet.append_row(["TEST USER", "2025-07-17 23:00:00", "IN"])
print("✅ Test row added.")
