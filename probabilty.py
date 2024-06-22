import tkinter as tk
from tkinter import messagebox

# Geçiş ihtimalleri sözlüğü
transition_probabilities = {
    'Düşüş_Düşüş': 0.3333333333333333,
    'Düşüş_Yükseliş': 0.3333333333333333,
    'Düşüş_Yatay': 0.3333333333333333,
    'Yatay_Düşüş': 0.2222222222222222,
    'Yatay_Yükseliş': 0.5555555555555556,
    'Yatay_Yatay': 0.2222222222222222,
    'Yükseliş_Düşüş': 0.23076923076923078,
    'Yükseliş_Yükseliş': 0.38461538461538464,
    'Yükseliş_Yatay': 0.38461538461538464
}

# Kullanıcı seçimi için geçiş listesi
transitions = []


# Uygulamayı oluşturma
def add_transition(transition):
    if len(transitions) < 3:
        transitions.append(transition)
        update_transition_label()
    else:
        messagebox.showwarning("Uyarı", "Sadece üç geçiş seçebilirsiniz.")


def remove_transition():
    if transitions:
        transitions.pop()
        update_transition_label()
    else:
        messagebox.showwarning("Uyarı", "Geçiş listesi zaten boş.")


def update_transition_label():
    transition_label.config(text="Geçişler: " + "_".join(transitions))


def calculate_probabilities():
    if len(transitions) != 3:
        messagebox.showerror("Hata", "Lütfen üç geçiş seçin.")
        return

    prob_list = []
    cumulative_prob = 1.0

    for i in range(2):
        transition_pair = transitions[i] + '_' + transitions[i + 1]
        if transition_pair in transition_probabilities:
            prob = transition_probabilities[transition_pair]
            prob_list.append((transition_pair, prob))
            cumulative_prob *= prob
        else:
            messagebox.showerror("Hata", "Geçersiz geçiş dizisi.")
            return

    last_transition = transitions[-1]
    next_probabilities = {k: v for k, v in transition_probabilities.items() if k.startswith(last_transition)}

    if not next_probabilities:
        messagebox.showerror("Hata", "Geçersiz geçiş dizisi.")
        return

    result_text = f"Geçişler: {'_'.join(transitions)}\n\n"
    result_text += "Adım Adım Geçiş İhtimalleri:\n"
    for pair, prob in prob_list:
        result_text += f"{pair}: % {prob * 100:.2f}\n"
    result_text += f"\nSon geçişten sonra olasılıklar:\n"

    for k, v in next_probabilities.items():
        combined_prob = cumulative_prob * v
        result_text += f"{k}: % {combined_prob * 100:.2f}\n"

    messagebox.showinfo("Sonuç", result_text)


# Tkinter penceresini oluşturma
root = tk.Tk()
root.title("Geçiş İhtimalleri Hesaplama")

# Geçiş butonları
buttons_frame = tk.Frame(root)
buttons_frame.pack(pady=10)

transitions_list = ['Düşüş', 'Yatay', 'Yükseliş']
for transition in transitions_list:
    button = tk.Button(buttons_frame, text=transition, command=lambda t=transition: add_transition(t))
    button.pack(side=tk.LEFT, padx=5)

# Geçişleri gösteren etiket
transition_label = tk.Label(root, text="Geçişler: ")
transition_label.pack(pady=10)

# Ekle ve çıkar butonları
actions_frame = tk.Frame(root)
actions_frame.pack(pady=10)

remove_button = tk.Button(actions_frame, text="Son Geçişi Çıkar", command=remove_transition)
remove_button.pack(side=tk.LEFT, padx=5)

# Hesapla butonu
calculate_button = tk.Button(root, text="Hesapla", command=calculate_probabilities)
calculate_button.pack(pady=20)

# Uygulamayı başlatma
root.mainloop()
