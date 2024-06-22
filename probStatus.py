import yfinance as yf
import pandas as pd

# Hisse senedi simgesi ve veri çekme tarih aralığı
ticker = "BTC-USD"
start_date = "2014-01-01"
end_date = "2024-06-21"

# Veri çekme
df = yf.download(ticker, start=start_date, end=end_date)

# Gereken sütunları seçme
df = df[['Close']]
df.reset_index(inplace=True)

# Tarihi, yıl ve çeyrek olarak ayırmak için:
df['Year'] = df['Date'].dt.year
df['Quarter'] = df['Date'].dt.to_period('Q')

# Her çeyrekteki kapanış fiyatının başlangıç ve bitiş değerlerini bulmak için:
quarterly_changes = df.groupby(['Year', 'Quarter'])['Close'].agg(['first', 'last'])

# Yüzde değişimini hesaplamak için:
quarterly_changes['Percent Change'] = ((quarterly_changes['last'] - quarterly_changes['first']) / quarterly_changes['first']) * 100

# Yatay hareketleri (%10'dan az değişim)
flat_movements = quarterly_changes[(quarterly_changes['Percent Change'] > -10) & (quarterly_changes['Percent Change'] < 10)]
total_flats = flat_movements.shape[0]
average_flat_change = flat_movements['Percent Change'].mean()

# Düşüş ve yükselişleri ayırmak (yatay hareketleri hariç tutarak)
declines = quarterly_changes[quarterly_changes['Percent Change'] <= -10]
increases = quarterly_changes[quarterly_changes['Percent Change'] >= 10]

# Ortalama düşüş ve yükselişi hesaplamak
average_decline = declines['Percent Change'].mean()
average_increase = increases['Percent Change'].mean()

# Toplam düşüş ve yükseliş sayısı
total_declines = declines.shape[0]
total_increases = increases.shape[0]

# Sonuçları yazdırmak
print(f"Toplam Düşüş Sayısı: {total_declines}")
print(f"Toplam Yükseliş Sayısı: {total_increases}")
print(f"Ortalama Düşüş: {average_decline:.2f}%")
print(f"Ortalama Yükseliş: {average_increase:.2f}%")
print(f"Toplam Yatay Hareket Sayısı: {total_flats}")
print(f"Ortalama Yatay Hareket: {average_flat_change:.2f}%")

# Yatay hareketlerin detayları
for index, row in flat_movements.iterrows():
    year, quarter = index
    percent_change = row['Percent Change']
    movement_type = "Yükseliş" if percent_change > 0 else "Düşüş"
    print(f"{year} Q{quarter}: {percent_change:.2f}% {movement_type}")

# Yüzde değişim detayları
flat_movements['Movement Type'] = flat_movements['Percent Change'].apply(lambda x: "Yükseliş" if x > 0 else "Düşüş")
print(flat_movements)
