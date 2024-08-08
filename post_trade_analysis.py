import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

class PostTradeAnalysis:
    def __init__(self, returns_series):
        self.returns_series = returns_series
        self.cumulative_returns = self.calculate_cumulative_returns()
        self.max_drawdown = self.calculate_max_drawdown()
        self.sharpe_ratio = self.calculate_sharpe_ratio()
        self.sortino_ratio = self.calculate_sortino_ratio()
        self.hit_ratio = self.calculate_hit_ratio()
    
    def calculate_cumulative_returns(self):
        # Compute cumulative returns using the cumulative product of (1 + returns)
        cumulative_returns = (1 + self.returns_series).cumprod() - 1
        return cumulative_returns

    def calculate_max_drawdown(self):
        # Calculate maximum drawdown (peak-to-trough decline) in cumulative returns
        cum_returns = (1 + self.returns_series).cumprod()
        peak = cum_returns.cummax()
        drawdown = (cum_returns - peak) / peak
        max_drawdown = drawdown.min()
        return max_drawdown

    def calculate_sharpe_ratio(self, risk_free_rate=0):
        # Compute Sharpe ratio (risk-adjusted return)
        excess_returns = self.returns_series - risk_free_rate
        sharpe_ratio = excess_returns.mean() / excess_returns.std() * np.sqrt(252)
        return sharpe_ratio

    def calculate_sortino_ratio(self, risk_free_rate=0):
        # Compute Sortino ratio (adjusted for downside risk)
        excess_returns = self.returns_series - risk_free_rate
        downside_std = excess_returns[excess_returns < 0].std()
        sortino_ratio = excess_returns.mean() / downside_std * np.sqrt(252)
        return sortino_ratio

    def calculate_hit_ratio(self):
        # Calculate proportion of positive returns
        hit_ratio = (self.returns_series > 0).sum() / len(self.returns_series)
        return hit_ratio

    def generate_monthly_returns_heatmap(self):
        # Resample returns to monthly frequency and create a heatmap
        monthly_returns = self.returns_series.resample('M').apply(lambda x: (1 + x).prod() - 1)
        monthly_returns = monthly_returns.unstack().T
        
        plt.figure(figsize=(12, 8))
        sns.heatmap(monthly_returns, annot=True, fmt=".2f", cmap='coolwarm', center=0)
        plt.title("Monthly Returns Heatmap")
        plt.show()

    def generate_plots(self):
        # Plot cumulative returns over time
        plt.figure(figsize=(12, 8))
        plt.plot(self.cumulative_returns, label="Cumulative Returns")
        plt.title("Cumulative Returns")
        plt.legend()
        plt.show()

        # Display calculated ratios
        print(f"Sharpe Ratio: {self.sharpe_ratio:.2f}")
        print(f"Sortino Ratio: {self.sortino_ratio:.2f}")
        print(f"Hit Ratio: {self.hit_ratio:.2f}")
        print(f"Maximum Drawdown: {self.max_drawdown:.2f}")

# Example Usage
if __name__ == "__main__":
    # Sample return series for demonstration
    date_range = pd.date_range(start='2023-01-01', periods=252, freq='B')
    sample_returns = pd.Series(np.random.randn(len(date_range)) / 100, index=date_range)

    analysis = PostTradeAnalysis(sample_returns)
    analysis.generate_plots()
    analysis.generate_monthly_returns_heatmap()
