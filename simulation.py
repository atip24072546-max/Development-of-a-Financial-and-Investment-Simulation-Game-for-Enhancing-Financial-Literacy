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

def calculate_annual_invest_capacity(net_cashflow_annual: float) -> float:
    return max(0.0, net_cashflow_annual * 0.6)

def calculate_debt_repayment(debt: float, net_cashflow_annual: float) -> float:
    if debt <= 0:
        return 0.0
    repayment = min(debt,net_cashflow_annual * 0.5)
    remaining_debt = debt - repayment
    return repayment, remaining_debt

def calculate_annual_savings_added(net_cashflow_annual: float) -> float:
    return max(0.0, net_cashflow_annual * 0.4)

def update_investment_portfolio(current_investments: float, annual_addition: float, return_rate: float) -> float:
    return (current_investments + annual_addition) * (1.0 + return_rate)

def calculate_assets_and_net_worth(cash: float, savings: float, investments: float, debt: float) -> Tuple[float, float]:
    assets = cash + savings + investments
    net_worth = assets - debt
    return assets, net_worth

def calculate_goal_progress(net_worth: float, target_wealth: float) -> float:
    if target_wealth <= 0:
        return 0.0
    return min(100.0, (net_worth / target_wealth) * 100)

def calculate_capm(risk_free_rate: float, beta: float, market_return: float) -> float:
    return risk_free_rate + beta * (market_return - risk_free_rate)