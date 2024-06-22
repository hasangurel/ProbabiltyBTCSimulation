import random


def generate_events(start_event, transition_probabilities, num_events):
    events = [start_event]
    current_event = start_event

    for _ in range(num_events - 1):
        possible_next_events = [event.split('_')[1] for event in transition_probabilities.keys() if
                                event.startswith(current_event)]
        probabilities = [transition_probabilities[f"{current_event}_{next_event}"] for next_event in
                         possible_next_events]
        next_event = random.choices(possible_next_events, weights=probabilities)[0]
        events.append(next_event)
        current_event = next_event

    return events


def simulate_portfolio(events, initial_value):
    portfolio_value = initial_value
    asset_price = 100  # Başlangıç fiyatı
    asset_count = 0
    quarters = []

    for i, event in enumerate(events):
        if event == 'Yükseliş':
            asset_price *= 1.8879  # %88.79 artış
        elif event == 'Düşüş':
            asset_price *= 0.7363  # %26.37 düşüş

        # Portföy dağılımını ayarla
        if event == 'Düşüş':
            asset_allocation = 0.4  # Düşüş sonrası %40 mal
        elif event == 'Yükseliş':
            asset_allocation = 0.6  # Yükseliş sonrası %60 mal
        else:  # Yatay
            asset_allocation = 0.5  # Yatay durumda %50 mal

        # Portföyü yeniden dengele
        total_asset_value = asset_count * asset_price
        cash = portfolio_value - total_asset_value
        target_asset_value = portfolio_value * asset_allocation

        if total_asset_value < target_asset_value:
            # Mal al
            amount_to_buy = (target_asset_value - total_asset_value) / asset_price
            asset_count += amount_to_buy
            cash -= amount_to_buy * asset_price
        elif total_asset_value > target_asset_value:
            # Mal sat
            amount_to_sell = (total_asset_value - target_asset_value) / asset_price
            asset_count -= amount_to_sell
            cash += amount_to_sell * asset_price

        portfolio_value = (asset_count * asset_price) + cash

        if (i + 1) % 4 == 0:  # Her 4 olayda bir (çeyrek sonu)
            quarters.append({
                'Quarter': (i + 1) // 4,
                'Portfolio Value': portfolio_value,
                'Asset Price': asset_price,
                'Asset Count': asset_count
            })

    return quarters


transition_probabilities = {
    'Düşüş_Düşüş': 0.26666666666666666,
    'Düşüş_Yükseliş': 0.4,
    'Düşüş_Yatay': 0.3333333333333333,
    'Yatay_Düşüş': 0.38461538461538464,
    'Yatay_Yükseliş': 0.38461538461538464,
    'Yatay_Yatay': 0.23076923076923078,
    'Yükseliş_Düşüş': 0.29411764705882354,
    'Yükseliş_Yükseliş': 0.35294117647058826,
    'Yükseliş_Yatay': 0.35294117647058826
}

# 100 çeyrek (25 yıl) için simülasyon yap
events = generate_events('Yatay', transition_probabilities, 400)
initial_value = 10000
quarters = simulate_portfolio(events, initial_value)

# Sonuçları yazdır
for q in quarters:
    print(f"Çeyrek {q['Quarter']}: Portföy Değeri: ${q['Portfolio Value']:.2f}, "
          f"Mal Fiyatı: ${q['Asset Price']:.2f}, Mal Sayısı: {q['Asset Count']:.2f}")

# Son durum
final_quarter = quarters[-1]
print(f"\nSon durum (25 yıl sonra):")
print(f"Portföy Değeri: ${final_quarter['Portfolio Value']:.2f}")
print(f"Başlangıç Değeri: ${initial_value:.2f}")
print(f"Toplam Getiri: %{(final_quarter['Portfolio Value'] / initial_value - 1) * 100:.2f}")