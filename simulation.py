from typing import Tuple

def format_currency(amount: float) -> str:
    return f"{amount:,.2f} บาท"

def calculate_cashflow(income_monthly: float,expenses_monthly: float) -> Tuple[float, float]:
    net_monthly = income_monthly - expenses_monthly
    net_annual = net_monthly * 12
    return net_monthly, net_annual

def calculate_emergency_fund_months(savings: float, expenses_monthly: float) -> float:
    if expenses_monthly <= 0:
        return 0.0
    return savings / expenses_monthly

def calculate_dti(debt: float, income_monthly: float) -> float:
    annual_income = income_monthly * 12
    if annual_income <= 0:
        return 0.0
    return (debt / annual_income) * 100

def calculate_risk_profile(age: int, debt: float, dti: float) -> Tuple[str, float]:
    if age < 35 and debt == 0:
        risk_level = "สูง"
        expected_return_rate = 0.08
    elif age < 50 and dti < 30:
        risk_level = "ปานกลาง"
        expected_return_rate = 0.05
    else:
        risk_level = "ต่ำ"
        expected_return_rate = 0.03
    return risk_level, expected_return_rate

