import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from datetime import datetime
import os
import json

class BMIApp:
    def __init__(self, master):
        self.master = master
        self.master.title("BMI Calculator")
        self.master.geometry("600x500")

        # Variables
        self.weight_var = tk.DoubleVar()
        self.height_var = tk.DoubleVar()
        self.weight_unit_var = tk.StringVar()
        self.weight_unit_var.set("kg")

        # GUI components
        self.title_label = tk.Label(master, text="BMI Calculator", font=("Helvetica", 16, "bold"))
        self.title_label.grid(row=0, column=0, columnspan=3, pady=10)

        self.weight_label = tk.Label(master, text="Enter weight:", font=("Helvetica", 12))
        self.weight_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")

        self.weight_entry = tk.Entry(master, textvariable=self.weight_var, font=("Helvetica", 12))
        self.weight_entry.grid(row=1, column=1, padx=5, pady=5)

        self.weight_unit_menu = tk.OptionMenu(master, self.weight_unit_var, "kg", "lbs", command=self.update_weight_entry)
        self.weight_unit_menu.config(font=("Helvetica", 10))
        self.weight_unit_menu.grid(row=1, column=2, padx=5, pady=5, sticky="w")

        self.height_label = tk.Label(master, text="Enter height (m):", font=("Helvetica", 12))
        self.height_label.grid(row=2, column=0, padx=5, pady=5, sticky="e")

        self.height_entry = tk.Entry(master, textvariable=self.height_var, font=("Helvetica", 12))
        self.height_entry.grid(row=2, column=1, padx=5, pady=5)

        self.calculate_button = tk.Button(master, text="Calculate BMI", command=self.calculate_bmi_and_save, font=("Helvetica", 12, "bold"))
        self.calculate_button.grid(row=3, column=0, columnspan=3, pady=20)

        self.result_label = tk.Label(master, text="", font=("Helvetica", 14, "bold"))
        self.result_label.grid(row=4, column=0, columnspan=3)

        self.save_button = tk.Button(master, text="Save Data", command=self.calculate_bmi_and_save, font=("Helvetica", 12, "bold"))
        self.save_button.grid(row=5, column=0, columnspan=3, pady=10)

        self.clear_button = tk.Button(master, text="Clear History", command=self.clear_bmi_history, font=("Helvetica", 12, "bold"))
        self.clear_button.grid(row=6, column=0, columnspan=3, pady=10)

        self.load_button = tk.Button(master, text="Load Data", command=self.load_data, font=("Helvetica", 12, "bold"))
        self.load_button.grid(row=7, column=0, columnspan=3, pady=10)

        self.plot_button = tk.Button(master, text="Plot BMI History", command=self.plot_bmi_history, font=("Helvetica", 12, "bold"))
        self.plot_button.grid(row=8, column=0, columnspan=3, pady=10)

        # Data storage
        self.data_file = "bmi_data.json"
        self.bmi_data = []

        # Load data on startup
        self.load_data()

    def update_weight_entry(self, event=None):
        # Convert weight to kg for internal calculations
        weight = self.weight_var.get()
        unit = self.weight_unit_var.get()

        if unit == "lbs":
            weight_kg = weight * 0.453592
            self.weight_var.set(weight_kg)

    def calculate_bmi_and_save(self):
        try:
            weight = float(self.weight_var.get())
            height = float(self.height_var.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter numeric values.")
            return

        if weight <= 0 or height <= 0:
            messagebox.showerror("Error", "Weight and height must be positive values.")
            return

        bmi = weight / (height ** 2)
        category = self.classify_bmi(bmi)

        result_text = f"BMI: {bmi:.2f}\nCategory: {category}"
        self.result_label.config(text=result_text)

        # Save data to history
        self.save_data_to_history(bmi)

    def classify_bmi(self, bmi):
        if bmi < 18.5:
            return "Underweight"
        elif 18.5 <= bmi < 25:
            return "Normal weight"
        elif 25 <= bmi < 30:
            return "Overweight"
        else:
            return "Obese"

    def save_data_to_history(self, bmi):
        try:
            data_entry = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "weight": self.weight_var.get(),
                "weight_unit": self.weight_unit_var.get(),
                "height": self.height_var.get(),
                "bmi": bmi
            }

            self.bmi_data.append(data_entry)

            with open(self.data_file, "w") as file:
                json.dump(self.bmi_data, file)

            messagebox.showinfo("Data Saved", "BMI data saved successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Error saving data: {str(e)}")

    def clear_bmi_history(self):
        result = messagebox.askyesno("Clear History", "Are you sure you want to clear BMI history?")
        if result:
            self.bmi_data = []
            with open(self.data_file, "w") as file:
                json.dump(self.bmi_data, file)
            messagebox.showinfo("History Cleared", "BMI history has been cleared.")

    def load_data(self):
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, "r") as file:
                    self.bmi_data = json.load(file)
        except Exception as e:
            messagebox.showerror("Error", f"Error loading data: {str(e)}")

    def plot_bmi_history(self):
        if not self.bmi_data:
            messagebox.showinfo("No Data", "No BMI data available for plotting.")
            return

        timestamps = [entry["timestamp"] for entry in self.bmi_data]
        bmi_values = [entry["bmi"] for entry in self.bmi_data]

        plt.figure(figsize=(10, 5))
        plt.plot(timestamps, bmi_values, marker='o', linestyle='-', color='b')
        plt.title('BMI History')
        plt.xlabel('Timestamp')
        plt.ylabel('BMI')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    root = tk.Tk()
    app = BMIApp(root)
    root.mainloop()
