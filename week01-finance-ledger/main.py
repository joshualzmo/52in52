from datetime import date, timedelta
import json
import os


# ----------------------------
# Validates and parses a date string entered by the user.
# Expected format: YYYY-MM-DD
# Returns the date string if valid, otherwise returns None.
# ----------------------------
def parse_date(date: str):
    date_check = date.strip().split("-")
    if "-" not in date or date.count("-") != 2:
        print("Must be formatted YYYY-MM-DD.")
        return None
    elif (len(date_check[0]) != 4 or date_check[0].isdigit() == False) or \
         (len(date_check[1]) != 2 or date_check[1].isdigit() == False) or \
         (len(date_check[2]) != 2 or date_check[2].isdigit() == False):
        print("Must be formatted YYYY-MM-DD.")
        return None
    elif (int(date_check[0]) > 2026 or int(date_check[0]) < 0) or \
         (int(date_check[1]) > 12 or int(date_check[1]) < 1) or \
         (int(date_check[2]) > 31 or int(date_check[2]) < 1):
        print("Please enter a valid date.")
        return None
    else:
        return str(date)


# ----------------------------
# Validates and parses a monetary amount entered by the user.
# Accepts values such as 10, 10.50, -4.25, $1,234.56
# Returns a float if valid, otherwise returns None.
# ----------------------------
def parse_amount(amount: str):
    if amount is None:
        print("Please enter a valid input.")
        return None

    s = amount.strip()
    if s == "":
        print("Please enter a valid input.")
        return None

    s = s.replace("$", "").replace(",", "")

    sign = 1
    if s.startswith("-"):
        sign = -1
        s = s[1:].strip()

    if s == "":
        print("Please enter a valid input.")
        return None

    if s.count(".") > 1:
        print("Please enter a valid input.")
        return None

    if "." in s:
        dollars, cents = s.split(".", 1)
        if dollars == "":
            dollars = "0"
        if not dollars.isdigit():
            print("Please enter a valid input.")
            return None
        if cents == "" or not cents.isdigit() or len(cents) > 2:
            print("Please enter a valid input ($$.$$).")
            return None
        cents = cents.ljust(2, "0")
        value = float(f"{dollars}.{cents}")
    else:
        if not s.isdigit():
            print("Please enter a valid input.")
            return None
        value = float(s)

    return sign * value


# ----------------------------
# Validates the transaction category.
# Only allows predefined category names.
# Returns the lowercase category if valid, otherwise None.
# ----------------------------
def category_check(category):
    if category.lower() == "" or category.lower().isalpha() == False or category.lower() not in (
        "food", "rent", "utilities", "transportation", "education",
        "entertainment", "shopping", "health", "personal", "other"
    ):
        print("Please enter a valid input (ex. food, rent, utilities, transportation, education, entertainment, etc)")
        return None
    else:
        return category.lower()


# ----------------------------
# Validates the transaction description.
# Ensures the description is not empty.
# Returns the lowercase description if valid.
# ----------------------------
def description_check(description):
    if description == "":
        print("Please enter a valid description.")
        return None
    else:
        return description.lower()


# ----------------------------
# Collects a single transaction from the user.
# Re-prompts until all fields are valid.
# Returns a dictionary representing one transaction.
# ----------------------------
def add():
    add_dict = {}
    d = None
    amount = None
    description = None
    category = None

    while d is None:
        d = parse_date(input("Add the date of your transaction (YYYY-MM-DD): "))
    add_dict["date"] = d

    while amount is None:
        amount = parse_amount(input("Enter the amount of your transaction ($$.$$): "))
    add_dict["amount"] = amount

    while category is None:
        category = category_check(input(
            "Enter the type of the transaction ('food', 'rent', 'utilities', 'transportation', "
            "'education', 'entertainment', 'shopping', 'health', 'personal', 'other'): "
        ))
    add_dict["category"] = category

    while description is None:
        description = description_check(input("Enter a description for your transaction: "))
    add_dict["description"] = description

    return add_dict


# ----------------------------
# Displays all stored transactions in a readable format.
# ----------------------------
def listTransactions(transactions):
    if len(transactions) == 0:
        print("No transactions yet.")
        return

    for i in range(len(transactions)):
        t = transactions[i]
        print(f"Index {i}: {t['date']} | {t['category']} | {t['description']} | {t['amount']:.2f}")


