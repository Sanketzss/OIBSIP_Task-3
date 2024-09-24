import random
import string
import tkinter as tk
from tkinter import messagebox, ttk
from history_helper import add_to_history, get_password_history
from file_saver import save_password_to_file


def calculate_password_strength(password):
    length = len(password)
    if length < 8:
        return "Weak", 33

    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_number = any(c.isdigit() for c in password)
    has_symbol = any(c in string.punctuation for c in password)

    if has_upper and has_lower and has_number and has_symbol and length >= 12:
        return "Strong", 100
    elif has_upper and has_lower and (has_number or has_symbol):
        return "Medium", 66
    else:
        return "Weak", 33


def generate_password(length, use_letters, use_numbers, use_symbols, exclude_chars, letter_count, number_count,
                      symbol_count):
    char_pool = ''
    password = ''

    if use_letters:
        char_pool += string.ascii_letters
    if use_numbers:
        char_pool += string.digits
    if use_symbols:
        char_pool += string.punctuation

    if not char_pool:
        raise ValueError("No character types selected")

    if exclude_chars:
        char_pool = ''.join([c for c in char_pool if c not in exclude_chars])

    if letter_count:
        password += ''.join(random.choice(string.ascii_letters) for _ in range(letter_count))
    if number_count:
        password += ''.join(random.choice(string.digits) for _ in range(number_count))
    if symbol_count:
        password += ''.join(random.choice(string.punctuation) for _ in range(symbol_count))

    remaining_length = length - len(password)
    if remaining_length > 0:
        password += ''.join(random.choice(char_pool) for _ in range(remaining_length))

    password = ''.join(random.sample(password, len(password)))

    return password


def copy_to_clipboard(password):
    window.clipboard_clear()
    window.clipboard_append(password)
    messagebox.showinfo("Copied", "Password copied to clipboard!")


def save_password(password):
    save_password_to_file(password)
    messagebox.showinfo("Saved", "Password saved to file!")


def generate_and_show_password():
    try:
        length = int(length_entry.get())
        use_letters = letters_var.get()
        use_numbers = numbers_var.get()
        use_symbols = symbols_var.get()
        exclude_chars = exclude_chars_entry.get()
        letter_count = int(letter_count_entry.get()) if letter_count_entry.get() else 0
        number_count = int(number_count_entry.get()) if number_count_entry.get() else 0
        symbol_count = int(symbol_count_entry.get()) if symbol_count_entry.get() else 0

        if letter_count + number_count + symbol_count > length:
            raise ValueError("Sum of specific counts exceeds the password length")

        password = generate_password(length, use_letters, use_numbers, use_symbols, exclude_chars, letter_count,
                                     number_count, symbol_count)
        password_output.config(text=password)

        strength, progress_value = calculate_password_strength(password)
        strength_output.config(text=f"Strength: {strength}")
        strength_bar['value'] = progress_value

        # Save to history
        add_to_history(password)

        # Enable the copy and save buttons
        copy_button.config(state=tk.NORMAL)
        save_button.config(state=tk.NORMAL)
    except ValueError as e:
        messagebox.showerror("Error", str(e))


# Create the main window
window = tk.Tk()
window.title("Advanced Password Generator")

# Create and place widgets
tk.Label(window, text="Password Length:").grid(row=0, column=0)
length_entry = tk.Entry(window)
length_entry.grid(row=0, column=1)

letters_var = tk.BooleanVar(value=True)
numbers_var = tk.BooleanVar(value=True)
symbols_var = tk.BooleanVar(value=True)

tk.Checkbutton(window, text="Include Letters", variable=letters_var).grid(row=1, column=0)
tk.Checkbutton(window, text="Include Numbers", variable=numbers_var).grid(row=1, column=1)
tk.Checkbutton(window, text="Include Symbols", variable=symbols_var).grid(row=1, column=2)

tk.Label(window, text="Exclude Characters:").grid(row=2, column=0)
exclude_chars_entry = tk.Entry(window)
exclude_chars_entry.grid(row=2, column=1)

tk.Label(window, text="Exact Letter Count (optional):").grid(row=3, column=0)
letter_count_entry = tk.Entry(window)
letter_count_entry.grid(row=3, column=1)

tk.Label(window, text="Exact Number Count (optional):").grid(row=4, column=0)
number_count_entry = tk.Entry(window)
number_count_entry.grid(row=4, column=1)

tk.Label(window, text="Exact Symbol Count (optional):").grid(row=5, column=0)
symbol_count_entry = tk.Entry(window)
symbol_count_entry.grid(row=5, column=1)

generate_button = tk.Button(window, text="Generate", command=generate_and_show_password)
generate_button.grid(row=6, column=1)

password_output = tk.Label(window, text="")
password_output.grid(row=7, column=1)

strength_output = tk.Label(window, text="Strength:")
strength_output.grid(row=8, column=1)

strength_bar = ttk.Progressbar(window, length=200, mode='determinate')
strength_bar.grid(row=9, column=1)

copy_button = tk.Button(window, text="Copy to Clipboard", state=tk.DISABLED,
                        command=lambda: copy_to_clipboard(password_output.cget("text")))
copy_button.grid(row=10, column=0)

save_button = tk.Button(window, text="Save Password", state=tk.DISABLED,
                        command=lambda: save_password(password_output.cget("text")))
save_button.grid(row=10, column=1)

# Password history
history_button = tk.Button(window, text="Show History",
                           command=lambda: messagebox.showinfo("Password History", "\n".join(get_password_history())))
history_button.grid(row=10, column=2)

# Start the Tkinter event loop
window.mainloop()
