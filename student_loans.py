import tkinter as tk
import math


def check_loan_parameters(loan_amount, interest_rate_year, loan_term, loan_term_units):
    """Checks that the parameters of the loan are valid.

    Params:
        loan_amount (float): loan amount in dollars
        interest_rate_year (float) interest rate (%)
        loan_term (int): length of loan (units in loan_term_units)
        loan_term_units (str): "months" or "years", unit of loan_term
        
    Returns:
        (str) the error message to show if a parameter is invalid or
        None if all parameters are valid
    """
    if loan_amount == 0:
        return("Please enter valid loan amount")

    if interest_rate_year == 0:
        return("Please enter valid interest rate")

    if loan_term == 0:
        return("Please enter valid loan term")

    if (loan_term_units != "months") and (loan_term_units != "years"):
        return("Please select 'years' or 'months' for the loan term")


def fill_missing_fields(entries, fields_to_fill):
    for field in fields_to_fill:
        if entries[field].get().strip() == "":
            entries[field].delete(0, tk.END)
            entries[field].insert(0, "0")


def calculate_monthly_payment(loan_amount, interest_rate_year, loan_term, loan_term_units="years"):
    """Calculates monthly payment of a loan.
    
    Params:
        loan_amount (float): loan amount in dollars
        interest_rate_year (float) interest rate (%)
        loan_term (int): length of loan (units in loan_term_units)
        loan_term_units (str): "months" or "years", unit of loan_term
        
    Returns:
        (float) amount of each month's payment or (str) the message to show
    """
    param_check = check_loan_parameters(loan_amount, interest_rate_year, loan_term, loan_term_units)

    if isinstance(param_check, str):
        return param_check

    interest_rate_month = interest_rate_year / 12
    
    if loan_term_units == "years":
        number_of_payments = loan_term * 12
    elif loan_term_units == "months":
        number_of_payments = loan_term
        
    monthly_payment = (
        loan_amount * interest_rate_month / 100 *
        (1 + interest_rate_month / 100) ** number_of_payments /
        ((1 + interest_rate_month / 100) ** number_of_payments - 1)
    )
    
    return monthly_payment


def calculate_time_to_repay(loan_amount, interest_rate_year, loan_term, loan_term_units="years", monthly_payment_additional=0):
    """Calculates how long it will take to repay a loan with additional monthly payments.
    
    Params:
        loan_amount (float): loan amount in dollars
        interest_rate_year (float): annual interest rate (%)
        loan_term (int): length of loan (units in loan_term_units)
        loan_term_units (string, optional): "months" or "years", unit of loan_term
        monthly_payment_additional (float, optional): additional monthly payment amount for earlier payoff
        
    Returns:
        (float) number of payments required to repay the loan or (str) the message to show
    """
    param_check = check_loan_parameters(loan_amount, interest_rate_year, loan_term, loan_term_units)

    if isinstance(param_check, str):
        return param_check

    monthly_payment_base = calculate_monthly_payment(
        loan_amount,
        interest_rate_year,
        loan_term,
        loan_term_units=loan_term_units
    )
    
    interest_rate_month = interest_rate_year / 12
    
    number_of_payments_required = (
        - math.log(1 - (interest_rate_month / 100 * loan_amount / (monthly_payment_base + monthly_payment_additional))) /
        math.log(1 + interest_rate_month / 100)
    )
    
    return number_of_payments_required


def calculate_monthly_takehome(salary_base, effective_tax_rate, annual_savings):
    """Calculate monthly takehome salary.
    
    Params:
        salary_base (float): annual base salary
        effective_tax_rate (float): estimate of effective tax rate
        annual_retirement_contribution (float): amount to contribute to retirement per year
        
    Returns:
        (float) monthly takehome salary or (str) the message to show
    """

    if salary_base == 0:
        return("Please enter valid salary")
    
    salary_takehome = salary_base * (1 - effective_tax_rate / 100) - annual_savings
    return (salary_takehome / 12)


