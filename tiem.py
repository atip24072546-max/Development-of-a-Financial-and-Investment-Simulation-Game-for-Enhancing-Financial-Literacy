from dataclasses import dataclass
import random

@dataclass
class EconomicState:
    year: int
    market_trend: str
    inflation_rate: float
    market_return_adjustment: float

class EconomyModel:
    def __init__(self, base_inflation: float = 0.025, seed: int = None):
        if seed is not None:
            random.seed(seed)
            self.base_inflation = base_inflation

    def generate_yearly_economy(self, year: int) -> EconomicState:
        scenarios = [
            ("ขาขึ้น (Bullish)",0.030,0.03),
            ("ปกติ (Neutral)",0.025,0.00),
            ("ขาลง (Bearish)",0.015,-0.04)
        ]
        trend, inflation, adj = random.choices(
            scenarios, weights = [0.25, 0.55, 0.20], k=1
        )[0]

        return EconomicState(
            year=year,
            market_trend=trend,
            inflation_rate=inflation,
            market_return_adjustment=adj
        )

    def calculate_res(self, base_return: float, economic_state: EconomicState) -> float:
        effective_return = base_return + economic_state.market_return_adjustment
        return max(-0.5, effective_return)