from datetime import datetime
from lumibot.brokers import Alpaca
from lumibot.traders import Trader
from strategy import MLTrader
from config import ALPACA_CREDS

# Example usage
start_date = datetime(2021, 1, 1)
end_date = datetime(2024, 1, 1)
symbols = ["SPY", "AAPL", "GOOGL"]  # Example symbols list
broker = Alpaca(ALPACA_CREDS)
strategy = MLTrader(name='mlstrat', broker=broker,
                    parameters={"symbol": "SPY",
                                "cash_at_risk": .5,
                                "risk_cap": 0.8,
                                "atr_multiple_tp": 6.0,
                                "atr_multiple_sl": 3.0,
                                "max_loss_per_trade": 0.02,
                                "probability_threshold": 0.95,
                                "conservative_threshold": 0.5,
                                "turbulence_threshold": 3})

trader = Trader()
trader.add_strategy(strategy)
trader.run_all()