def call_calculate_time_to_repay(entries):
    """Wrapper for calculate_time_tor_repay.

    Params:
        entries (dict): dictionary of GUI entries
    """
    fill_missing_fields(
        entries,
        ["Loan Amount", "Annual Interest Rate", "Loan Term", "Additional Monthly Payment"]
    )
    time_to_repay = calculate_time_to_repay(
        float(entries["Loan Amount"].get()),
        float(entries["Annual Interest Rate"].get()),
        float(entries["Loan Term"].get()),
        loan_term_units=str(entries["Loan Term Units"].get()),
        monthly_payment_additional=float(entries["Additional Monthly Payment"].get())
    )
    entries["Time to Repay"].delete(0, tk.END)
    if str(entries["Repay Time Units"].get()) == "months":
        entries["Time to Repay"].insert(0, "{:d}".format(math.ceil(time_to_repay)))
    elif str(entries["Repay Time Units"].get()) == "years":
        entries["Time to Repay"].insert(0, "{:.1f}".format(time_to_repay/12))
    else:
        entries["Time to Repay"].insert(0, "Please select 'years' or 'months'")


def call_calculate_total_monthly_payment(entries):
    """Wrapper for calculate_total_monthly_payment.

    Params:
        entries (dict): dictionary of GUI entries
    """
    fill_missing_fields(
        entries,
        ["Loan Amount", "Annual Interest Rate", "Loan Term", "Additional Monthly Payment"]
    )
    monthly_payment_base = calculate_monthly_payment(
        float(entries["Loan Amount"].get()),
        float(entries["Annual Interest Rate"].get()),
        float(entries["Loan Term"].get()),
        loan_term_units=str(entries["Loan Term Units"].get()),
    )
    entries["Total Monthly Payment"].delete(0, tk.END)
    if not isinstance(monthly_payment_base, str):
        total_monthly_payment = monthly_payment_base + float(entries["Additional Monthly Payment"].get())
        entries["Total Monthly Payment"].insert(0, "{:.2f}".format(total_monthly_payment))
    else:
        entries["Total Monthly Payment"].insert(0, monthly_payment_base)


def call_calculate_monthly_takehome(entries):
    """Wrapper for calculate_monthly_takehome.

    Params:
        entries (dict): dictionary of GUI entries
    """
    fill_missing_fields(
        entries,
        ["Loan Amount", "Annual Interest Rate", "Loan Term", "Additional Monthly Payment", "Salary", "Effective Tax Rate", "Annual Savings Target"]
    )
    monthly_takehome = calculate_monthly_takehome(
        float(entries["Salary"].get()),
        float(entries["Effective Tax Rate"].get()),
        float(entries["Annual Savings Target"].get()),
    )
    if float(entries["Loan Amount"].get()) == 0:
        monthly_payment_base = 0
        additional_monthly_payment = float(0)
    else:
        monthly_payment_base = calculate_monthly_payment(
            float(entries["Loan Amount"].get()),
            float(entries["Annual Interest Rate"].get()),
            float(entries["Loan Term"].get()),
            loan_term_units=str(entries["Loan Term Units"].get()),
        )
        additional_monthly_payment = float(entries["Additional Monthly Payment"].get())
    entries["Monthly Take-home Salary"].delete(0, tk.END)
    if not isinstance(monthly_takehome, str) and not isinstance(monthly_payment_base, str):
        entries["Monthly Take-home Salary"].insert(0, "{:.2f}".format(monthly_takehome - monthly_payment_base - additional_monthly_payment))
    elif isinstance(monthly_takehome, str):
        entries["Monthly Take-home Salary"].insert(0, monthly_takehome)  # error for salary calculation
    elif isinstance(monthly_payment_base, str):
        entries["Monthly Take-home Salary"].insert(0, monthly_payment_base)  # error from loan calculation


