import random
import pandas as pd


class BitcoinSimulation:
    def __init__(self, initial_cash=1000, bitcoin_price_data=None, average_decline=-0.2637, average_increase=0.8879,
                 average_flat_change=-0.0091):
        self.initial_cash = initial_cash
        self.bitcoin_price_data = bitcoin_price_data
        self.average_decline = average_decline
        self.average_increase = average_increase
        self.average_flat_change = average_flat_change

    def run_simulation(self):
        cash = self.initial_cash
        btc_owned = 0
        history = []

        for quarter in self.bitcoin_price_data:
            # İlk hafta yükselmişse BTC alımı
            if quarter['first_week_trend'] == 'increase':
                btc_to_buy = cash * self.average_increase
                cash -= btc_to_buy
                btc_owned += btc_to_buy / quarter['previous_close']

            # Son çeyrek fiyatı ile BTC satışı
            btc_to_sell = btc_owned
            cash += btc_to_sell * quarter['current_close']
            btc_owned = 0

            # İstatistiklere göre sonraki çeyrek stratejisi
            if quarter['trend'] == 'increase':
                probability = self.average_increase
            elif quarter['trend'] == 'decrease':
                probability = self.average_decline
            else:
                probability = self.average_flat_change

            # Sonraki çeyrekte işlem yapılacak mı yoksa sadece nakit mi tutulacak?
            if random.random() < probability:
                # BTC alımı
                btc_to_buy = cash * probability
                cash -= btc_to_buy
                btc_owned += btc_to_buy / quarter['current_close']

            # Simülasyon geçmişi kayıt
            history.append({
                'quarter': quarter['quarter'],
                'cash': cash,
                'btc_owned': btc_owned,
                'btc_price': quarter['current_close']
            })

        return history
