transactions = []
running = True

def parse_date(date: str):
    date_check = date.strip().split("-")
    if "-" not in date or date.count("-") != 2:
        print("Must be formatted YYYY-MM-DD.")
        return None
    elif (len(date_check[0]) != 4 or date_check[0].isdigit() == False) or (len(date_check[1]) != 2 or date_check[1].isdigit() ==  False) or (len(date_check[2]) != 2 or date_check[2].isdigit() == False):
        print("Must be formatted YYYY-MM-DD.")
        return None
    elif (int(date_check[0]) > 2026 or int(date_check[0]) < 0) or (int(date_check[1]) > 12 or int(date_check[1]) < 0) or (int(date_check[2]) > 31 or int(date_check[2]) < 0):
        print("Please enter a valid date.")
        return None
    else:
        return str(date)

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


def category_check(category):
    if category.lower() == "" or category.lower().isalpha() == False or category.lower() not in ('food', 'rent', 'utilities', 'transportation', 'education', 'entertainment', 'shopping', 'health', 'personal', 'other'):
        print("Please enter a valid input (ex. food, rent, utilities, transportation, education, entertainment, etc)")
        return None
    else:
        return category.lower()

def description_check(description):
    if description == "":
        print("Please enter a valid description.")
        return None
    else:
        return description.lower()
    

def add():
    add_dict = {}
    date = None
    amount = None
    description = None
    category = None
    while date == None:
        date = parse_date(input("Add the date of your transaction (YYYY-MM-DD): "))
    add_dict['date'] = date
    while amount == None:
        amount = parse_amount(input("Enter the amount of your transaction ($$.$$): "))
    add_dict['amount'] = amount
    while category == None:
        category = category_check(input("Enter the type of the transaction: "))
    add_dict['category'] = category
    while description == None:
        description = description_check(input("Enter a description for your transaction: "))
    add_dict['description'] = description
    return add_dict


def main():
    while running:
        print('MENU')
        print('-----------------')
        print('1. Add')
        print('2. List')
        print('3. Summaries')
        print('4. Save/Load')
        print('5. Exit')
        print('-----------------')
        user_choice = int(input('Enter a number in the menu: '))
        match user_choice:
            case 1:
                transactions.append(add())
            case 2:
                pass
            case 3:
                pass 
            case 4:
                pass 
            case 5:
                running = False


main()