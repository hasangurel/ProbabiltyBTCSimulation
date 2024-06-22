import requests
from datetime import datetime

class CryptoPriceAnalyzer:
    def __init__(self, ticker='BTC-USD'):
        self.ticker = ticker
        self.current_price = self._fetch_current_price()
        self.next_quarter_probability = self._calculate_next_quarter_probability()

    def _fetch_current_price(self):
        # Kripto para biriminin anlık fiyatını çekme
        url = f'https://api.coinbase.com/v2/prices/{self.ticker}/spot'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return float(data['data']['amount'])
        else:
            print(f"Hata: {response.status_code} - Fiyat çekilemedi.")
            return None

    def _calculate_next_quarter_probability(self):
        probabilities = {
            'increase_after_increase_prev_probability': 81.25,
            'decrease_after_increase_prev_probability': 18.75,
            'increase_after_decrease_prev_probability': 41.66666666666667,
            'decrease_after_decrease_prev_probability': 58.333333333333336
        }
        return 75.0  # Örnek olarak %75 yeşil olma olasılığı

    def get_current_price(self):
        return self.current_price

    def get_next_quarter_probability(self):
        return self.next_quarter_probability

    def display_analysis(self):
        print(f"Anlık {self.ticker} fiyatı: ${self.current_price:.2f}")
        print(f"Bir sonraki çeyreğin yeşil olma olasılığı: {self.next_quarter_probability}%")

# Örnek kullanım
if __name__ == "__main__":
    analyzer = CryptoPriceAnalyzer()
    analyzer.display_analysis()
