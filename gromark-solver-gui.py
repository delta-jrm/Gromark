import tkinter as tk
from tkinter import messagebox, scrolledtext
import string


def generate_running_key(primer, length):
    if not primer.isdigit():
        raise ValueError("Primer must be numeric.")
    primer = [int(d) for d in primer]
    if length <= len(primer):
        raise ValueError("Length must be greater than the primer length.")
    running_key = primer[:]
    a, b = 0, 1
    while len(running_key) < length:
        result = (running_key[a] + running_key[b]) % 10
        running_key.append(result)
        a += 1
        b += 1
    return running_key


def generate_mixed_alphabet(keyword):
    keyword = ''.join(sorted(set(keyword.upper()), key=keyword.index))
    base_alphabet = ''.join(sorted(set(string.ascii_uppercase) - set(keyword)))
    combined = keyword + base_alphabet

    num_cols = len(keyword)
    grid = [combined[i:i+num_cols] for i in range(0, len(combined), num_cols)]

    keyword_order = sorted([(char, idx) for idx, char in enumerate(keyword)])
    column_order = [idx for _, idx in keyword_order]

    mixed_alphabet = ''
    for idx in column_order:
        for row in grid:
            if idx < len(row):
                mixed_alphabet += row[idx]
    return mixed_alphabet


def encrypt(text, mixed_alphabet, running_key):
    standard = string.ascii_uppercase
    encrypted = ''
    for char, rk in zip(text.upper(), running_key):
        if char in standard:
            idx = (mixed_alphabet.index(char) + rk) % 26
            encrypted += mixed_alphabet[idx]
        else:
            encrypted += char
    return encrypted


def decrypt(text, mixed_alphabet, running_key):
    alphabet = list(string.ascii_uppercase)
    decrypted = ''
    for char, rk in zip(text.upper(), running_key):
        if char in mixed_alphabet:
            idx = (mixed_alphabet.index(char) - rk) % 26
            decrypted += alphabet[idx]
        else:
            decrypted += char
    return decrypted


def process(mode):
    text = input_text.get("1.0", tk.END).strip()
    primer = primer_entry.get().strip()
    keyword = keyword_entry.get().strip()

    if not text or not primer or not keyword:
        messagebox.showerror("Missing Input", "All fields must be filled.")
        return

    try:
        mixed_alpha = generate_mixed_alphabet(keyword)
        running_key = generate_running_key(primer, len(text))
        if mode == 'encrypt':
            result = encrypt(text, mixed_alpha, running_key)
        else:
            result = decrypt(text, mixed_alpha, running_key)
        output_text.config(state=tk.NORMAL)
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, result)
        output_text.config(state=tk.DISABLED)
    except Exception as e:
        messagebox.showerror("Error", str(e))

root = tk.Tk()
root.title("Delta_JRM's GROMARK Cipher Tool")

# Main Text Input
tk.Label(root, text="Input Text (Plaintext or Ciphertext):").pack(anchor="w", padx=10, pady=(10, 0))
input_text = scrolledtext.ScrolledText(root, height=6, wrap=tk.WORD)
input_text.pack(padx=10, fill="both", expand=True)

# Primer and Keyword Frame
entry_frame = tk.Frame(root)
entry_frame.pack(padx=10, pady=5, fill="x")

tk.Label(entry_frame, text="Primer:").grid(row=0, column=0, padx=5, sticky="e")
primer_entry = tk.Entry(entry_frame, width=10)
primer_entry.grid(row=0, column=1, padx=(0, 15))

tk.Label(entry_frame, text="Keyword:").grid(row=0, column=2, padx=5, sticky="e")
keyword_entry = tk.Entry(entry_frame, width=15)
keyword_entry.grid(row=0, column=3, padx=(0, 15))

# Encrypt/Decrypt Buttons
button_frame = tk.Frame(root)
button_frame.pack(pady=5)

encrypt_btn = tk.Button(button_frame, text="Encrypt", width=12, command=lambda: process("encrypt"))
encrypt_btn.grid(row=0, column=0, padx=10)

decrypt_btn = tk.Button(button_frame, text="Decrypt", width=12, command=lambda: process("decrypt"))
decrypt_btn.grid(row=0, column=1, padx=10)

# Output Text Box
tk.Label(root, text="Output Text:").pack(anchor="w", padx=10, pady=(10, 0))
output_text = scrolledtext.ScrolledText(root, height=6, wrap=tk.WORD, state=tk.DISABLED)
output_text.pack(padx=10, fill="both", expand=True, pady=(0, 10))

# Start the GUI
root.mainloop()
