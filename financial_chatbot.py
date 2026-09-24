# ============================================================
# FINANCIAL CHATBOT - ALEX
# Offline Rule-Based Personal Finance Assistant
# ============================================================

import json
import os
from datetime import datetime

DATA_FILE = "financial_data.json"


# -------------------- DATA MANAGEMENT --------------------

def load_data():
    if not os.path.exists(DATA_FILE):
        return {
            "income": 0.0,
            "expenses": [],
            "savings_goal": None
        }

    try:
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        return {
            "income": 0.0,
            "expenses": [],
            "savings_goal": None
        }


def save_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)


# -------------------- KNOWLEDGE BASE --------------------

TOPICS = {
    "budgeting": (
        "Budgeting is the process of planning your income and expenses. "
        "A good budget helps control unnecessary spending, maintain savings "
        "and achieve financial goals."
    ),

    "savings": (
        "Savings are the portion of income kept aside for future needs. "
        "Regular savings can help build an emergency fund and achieve "
        "short-term and long-term financial goals."
    ),

    "investment": (
        "Investment means putting money into assets such as stocks, bonds, "
        "mutual funds or other instruments with the expectation of earning "
        "returns over time. Investments involve different levels of risk."
    ),

    "emi": (
        "EMI stands for Equated Monthly Instalment. It is the fixed periodic "
        "payment made towards a loan and generally contains both principal "
        "and interest."
    ),

    "interest": (
        "Interest is the cost of borrowing money or the return earned on "
        "money deposited or invested. It can be calculated using simple or "
        "compound interest methods."
    ),

    "tax": (
        "Tax is a compulsory financial charge collected by the government "
        "from individuals or businesses to fund public services and "
        "government activities. Actual tax liability depends on applicable "
        "laws and the person's circumstances."
    ),

    "credit": (
        "Credit refers to the ability to borrow money or obtain goods and "
        "services with an agreement to repay later. Credit history and "
        "repayment behaviour can affect creditworthiness."
    ),

    "credit score": (
        "A credit score is a numerical indicator based on information in a "
        "person's credit history. Factors can include repayment history, "
        "credit utilisation and the length and type of credit accounts."
    ),

    "inflation": (
        "Inflation is the sustained increase in the general price level of "
        "goods and services. When prices rise, the purchasing power of money "
        "generally decreases."
    ),

    "expenses": (
        "Expenses are the costs incurred for goods and services. Common "
        "categories include food, rent, transportation, education, utilities "
        "and entertainment."
    ),

    "financial planning": (
        "Financial planning involves managing income, expenses, savings, "
        "investments, insurance and financial goals to improve long-term "
        "financial stability."
    ),

    "mutual funds": (
        "A mutual fund pools money from multiple investors and invests it "
        "according to a defined investment strategy. Mutual funds can provide "
        "diversification but are still subject to market and other risks."
    ),

    "stocks": (
        "Stocks represent ownership in a company. Investors may earn through "
        "capital appreciation and, where applicable, dividends. Stock prices "
        "can fluctuate and losses are possible."
    ),

    "compound interest": (
        "Compound interest is calculated on the original principal plus "
        "interest accumulated during previous periods."
    ),

    "simple interest": (
        "Simple interest is calculated only on the original principal amount "
        "using the applicable interest rate and time period."
    ),

    "loan": (
        "A loan is money borrowed from a lender that is repaid according to "
        "agreed terms, usually with interest. Important factors include "
        "principal, interest rate, tenure, fees and repayment schedule."
    ),

    "risk": (
        "Financial risk is the possibility that a financial decision or "
        "investment may result in loss or an outcome different from what "
        "was expected."
    ),

    "diversification": (
        "Diversification means spreading investments across different assets "
        "or categories so that the performance of one investment does not "
        "completely determine the overall result."
    ),

    "returns": (
        "Investment return is the gain or loss generated by an investment "
        "over a period. It may come from price changes, interest, dividends "
        "or other income."
    ),

    "insurance": (
        "Insurance is a risk-management product in which a policyholder pays "
        "a premium in exchange for coverage against specified financial losses "
        "or events according to policy terms."
    ),

    "retirement": (
        "Retirement planning involves estimating future financial needs and "
        "building savings or investments to support those needs after regular "
        "employment income decreases or stops."
    ),

    "liquidity": (
        "Liquidity describes how quickly and easily an asset can be converted "
        "into cash without a significant loss in value."
    ),

    "net worth": (
        "Net worth is calculated as total assets minus total liabilities. "
        "It gives a snapshot of an individual's financial position."
    ),

    "emergency fund": (
        "An emergency fund is money kept aside for unexpected expenses such "
        "as urgent repairs, medical costs or temporary income disruption. "
        "The appropriate amount depends on individual circumstances."
    ),

    "financial literacy": (
        "Financial literacy is the ability to understand and use financial "
        "concepts such as budgeting, saving, borrowing, investing, insurance "
        "and risk management."
    )
}


