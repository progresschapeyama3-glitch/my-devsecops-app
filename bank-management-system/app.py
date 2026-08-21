from flask import Flask, render_template, request, redirect, url_for, flash
from services.bank_service import BankService
from repositories.account_repository import InMemoryAccountRepository
from services.notification_service import NotificationService

app = Flask(__name__)
app.secret_key = "change-this-secret-key"

repository = InMemoryAccountRepository()
notifications = NotificationService()
bank = BankService(repository, notifications)


@app.route("/")
def index():
    accounts = repository.all_accounts()
    total_balance = sum(account.balance for account in accounts)
    return render_template(
        "index.html",
        accounts=accounts,
        total_balance=total_balance,
        account_count=len(accounts),
    )


@app.route("/create-account", methods=["GET", "POST"])
def create_account():
    if request.method == "POST":
        try:
            customer_id = request.form["customer_id"].strip()
            name = request.form["name"].strip()
            email = request.form["email"].strip()
            account_number = request.form["account_number"].strip()
            account_type = request.form["account_type"].strip()
            initial_balance = float(request.form["initial_balance"] or 0)

            bank.create_account(
                customer_id=customer_id,
                name=name,
                email=email,
                account_number=account_number,
                account_type=account_type,
                initial_balance=initial_balance,
            )

            flash("Account created successfully.", "success")
            return redirect(url_for("index"))

        except (ValueError, KeyError) as exc:
            flash(str(exc), "danger")

    return render_template("create_account.html")


@app.route("/account/<account_number>")
def account_details(account_number):
    try:
        account = bank.get_account(account_number)
        return render_template(
            "account.html",
            account=account,
            transactions=account.transactions,
        )
    except ValueError as exc:
        flash(str(exc), "danger")
        return redirect(url_for("index"))


@app.route("/deposit/<account_number>", methods=["POST"])
def deposit(account_number):
    try:
        amount = float(request.form["amount"])
        bank.deposit(account_number, amount)
        flash("Deposit completed successfully.", "success")
    except (ValueError, KeyError) as exc:
        flash(str(exc), "danger")
    return redirect(url_for("account_details", account_number=account_number))


@app.route("/withdraw/<account_number>", methods=["POST"])
def withdraw(account_number):
    try:
        amount = float(request.form["amount"])
        bank.withdraw(account_number, amount)
        flash("Withdrawal completed successfully.", "success")
    except (ValueError, KeyError) as exc:
        flash(str(exc), "danger")
    return redirect(url_for("account_details", account_number=account_number))


@app.route("/transfer/<account_number>", methods=["POST"])
def transfer(account_number):
    try:
        destination = request.form["destination_account"].strip()
        amount = float(request.form["amount"])
        bank.transfer(account_number, destination, amount)
        flash("Transfer completed successfully.", "success")
    except (ValueError, KeyError) as exc:
        flash(str(exc), "danger")
    return redirect(url_for("account_details", account_number=account_number))


@app.route("/account/<account_number>/transactions")
def transactions(account_number):
    try:
        account = bank.get_account(account_number)
        return render_template(
            "transactions.html",
            account=account,
            transactions=account.transactions,
        )
    except ValueError as exc:
        flash(str(exc), "danger")
        return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
