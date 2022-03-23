import csv
import datetime
from decimal import Decimal
import os
from pathlib import Path

from sheets.models import Category, Expense


for file in os.listdir("inputdata"):
    if file.endswith(".csv"):
        with open(Path("inputdata") / Path(file), newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if datetime.datetime.strptime(
                    row.get("Date"), "%d/%m/%Y"
                ).date() < datetime.date(2021, 11, 19):
                    continue
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
                        "time": datetime.datetime.strptime(
                            row.get("Time"), "%H:%M:%S"
                        ).time(),
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