# -------------------- HELP --------------------

def show_help():
    return """
================ FINANCIAL CHATBOT HELP ================

General:
  help
  topics
  about
  exit
  clear

Financial Information:
  ask <topic>
  what is <topic>
  explain <topic>
  tell me about <topic>

Calculators:
  calculate emi
  calculate simple interest
  calculate compound interest
  calculate savings
  calculate inflation
  calculate net worth

Personal Finance:
  set income
  add expense
  show expenses
  budget
  set savings goal
  show savings goal
  financial summary

Examples:
  what is inflation
  explain mutual funds
  calculate emi
  set income
  add expense
  budget

=========================================================
"""


def show_topics():
    return (
        "\nAvailable Finance Topics:\n"
        + "\n".join(f"- {topic.title()}" for topic in TOPICS)
    )


def about_bot():
    return """
Alex is an offline Financial Chatbot designed for personal finance
awareness and basic financial calculations.

The system uses a rule-based knowledge base and local calculations.
It does not require a paid API or internet connection.

It can provide information about budgeting, savings, investments,
loans, insurance, taxation basics, credit, inflation and other
personal finance concepts.

Note: This chatbot is for educational and financial-awareness purposes.
It does not replace advice from a qualified financial professional.
"""


# -------------------- CALCULATORS --------------------

def get_float(prompt):
    while True:
        try:
            value = float(input(prompt))
            if value < 0:
                print("Please enter a non-negative value.")
                continue
            return value
        except ValueError:
            print("Invalid input. Please enter a number.")


def get_positive_float(prompt):
    while True:
        value = get_float(prompt)
        if value > 0:
            return value
        print("Value must be greater than 0.")


def get_positive_int(prompt):
    while True:
        try:
            value = int(input(prompt))
            if value > 0:
                return value
            print("Enter a value greater than 0.")
        except ValueError:
            print("Invalid input. Please enter a whole number.")


def calculate_emi():
    print("\n---------- EMI CALCULATOR ----------")

    principal = get_positive_float("Enter loan amount (₹): ")
    annual_rate = get_float("Enter annual interest rate (%): ")
    months = get_positive_int("Enter loan tenure (months): ")

    monthly_rate = annual_rate / 12 / 100

    if monthly_rate == 0:
        emi = principal / months
        total_payment = principal
        total_interest = 0
    else:
        factor = (1 + monthly_rate) ** months
        emi = principal * monthly_rate * factor / (factor - 1)
        total_payment = emi * months
        total_interest = total_payment - principal

    return (
        f"\nLoan Amount: ₹{principal:,.2f}\n"
        f"Monthly EMI: ₹{emi:,.2f}\n"
        f"Total Payment: ₹{total_payment:,.2f}\n"
        f"Total Interest: ₹{total_interest:,.2f}"
    )


def calculate_simple_interest():
    print("\n------ SIMPLE INTEREST CALCULATOR ------")

    principal = get_positive_float("Enter principal amount (₹): ")
    rate = get_float("Enter annual interest rate (%): ")
    years = get_positive_float("Enter time (years): ")

    interest = (principal * rate * years) / 100
    amount = principal + interest

    return (
        f"\nPrincipal: ₹{principal:,.2f}\n"
        f"Interest: ₹{interest:,.2f}\n"
        f"Final Amount: ₹{amount:,.2f}"
    )


