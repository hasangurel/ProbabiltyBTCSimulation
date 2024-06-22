import pandas as pd

# CSV dosyasını yükle
file_path = 'btc_quarterly_trends_classified.csv'  # Dosya yolunu burada güncelleyin
data = pd.read_csv(file_path)

# Geçiş sayılarını hesaplamak için bir sözlük oluştur
transitions = {
    'Düşüş_Düşüş': 0, 'Düşüş_Yükseliş': 0, 'Düşüş_Yatay': 0,
    'Yatay_Düşüş': 0, 'Yatay_Yükseliş': 0, 'Yatay_Yatay': 0,
    'Yükseliş_Düşüş': 0, 'Yükseliş_Yükseliş': 0, 'Yükseliş_Yatay': 0
}

# Geçişleri say
for i in range(len(data) - 1):
    current_state = data.iloc[i, 0]
    next_state = data.iloc[i + 1, 0]
    transition_key = f'{current_state}_{next_state}'
    if transition_key in transitions:
        transitions[transition_key] += 1

# Toplam sayıları hesapla
total_counts = {
    'Düşüş': transitions['Düşüş_Düşüş'] + transitions['Düşüş_Yükseliş'] + transitions['Düşüş_Yatay'],
    'Yatay': transitions['Yatay_Düşüş'] + transitions['Yatay_Yükseliş'] + transitions['Yatay_Yatay'],
    'Yükseliş': transitions['Yükseliş_Düşüş'] + transitions['Yükseliş_Yükseliş'] + transitions['Yükseliş_Yatay']
}

# İhtimalleri hesapla
probabilities = {k: (v / total_counts[k.split('_')[0]]) if total_counts[k.split('_')[0]] > 0 else 0 for k, v in transitions.items()}

# Sonuçları yazdır
print("Geçiş Sayıları:", transitions)
print("İhtimaller:", probabilities)
