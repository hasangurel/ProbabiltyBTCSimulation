import yfinance as yf
import pandas as pd
import numpy as np

# Hisse senedi simgesi ve veri çekme tarih aralığı
ticker = "BTC-USD"
start_date = "2014-01-01"
end_date = "2024-06-21"

# Yahoo Finance üzerinden verileri çekme
stock_data = yf.download(ticker, start=start_date, end=end_date)

# Veri setinde çeyrekleri belirlemek için tarih sınırlarını hesaplayalım
def get_quarter(date):
    quarter = (date.month - 1) // 3 + 1
    return f"Q{quarter}"

# Veri setine çeyrek sütunu ekleyelim
stock_data['Quarter'] = stock_data.index.to_series().apply(get_quarter)
stock_data['Year'] = stock_data.index.year

# Yıl ve çeyrek bazında yükselme/düşüşü kontrol eden fonksiyon
def classify_trend(start_price, end_price):
    change_percentage = ((end_price - start_price) / start_price) * 100
    if change_percentage >= 10:
        return "Yükseliş", change_percentage
    elif change_percentage <= -10:
        return "Düşüş", change_percentage
    else:
        return "Yatay", change_percentage

# Çeyrek bazında trendleri belirleme
results = []
for (year, quarter), quarter_data in stock_data.groupby(['Year', 'Quarter']):
    if len(quarter_data) > 0:
        start_price = quarter_data.iloc[0]['Close']
        end_price = quarter_data.iloc[-1]['Close']
        trend, change_percentage = classify_trend(start_price, end_price)
        results.append({'Year': year, 'Quarter': quarter, 'Trend': trend, 'Change_Percentage': change_percentage})

# Sonuçları DataFrame'e çevirme
results_df = pd.DataFrame(results)

# Yükseliş ve düşüşlerin ortalama yüzde değişimini hesaplama
avg_increase = results_df[results_df['Trend'] == 'Yükseliş']['Change_Percentage'].mean()
avg_decrease = results_df[results_df['Trend'] == 'Düşüş']['Change_Percentage'].mean()

# Sonuçları yazdırma
print(f"Yükselişlerin ortalama yüzde artışı: {avg_increase:.2f}%")
print(f"Düşüşlerin ortalama yüzde düşüşü: {avg_decrease:.2f}%")

# Her bir trend türünün sayısını ve yüzdesini hesaplama
trend_counts = results_df['Trend'].value_counts()
trend_percentages = (trend_counts / len(results_df)) * 100

print("\nTrend dağılımı:")
for trend, count in trend_counts.items():
    percentage = trend_percentages[trend]
    print(f"{trend}: {count} kez ({percentage:.2f}%)")

# Sonuçları CSV dosyasına kaydetme
results_csv_path = 'BTCson.csv'
results_df.to_csv(results_csv_path, index=False)

print(f"\nCSV dosyası oluşturuldu: {results_csv_path}")