def calculate_compound_interest():
    print("\n---- COMPOUND INTEREST CALCULATOR ----")

    principal = get_positive_float("Enter principal amount (₹): ")
    rate = get_float("Enter annual interest rate (%): ")
    years = get_positive_float("Enter time (years): ")
    frequency = get_positive_int(
        "Enter compounding frequency per year (e.g. 12 for monthly): "
    )

    amount = principal * (
        1 + (rate / 100) / frequency
    ) ** (frequency * years)

    interest = amount - principal

    return (
        f"\nPrincipal: ₹{principal:,.2f}\n"
        f"Compound Interest: ₹{interest:,.2f}\n"
        f"Final Amount: ₹{amount:,.2f}"
    )


def calculate_savings():
    print("\n--------- SAVINGS CALCULATOR ---------")

    monthly_income = get_positive_float("Enter monthly income (₹): ")
    monthly_expenses = get_float("Enter monthly expenses (₹): ")

    savings = monthly_income - monthly_expenses

    if monthly_income == 0:
        saving_rate = 0
    else:
        saving_rate = (savings / monthly_income) * 100

    if savings > 0:
        message = "You have a positive monthly surplus."
    elif savings == 0:
        message = "Your income and expenses are equal."
    else:
        message = "Your expenses are higher than your income."

    return (
        f"\nMonthly Income: ₹{monthly_income:,.2f}\n"
        f"Monthly Expenses: ₹{monthly_expenses:,.2f}\n"
        f"Monthly Savings/Surplus: ₹{savings:,.2f}\n"
        f"Savings Rate: {saving_rate:.2f}%\n"
        f"{message}"
    )


def calculate_inflation():
    print("\n--------- INFLATION CALCULATOR ---------")

    current_value = get_positive_float(
        "Enter current amount/value (₹): "
    )
    inflation_rate = get_float(
        "Enter expected annual inflation rate (%): "
    )
    years = get_positive_float("Enter number of years: ")

    future_value = current_value * (
        1 + inflation_rate / 100
    ) ** years

    return (
        f"\nCurrent Value: ₹{current_value:,.2f}\n"
        f"Inflation Rate: {inflation_rate:.2f}%\n"
        f"Period: {years:g} years\n"
        f"Estimated Future Cost: ₹{future_value:,.2f}"
    )


def calculate_net_worth(data):
    print("\n----------- NET WORTH CALCULATOR -----------")

    assets = get_float("Enter total assets value (₹): ")
    liabilities = get_float("Enter total liabilities (₹): ")

    net_worth = assets - liabilities

    return (
        f"\nTotal Assets: ₹{assets:,.2f}\n"
        f"Total Liabilities: ₹{liabilities:,.2f}\n"
        f"Net Worth: ₹{net_worth:,.2f}"
    )


# -------------------- PERSONAL FINANCE --------------------

def set_income(data):
    income = get_positive_float("\nEnter your monthly income (₹): ")
    data["income"] = income
    save_data(data)

    return f"Monthly income saved: ₹{income:,.2f}"


def add_expense(data):
    print("\n------------- ADD EXPENSE -------------")

    amount = get_positive_float("Enter expense amount (₹): ")
    category = input("Enter category (food/rent/travel/etc.): ").strip()

    if not category:
        category = "other"

    description = input("Enter description: ").strip()

    expense = {
        "amount": amount,
        "category": category.lower(),
        "description": description or "No description",
        "date": datetime.now().strftime("%Y-%m-%d %H:%M")
    }

    data["expenses"].append(expense)
    save_data(data)

    return (
        f"Expense added successfully.\n"
        f"Amount: ₹{amount:,.2f}\n"
        f"Category: {category.lower()}"
    )


def show_expenses(data):
    expenses = data.get("expenses", [])

    if not expenses:
        return "No expenses recorded yet."

    lines = ["\n--------------- EXPENSES ---------------"]

    total = 0

    for index, expense in enumerate(expenses, start=1):
        total += expense["amount"]

        lines.append(
            f"{index}. ₹{expense['amount']:,.2f} | "
            f"{expense['category'].title()} | "
            f"{expense['description']} | "
            f"{expense['date']}"
        )

    lines.append("-----------------------------------------")
    lines.append(f"Total Expenses: ₹{total:,.2f}")

    return "\n".join(lines)