def make_form(root):
    """Make the GUI.

    Params:
        root (Tk()): tkinter widget or main window

    Returns:
        (dict) Dictionary mapping fields to their values
    """
    root.title("Loan and Salary Calculator")
    entries = {}
    fields = (
        "Loan Amount",
        "Annual Interest Rate",
        "Loan Term",
        "Additional Monthly Payment",
        "Salary",
        "Effective Tax Rate",
        "Annual Savings Target",
        "Total Monthly Payment",
        "Time to Repay",
        "Monthly Take-home Salary",
    )
    money_fields = [
        "Loan Amount",
        "Additional Monthly Payment",
        "Salary",
        "Annual Savings Target",
        "Total Monthly Payment",
        "Monthly Take-home Salary",
    ]
    percent_fields = [
        "Annual Interest Rate",
        "Effective Tax Rate",
    ]
    loan_term_units = tk.StringVar(root, "Loan Term Units")
    repay_time_units = tk.StringVar(root, "Repay Time Units")

    for field in fields:
        if field == "Total Monthly Payment":
            row = tk.Frame(root)
            button_total_monthly_payment = tk.Button(
                row,
                text="Total Monthly Payment",
                command=(
                    lambda e=entries: call_calculate_total_monthly_payment(e)
                )
            )
            button_total_monthly_payment.pack(side=tk.LEFT, padx=5, pady=5)
            button_time_to_repay = tk.Button(
                row,
                text="Time to Repay",
                command=(
                    lambda e=entries: call_calculate_time_to_repay(e)
                )
            )
            button_time_to_repay.pack(side=tk.LEFT, padx=5, pady=5)
            button_monthly_takehome_salary = tk.Button(
                row,
                text="Monthly Take-home Salary",
                command=(
                    lambda e=entries: call_calculate_monthly_takehome(e)
                )
            )
            button_monthly_takehome_salary.pack(side=tk.LEFT, padx=5, pady=5)
            row.pack(side=tk.TOP, 
                     fill=tk.X, 
                     padx=5, 
                     pady=5)
        
        row = tk.Frame(root)
        lab = tk.Label(row, width=22, text=field+": ", anchor='w')
        ent = tk.Entry(row)
        ent.insert(0, "0")
        row.pack(side=tk.TOP,
                 fill=tk.X, 
                 padx=5, 
                 pady=5)
        lab.pack(side=tk.LEFT)
        if field in percent_fields:
            unit = tk.Label(row, text="%")
            unit.pack(side=tk.RIGHT)
        if field == "Loan Term":
            tk.Radiobutton(
                row,
                text="months",
                padx = 5,
                variable=loan_term_units,
                value="months"
            ).pack(side=tk.RIGHT)
            tk.Radiobutton(
                row,
                text="years",
                padx = 5,
                variable=loan_term_units,
                value="years"
            ).pack(side=tk.RIGHT)
            entries["Loan Term Units"] = loan_term_units
        if field == "Time to Repay":
            tk.Radiobutton(
                row,
                text="months",
                padx = 5,
                variable=repay_time_units,
                value="months"
            ).pack(side=tk.RIGHT)
            tk.Radiobutton(
                row,
                text="years",
                padx = 5,
                variable=repay_time_units,
                value="years"
            ).pack(side=tk.RIGHT)
            entries["Repay Time Units"] = repay_time_units
        ent.pack(side=tk.RIGHT, 
                 expand=tk.YES, 
                 fill=tk.X)
        entries[field] = ent
        if field in money_fields:
            unit = tk.Label(row, text="$")
            unit.pack(side=tk.RIGHT)
    return entries
    

if __name__ == "__main__":
    root = tk.Tk()

    entries = make_form(root)

    button_quit = tk.Button(root, text='Quit', command=root.destroy)
    button_quit.pack(side=tk.LEFT, padx=5, pady=5)

    root.mainloop()
