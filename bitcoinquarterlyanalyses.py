import yfinance as yf
import pandas as pd


class BitcoinQuarterlyAnalysis:
    def __init__(self, ticker='BTC-USD', start_date='2014-01-01', end_date=None):
        self.ticker = ticker
        self.start_date = start_date
        self.end_date = end_date
        self.data = self._fetch_data()
        self.quarterly_data = self._resample_to_quarters()
        self.analysis = self._analyze_quarters()
        self.statistics = self._calculate_statistics()

    def _fetch_data(self):
        """Fetch historical data for the given ticker and date range."""
        return yf.download(self.ticker, start=self.start_date, end=self.end_date)

    def _resample_to_quarters(self):
        """Resample data to quarterly frequency and calculate the closing price at the end of each quarter."""
        return self.data['Adj Close'].resample('Q').last()

    def _analyze_quarters(self):
        """Analyze each quarter to determine if it was an increase, decrease, or flat movement."""
        results = []
        for i in range(1, len(self.quarterly_data)):
            previous = self.quarterly_data[i - 1]
            current = self.quarterly_data[i]
            percentage_change = (current - previous) / previous * 100

            if percentage_change > 10:
                trend = 'increase'
            elif percentage_change < -10:
                trend = 'decrease'
            else:
                trend = 'flat'

            # İlk haftanın değişim yüzdesini hesapla
            quarter_start = self.quarterly_data.index[i].to_period('Q').start_time
            quarter_end = quarter_start + pd.DateOffset(days=7)
            first_week_data = self.data[(self.data.index >= quarter_start) & (self.data.index < quarter_end)]
            if not first_week_data.empty:
                first_week_close = first_week_data['Adj Close'].iloc[-1]
                first_week_percentage_change = (first_week_close - previous) / previous * 100
                first_week_trend = 'increase' if first_week_percentage_change > 0 else 'decrease'
            else:
                first_week_percentage_change = None
                first_week_trend = 'unknown'

            results.append({
                'quarter': self.quarterly_data.index[i],
                'previous_close': previous,
                'current_close': current,
                'percentage_change': percentage_change,
                'trend': trend,
                'first_week_percentage_change': first_week_percentage_change,
                'first_week_trend': first_week_trend
            })
        return results

    def _calculate_statistics(self):
        """Calculate statistics based on the first week's performance."""
        increase_previous_quarter = [q for q in self.analysis if q['trend'] == 'increase']
        decrease_previous_quarter = [q for q in self.analysis if q['trend'] == 'decrease']

        increase_first_week_increase_prev = [q for q in increase_previous_quarter if
                                             q['first_week_trend'] == 'increase']
        decrease_first_week_increase_prev = [q for q in increase_previous_quarter if
                                             q['first_week_trend'] == 'decrease']

        increase_first_week_decrease_prev = [q for q in decrease_previous_quarter if
                                             q['first_week_trend'] == 'increase']
        decrease_first_week_decrease_prev = [q for q in decrease_previous_quarter if
                                             q['first_week_trend'] == 'decrease']

        increase_after_increase_prev_probability = (len(increase_first_week_increase_prev) / len(
            increase_previous_quarter)) * 100 if len(increase_previous_quarter) > 0 else 0
        decrease_after_increase_prev_probability = (len(decrease_first_week_increase_prev) / len(
            increase_previous_quarter)) * 100 if len(increase_previous_quarter) > 0 else 0

        increase_after_decrease_prev_probability = (len(increase_first_week_decrease_prev) / len(
            decrease_previous_quarter)) * 100 if len(decrease_previous_quarter) > 0 else 0
        decrease_after_decrease_prev_probability = (len(decrease_first_week_decrease_prev) / len(
            decrease_previous_quarter)) * 100 if len(decrease_previous_quarter) > 0 else 0

        return {
            'increase_after_increase_prev_probability': increase_after_increase_prev_probability,
            'decrease_after_increase_prev_probability': decrease_after_increase_prev_probability,
            'increase_after_decrease_prev_probability': increase_after_decrease_prev_probability,
            'decrease_after_decrease_prev_probability': decrease_after_decrease_prev_probability
        }

    def get_quarterly_analysis(self):
        """Return the analysis of quarterly movements."""
        return self.analysis

    def get_statistics(self):
        """Return the calculated statistics."""
        return self.statistics

    def save_to_csv(self, analysis_filepath, statistics_filepath):
        """Save the analysis and statistics to CSV files."""
        # Save analysis
        analysis_df = pd.DataFrame(self.analysis)
        analysis_df.to_csv(analysis_filepath, index=False)

        # Save statistics
        statistics_df = pd.DataFrame([self.statistics])
        statistics_df.to_csv(statistics_filepath, index=False)


# BitcoinQuarterlyAnalysis sınıfını kullanarak bir örnek oluşturup analizi çalıştırabiliriz.
if __name__ == "__main__":
    analysis = BitcoinQuarterlyAnalysis()
    quarterly_analysis = analysis.get_quarterly_analysis()
    statistics = analysis.get_statistics()

    for quarter in quarterly_analysis:
        print(quarter)

    print("Statistics:")
    print(statistics)

    # Analiz ve istatistikleri CSV dosyasına kaydet
    analysis.save_to_csv('quarterly_analysis.csv', 'statistics.csv')