def expense_by_category(data):
    expenses = data.get("expenses", [])

    if not expenses:
        return "No expenses recorded yet."

    totals = {}

    for expense in expenses:
        category = expense["category"]
        totals[category] = totals.get(category, 0) + expense["amount"]

    lines = ["\n---------- EXPENSE CATEGORY SUMMARY ----------"]

    for category, amount in sorted(
        totals.items(),
        key=lambda item: item[1],
        reverse=True
    ):
        lines.append(f"{category.title()}: ₹{amount:,.2f}")

    lines.append("----------------------------------------------")
    lines.append(
        f"Total: ₹{sum(totals.values()):,.2f}"
    )

    return "\n".join(lines)


def budget_summary(data):
    income = data.get("income", 0.0)
    expenses = data.get("expenses", [])

    total_expenses = sum(
        expense["amount"] for expense in expenses
    )

    remaining = income - total_expenses

    if income <= 0:
        return (
            "No income has been recorded yet.\n"
            "Use 'set income' to create your budget."
        )

    spending_percentage = (
        total_expenses / income
    ) * 100

    savings_percentage = (
        remaining / income
    ) * 100

    if remaining < 0:
        recommendation = (
            "Your recorded expenses exceed your income. "
            "Review discretionary spending and recurring costs."
        )
    elif spending_percentage > 80:
        recommendation = (
            "A large portion of your income is already allocated "
            "to recorded expenses. Consider increasing your savings buffer."
        )
    elif savings_percentage >= 20:
        recommendation = (
            "Your recorded budget leaves a positive savings surplus. "
            "You can allocate part of it toward financial goals."
        )
    else:
        recommendation = (
            "You have a positive balance. Review your expenses "
            "and set a specific savings target."
        )

    return (
        f"\n--------------- BUDGET SUMMARY ---------------\n"
        f"Monthly Income: ₹{income:,.2f}\n"
        f"Recorded Expenses: ₹{total_expenses:,.2f}\n"
        f"Remaining Balance: ₹{remaining:,.2f}\n"
        f"Expense Ratio: {spending_percentage:.2f}%\n"
        f"Potential Savings Ratio: {savings_percentage:.2f}%\n\n"
        f"Suggestion: {recommendation}"
    )


def set_savings_goal(data):
    print("\n----------- SAVINGS GOAL -----------")

    goal_name = input("Enter goal name: ").strip()

    if not goal_name:
        goal_name = "My Savings Goal"

    target = get_positive_float("Enter target amount (₹): ")
    saved = get_float("Enter amount already saved (₹): ")

    data["savings_goal"] = {
        "name": goal_name,
        "target": target,
        "saved": saved
    }

    save_data(data)

    remaining = max(target - saved, 0)

    return (
        f"\nSavings goal saved.\n"
        f"Goal: {goal_name}\n"
        f"Target: ₹{target:,.2f}\n"
        f"Saved: ₹{saved:,.2f}\n"
        f"Remaining: ₹{remaining:,.2f}"
    )


def show_savings_goal(data):
    goal = data.get("savings_goal")

    if not goal:
        return (
            "No savings goal has been created yet.\n"
            "Use 'set savings goal' to create one."
        )

    target = goal["target"]
    saved = goal["saved"]
    remaining = max(target - saved, 0)

    progress = min((saved / target) * 100, 100)

    return (
        f"\n------------ SAVINGS GOAL ------------\n"
        f"Goal: {goal['name']}\n"
        f"Target: ₹{target:,.2f}\n"
        f"Saved: ₹{saved:,.2f}\n"
        f"Remaining: ₹{remaining:,.2f}\n"
        f"Progress: {progress:.2f}%"
    )


def financial_summary(data):
    income = data.get("income", 0.0)
    expenses = data.get("expenses", [])

    total_expenses = sum(
        expense["amount"] for expense in expenses
    )

    balance = income - total_expenses

    goal = data.get("savings_goal")

    result = (
        "\n============== FINANCIAL SUMMARY ==============\n"
        f"Monthly Income: ₹{income:,.2f}\n"
        f"Recorded Expenses: ₹{total_expenses:,.2f}\n"
        f"Remaining Balance: ₹{balance:,.2f}\n"
    )

    if goal:
        remaining_goal = max(
            goal["target"] - goal["saved"], 0
        )

        result += (
            f"Savings Goal: {goal['name']}\n"
            f"Goal Remaining: ₹{remaining_goal:,.2f}\n"
        )
    else:
        result += "Savings Goal: Not set\n"

    result += "==============================================="

    return result


