import csv
import datetime
from decimal import Decimal

from sheets.models import Category, Expense

FILE_NAME = "MonzoDataExport_1Jul2018-23Mar2022_2022-03-23_193000.csv"

with open(FILE_NAME, newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        category, created = Category.objects.get_or_create(
            name=row.get("Category")
        )
        if created:
            print(f"Created {category}")
        expense, created_expense = Expense.objects.update_or_create(
            import_reference=row.get("Transaction ID"),
            defaults={
                "category": category,
                "date": datetime.datetime.strptime(
                    row.get("Date"), "%d/%m/%Y"
                ).date(),
                "description": "\n".join(
                    [
                        row.get("Emoji", "")
                        + " "
                        + (row.get("Name") or row.get("Description")),
                        row.get("Notes and #tags"),
                    ],
                ),
                "amount": Decimal(row.get("Amount", "0")),
                "repeat_next_month": False,
                "import_reference": row.get("Transaction ID"),
            },
        )
        if created_expense:
            print(f"Created {expense}")
        else:
            print(f"Updated {expense}")
