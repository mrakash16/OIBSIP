import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import random
import string

class PasswordGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Generator")

        # Password Length
        self.length_label = ttk.Label(root, text="Password Length:")
        self.length_entry = ttk.Entry(root, width=5)
        self.length_entry.insert(0, "8")  # Default length

        # Character Set Checkboxes
        self.use_letters_var = tk.BooleanVar(value=True)
        self.use_numbers_var = tk.BooleanVar(value=True)
        self.use_symbols_var = tk.BooleanVar(value=True)

        self.letters_checkbox = ttk.Checkbutton(root, text="Include Letters", variable=self.use_letters_var)
        self.numbers_checkbox = ttk.Checkbutton(root, text="Include Numbers", variable=self.use_numbers_var)
        self.symbols_checkbox = ttk.Checkbutton(root, text="Include Symbols", variable=self.use_symbols_var)

        # Password Display
        self.password_label = ttk.Label(root, text="Generated Password:")
        self.password_entry = ttk.Entry(root, state="readonly")

        # Generate Button
        self.generate_button = ttk.Button(root, text="Generate Password", command=self.generate_password)

        # Copy to Clipboard Button
        self.copy_button = ttk.Button(root, text="Copy to Clipboard", command=self.copy_to_clipboard)

        # Layout
        self.length_label.grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.length_entry.grid(row=0, column=1, padx=5, pady=5)
        self.letters_checkbox.grid(row=1, column=0, columnspan=2, sticky="w", padx=5, pady=2)
        self.numbers_checkbox.grid(row=2, column=0, columnspan=2, sticky="w", padx=5, pady=2)
        self.symbols_checkbox.grid(row=3, column=0, columnspan=2, sticky="w", padx=5, pady=2)
        self.generate_button.grid(row=4, column=0, columnspan=2, pady=10)
        self.password_label.grid(row=5, column=0, sticky="e", padx=5, pady=5)
        self.password_entry.grid(row=5, column=1, padx=5, pady=5)
        self.copy_button.grid(row=6, column=0, columnspan=2, pady=5)

    def generate_password(self):
        try:
            length = int(self.length_entry.get())
            use_letters = self.use_letters_var.get()
            use_numbers = self.use_numbers_var.get()
            use_symbols = self.use_symbols_var.get()

            characters = ""
            if use_letters:
                characters += string.ascii_letters
            if use_numbers:
                characters += string.digits
            if use_symbols:
                characters += string.punctuation

            if not characters:
                messagebox.showerror("Error", "No character set selected.")
                return

            password = ''.join(random.choice(characters) for _ in range(length))
            self.password_entry.config(state="normal")
            self.password_entry.delete(0, tk.END)
            self.password_entry.insert(0, password)
            self.password_entry.config(state="readonly")

        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number for password length.")

    def copy_to_clipboard(self):
        generated_password = self.password_entry.get()
        if generated_password:
            self.root.clipboard_clear()
            self.root.clipboard_append(generated_password)
            self.root.update()  
            messagebox.showinfo("Success", "Password copied to clipboard!")
        else:
            messagebox.showwarning("Warning", "No password generated yet.")

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGeneratorApp(root)
    root.mainloop()