# -------------------- QUERY PROCESSING --------------------

def find_topic(user):
    if user in TOPICS:
        return user

    # Try exact phrase matching inside the user's sentence.
    for topic in sorted(TOPICS, key=len, reverse=True):
        if topic in user:
            return topic

    return None


def topic_response(user):
    topic = find_topic(user)

    if topic:
        return TOPICS[topic]

    return None


def get_response(user, data):
    user = user.lower().strip()

    if not user:
        return "Please enter a command or question."

    # Help
    if user in {"help", "help commands", "commands"}:
        return show_help()

    if user in {"help topics", "topics"}:
        return show_topics()

    # About
    if user == "about":
        return about_bot()

    # Calculators
    if user in {"calculate emi", "emi calculator", "emi"}:
        return calculate_emi()

    if user in {
        "calculate simple interest",
        "simple interest calculator",
        "simple interest"
    }:
        return calculate_simple_interest()

    if user in {
        "calculate compound interest",
        "compound interest calculator",
        "compound interest"
    }:
        return calculate_compound_interest()

    if user in {
        "calculate savings",
        "savings calculator"
    }:
        return calculate_savings()

    if user in {
        "calculate inflation",
        "inflation calculator"
    }:
        return calculate_inflation()

    if user in {
        "calculate net worth",
        "net worth calculator",
        "net worth"
    }:
        return calculate_net_worth(data)

    # Personal finance commands
    if user in {"set income", "add income"}:
        return set_income(data)

    if user in {"add expense", "record expense"}:
        return add_expense(data)

    if user in {"show expenses", "expenses", "expense list"}:
        return show_expenses(data)

    if user in {
        "expense summary",
        "expense categories",
        "categories"
    }:
        return expense_by_category(data)

    if user in {"budget", "budget summary", "my budget"}:
        return budget_summary(data)

    if user in {"set savings goal", "create savings goal"}:
        return set_savings_goal(data)

    if user in {"show savings goal", "savings goal"}:
        return show_savings_goal(data)

    if user in {
        "financial summary",
        "my financial summary",
        "summary"
    }:
        return financial_summary(data)

    # Topic questions
    response = topic_response(user)

    if response:
        return response

    # Greetings
    if user in {"hi", "hello", "hey", "hii", "hiii"}:
        return (
            "Hello! 👋 I am Alex, your Financial Chatbot.\n"
            "You can ask me about budgeting, savings, investments, "
            "loans, taxes, insurance, credit and more.\n"
            "Type 'help' to see all commands."
        )

    # Financial keyword guidance
    financial_keywords = [
        "money", "finance", "financial", "budget",
        "saving", "investment", "loan", "tax",
        "insurance", "expense", "income", "interest",
        "stock", "mutual fund", "credit", "inflation"
    ]

    if any(keyword in user for keyword in financial_keywords):
        return (
            "I can help with that financial topic. Try asking:\n"
            "'what is budgeting'\n"
            "'explain investment'\n"
            "'what is inflation'\n"
            "or type 'topics' to see all supported topics."
        )

    return (
        "I couldn't match that question to my current financial "
        "knowledge base.\n\n"
        "Try 'help', 'topics', or ask about budgeting, savings, "
        "investment, EMI, loans, tax, insurance, credit, inflation "
        "or financial planning."
    )


# -------------------- MAIN PROGRAM --------------------

def main():
    data = load_data()

    print("""
=========================================================
          🤖 ALEX - FINANCIAL CHATBOT
=========================================================
Offline Personal Finance Assistant

Type 'help'   → Show available commands
Type 'topics' → Show financial topics
Type 'exit'   → Quit chatbot
=========================================================
""")

    while True:
        try:
            user_input = input("\nYou: ").strip()

            if user_input.lower() in {"exit", "quit", "bye"}:
                print("Alex: Goodbye! 👋")
                break

            if user_input.lower() == "clear":
                os.system("clear")
                print("Alex: Screen cleared.")
                continue

            response = get_response(user_input, data)
            print(f"\nAlex: {response}")

        except KeyboardInterrupt:
            print("\n\nAlex: Goodbye! 👋")
            break

        except EOFError:
            print("\nAlex: Goodbye! 👋")
            break


if __name__ == "__main__":
    main()
