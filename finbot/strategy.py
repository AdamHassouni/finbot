from datetime import datetime, timedelta
from alpaca_trade_api import REST
from lumibot.strategies.strategy import Strategy
import numpy as np
from finbert_utiles import estimate_sentiment
from utils import calculate_atr, calculate_var, calculate_cvar, calculate_turbulence, advanced_position_sizing
from config import API_KEY, API_SECRET, BASE_URL

class MLTrader(Strategy):
    def initialize(self, symbol: str = "SPY", cash_at_risk: float = .5, risk_cap: float = 0.8, atr_multiple_tp: float = 6.0, atr_multiple_sl: float = 3.0, max_loss_per_trade: float = 0.02, probability_threshold: float = 0.95, conservative_threshold: float = 0.5, turbulence_threshold: float = 3):
        self.symbol = symbol
        self.sleeptime = "6H" 
        self.cash_at_risk = cash_at_risk
        self.risk_cap = risk_cap
        self.atr_multiple_tp = atr_multiple_tp
        self.atr_multiple_sl = atr_multiple_sl
        self.max_loss_per_trade = max_loss_per_trade
        self.probability_threshold = probability_threshold
        self.conservative_threshold = conservative_threshold
        self.initial_cash = self.get_cash()
        self.api = REST(API_KEY, API_SECRET, BASE_URL)
        self.turbulence_threshold = turbulence_threshold

    def get_dates(self):
        today = self.get_datetime()
        three_days_prior = today - timedelta(days=3)
        return today.strftime('%Y-%m-%d'), three_days_prior.strftime('%Y-%m-%d')

    def get_sentiment(self):
        today, three_days_prior = self.get_dates()
        news = self.api.get_news(symbol=self.symbol, start=three_days_prior, end=today)
        news = [ev.headline for ev in news]
        probability, sentiment = estimate_sentiment(news)
        return probability, sentiment
    
    def on_trading_iteration(self):
        cash = self.get_cash()
        conservative_mode = cash < (self.initial_cash * self.conservative_threshold)
        risk_cap = self.risk_cap if not conservative_mode else self.risk_cap / 2  # Reduce risk in conservative mode
        probability, sentiment = self.get_sentiment()
        last_price = self.get_last_price(self.symbol)
        atr = calculate_atr(self.api, self.symbol)
        
        # Fetch historical returns for the asset
        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
        bars = self.api.get_bars(self.symbol, '1D', start=start_date, end=end_date, feed='iex').df
        returns = bars['close'].pct_change().dropna()
        
        cash, last_price, quantity, atr = advanced_position_sizing(
            returns, cash, last_price, atr, probability
        )
        turbulence = calculate_turbulence(self.api, self.symbol)
        if turbulence > self.turbulence_threshold:
            self.log_message("Turbulence is high, halting trading and selling all positions.")

        if cash > last_price:
            if sentiment == "positive" and probability > self.probability_threshold:
                order = self.create_order(
                    self.symbol,
                    quantity,
                    "buy",
                    type="bracket",
                    take_profit_price=last_price + self.atr_multiple_tp * atr,
                    stop_loss_price=last_price - self.atr_multiple_sl * atr
                )
                self.submit_order(order)
            elif sentiment == "negative" and probability > self.probability_threshold:
                order = self.create_order(
                    self.symbol,
                    quantity,
                    "sell",
                    type="bracket",
                    take_profit_price=last_price - self.atr_multiple_tp * atr,
                    stop_loss_price=last_price + self.atr_multiple_sl * atr
                )
                self.submit_order(order)
