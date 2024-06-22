import numpy as np
import random
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Parametreler
total_declines = 12
total_increases = 15
total_flats = 13
average_decline = -26.37 / 100  # Yüzdeyi oran olarak çevirmek
average_increase = 88.79 / 100  # Yüzdeyi oran olarak çevirmek
average_flat_change = -0.91 / 100  # Yüzdeyi oran olarak çevirmek

# Olasılıkları hesapla
total_events = total_declines + total_increases + total_flats
prob_decline = total_declines / total_events
prob_increase = total_increases / total_events
prob_flat = total_flats / total_events


# Simülasyon işlevi
def run_simulation():
    num_simulation_events = int(num_events_entry.get())
    initial_value = 100
    cash = initial_value
    invested = 0
    values = [initial_value]
    events = []

    for _ in range(num_simulation_events):
        # Yatırım yüzdeleri
        total_prob = prob_decline + prob_increase + prob_flat
        cash_weight = 1 - (prob_increase / total_prob)
        invested_weight = prob_increase / total_prob

        # Toplam değer üzerinden nakit ve yatırım hesaplamaları
        total_value = cash + invested
        cash = total_value * cash_weight
        invested = total_value * invested_weight

        event = random.choices(['decline', 'increase', 'flat'], weights=[prob_decline, prob_increase, prob_flat], k=1)[
            0]

        if event == 'decline':
            invested *= (1 + average_decline)
        elif event == 'increase':
            invested *= (1 + average_increase)
        elif event == 'flat':
            invested *= (1 + average_flat_change)

        total_value = cash + invested
        values.append(total_value)
        events.append(event)

    result_label.config(text=f"Başlangıç Değeri: {initial_value}\nSimülasyon Sonrası Değer: {total_value:.2f}")

    # Grafiği güncelle
    ax.clear()
    ax.plot(values, marker='o')
    for i, event in enumerate(events):
        ax.annotate(event, (i + 1, values[i + 1]), textcoords="offset points", xytext=(0, 10), ha='center')
    ax.set_title('Simülasyon Sonuçları')
    ax.set_xlabel('Olay Sayısı')
    ax.set_ylabel('Değer')
    canvas.draw()


# UI oluşturma
root = tk.Tk()
root.title("Simülasyon")
root.geometry("1024x768")

mainframe = ttk.Frame(root, padding="10 10 10 10")
mainframe.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))



ttk.Label(mainframe, text="Olay Sayısı:").grid(column=1, row=1, sticky=tk.W)
num_events_entry = ttk.Entry(mainframe, width=7)
num_events_entry.grid(column=2, row=1, sticky=(tk.W, tk.E))
num_events_entry.insert(0, "40")

ttk.Button(mainframe, text="Simülasyonu Çalıştır", command=run_simulation).grid(column=3, row=1, sticky=tk.W)

result_label = ttk.Label(mainframe, text="")
result_label.grid(column=1, row=2, columnspan=3, sticky=tk.W)

fig, ax = plt.subplots(figsize=(10, 6))
canvas = FigureCanvasTkAgg(fig, master=mainframe)
canvas.get_tk_widget().grid(column=1, row=3, columnspan=3)

for child in mainframe.winfo_children():
    child.grid_configure(padx=5, pady=5)

num_events_entry.focus()

root.mainloop()
