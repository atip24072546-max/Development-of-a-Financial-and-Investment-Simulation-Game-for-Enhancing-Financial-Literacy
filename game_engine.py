from dataclasses import dataclass
from enum import Enum
from typing import List
import simulation
import tiem

class GameState(Enum):
    SETUP = "SETUP" 
    RUNNING = "RUNNING"
    FINISHED = "FINISHED"

@dataclass
class PlayerProfile:
    age: int
    income_monthly: float
    expenses_monthly: float
    savings: float
    debt: float
    sim_duration: int
    retirement_age: int
    target_wealth: float

@dataclass
class FinancialSnapshot:
    year: int
    age: int
    cash: float
    savings: float
    investments: float
    assets: float
    debt: float
    net_worth: float
    progress: float
    repayment: float
    savings_added: float
    return_rate: float
    is_retired: bool

class FinancialGameEngine:
    def __init__(self, profile: PlayerProfile, use_dynamic_economy: bool = False):
        self.profile = profile
        self.state = GameState.SETUP
        self.current_year = 0
        self.current_age = profile.age

        self.net_cashflow_monthly, self.net_cashflow_annual = simulation.calculate_cashflow(
            profile.income_monthly, profile.expenses_monthly
        )
        self.emergency_fund_months = simulation.calculate_emergency_fund_months(
            profile.savings, profile.expenses_monthly
        )
        self.dti = simulation.calculate_dti(profile.debt, profile.income_monthly)

        self.risk_level, self.base_return_rate = simulation.calculate_risk_profile(
            profile.age, profile.debt, self.dti
        )
        self.annual_invest_capacity = simulation.calculate_annual_invest_capacity(self.net_cashflow_annual)

        self.cash = max(0.0, self.net_cashflow_monthly * 3.0)
        self.savings = profile.savings
        self.debt = profile.debt
        self.investments = 0.0
        self.use_dynamic_economy = use_dynamic_economy
        self.economy_model = tiem.EconomyModel()
        self.history: List[FinancialSnapshot] = []

    def start_game(self):
        self.state = GameState.RUNNING

    def step_year(self) -> FinancialSnapshot:
        """รันการจำลองข้ามไป 1 ปี และบันทึกสถานะทางการเงิน"""
        if self.state != GameState.RUNNING:
            raise RuntimeError("เกมยังไม่เริ่มหรือจบการจำลองแล้ว")
        self.current_year += 1
        self.current_age += 1

        if self.use_dynamic_economy:
            econ = self.economy_model.generate_yearly_economy(self.current_year)
            effective_return = self.economy_model.calculate_res(self.base_return_rate, econ)
        else:
            effective_return = self.base_return_rate

        repayment, self.debt = simulation.calculate_debt_repayment(self.debt, self.net_cashflow_annual)

        savings_added = simulation.calculate_annual_savings_added(self.net_cashflow_annual)
        self.savings += savings_added

        self.investments = simulation.update_investment_portfolio(
            self.investments, self.annual_invest_capacity, effective_return
        )

        assets, net_worth = simulation.calculate_assets_and_net_worth(
            self.cash, self.savings, self.investments, self.debt
        )
        progress = simulation.calculate_goal_progress(net_worth, self.profile.target_wealth)
        is_retired = (self.current_age == self.profile.retirement_age)
        snapshot = FinancialSnapshot(
            year=self.current_year,
            age=self.current_age,
            cash=self.cash,
            savings=self.savings,
            investments=self.investments,
            assets=assets,
            debt=self.debt,
            net_worth=net_worth,
            progress=progress,
            repayment=repayment,
            savings_added=savings_added,
            return_rate=effective_return,
            is_retired=is_retired
        )
        self.history.append(snapshot)
        if self.current_year >= self.profile.sim_duration:
            self.state = GameState.FINISHED
        return snapshot

    def is_finished(self) -> bool:
        return self.state == GameState.FINISHED