# ----------------------------
# Converts a stored date string into a datetime.date object.
# Used internally for date comparisons in summaries.
# ----------------------------
def _date_obj_from_string(date_str: str):
    parts = date_str.strip().split("-")
    try:
        y = int(parts[0])
        m = int(parts[1])
        d = int(parts[2])
        return date(y, m, d)
    except Exception:
        return None


# ----------------------------
# Prints a formatted summary report.
# Shows totals and top categories.
# ----------------------------
def _print_summary(period_label: str, start_date: date, end_date: date,
                   total_income: float, total_expenses: float, category_totals: dict):
    net = total_income + total_expenses

    print("\nSUMMARY:", period_label)
    print(f"Range: {start_date.isoformat()} to {end_date.isoformat()}")
    print(f"Total income:   {total_income:.2f}")
    print(f"Total expenses: {total_expenses:.2f}")
    print(f"Net:            {net:.2f}")

    if len(category_totals) == 0:
        print("No transactions in this period.")
        return

    sorted_items = sorted(category_totals.items(), key=lambda kv: abs(kv[1]), reverse=True)

    print("\nTop categories:")
    for cat, amt in sorted_items[:5]:
        print(f"- {cat}: {amt:.2f}")
    print("")


# ----------------------------
# Generates weekly or monthly summaries of transactions.
# ----------------------------
def summaries(transactions):
    if len(transactions) == 0:
        print("No transactions yet.")
        return

    print("\nSUMMARIES")
    print("-----------------")
    print("1. Week (last 7 days)")
    print("2. Month (current month)")
    print("3. Back")
    print("-----------------")

    choice_raw = input("Choose an option: ").strip()
    if not choice_raw.isdigit():
        print("Please enter a valid option.")
        return

    choice = int(choice_raw)
    if choice == 3:
        return
    if choice not in (1, 2):
        print("Please enter a valid option.")
        return

    today = date.today()

    if choice == 1:
        start_date = today - timedelta(days=6)
        end_date = today
        label = "WEEK (last 7 days)"
    else:
        start_date = date(today.year, today.month, 1)
        end_date = today
        label = "MONTH (current month)"

    total_income = 0.0
    total_expenses = 0.0
    category_totals = {}

    for t in transactions:
        d_obj = _date_obj_from_string(t["date"])
        if d_obj is None:
            continue

        if start_date <= d_obj <= end_date:
            amt = float(t["amount"])
            cat = t["category"]

            if amt > 0:
                total_income += amt
            else:
                total_expenses += amt

            if cat not in category_totals:
                category_totals[cat] = 0.0
            category_totals[cat] += amt

    _print_summary(label, start_date, end_date, total_income, total_expenses, category_totals)


# ----------------------------
# Saves all transactions to a JSON file.
# ----------------------------
def save_transactions(transactions, file_path: str):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(transactions, f, indent=2)


# ----------------------------
# Loads transactions from a JSON file if it exists.
# Returns an empty list if the file does not exist or is invalid.
# ----------------------------
def load_transactions(file_path: str):
    transactions = []
    if not os.path.exists(file_path):
        return transactions

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        return transactions

    if not isinstance(data, list):
        return transactions

    for item in data:
        if not isinstance(item, dict):
            continue
        if "date" not in item or "amount" not in item or "category" not in item or "description" not in item:
            continue

        try:
            transaction = {
                "date": str(item["date"]),
                "amount": float(item["amount"]),
                "category": str(item["category"]),
                "description": str(item["description"]),
            }
            transactions.append(transaction)
        except Exception:
            continue

    return transactions


# ----------------------------
# Main program loop.
# Loads saved data at startup and handles the menu.
# ----------------------------
def main():
    file_path = "week1data.json"
    transactions = load_transactions(file_path)
    running = True

    while running:
        print("MENU")
        print("-----------------")
        print("1. Add")
        print("2. List")
        print("3. Summaries")
        print("4. Save/Load")
        print("5. Exit")
        print("-----------------")

        choice_raw = input("Enter a number in the menu: ").strip()
        if not choice_raw.isdigit():
            print("Please enter a valid menu number.\n")
            continue

        user_choice = int(choice_raw)

        match user_choice:
            case 1:
                transactions.append(add())
                save_transactions(transactions, file_path)
                print("Transaction added.\n")
            case 2:
                listTransactions(transactions)
                print("")
            case 3:
                summaries(transactions)
            case 4:
                save_transactions(transactions, file_path)
                print("Saved.\n")
            case 5:
                running = False
            case _:
                print("Please enter a valid menu number.\n")


main()
