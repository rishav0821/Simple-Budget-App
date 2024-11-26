import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

class BudgetAppGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Budget App")
        self.data = pd.DataFrame(columns=["Type", "Category", "Amount"])

        # Create GUI Layout
        self.create_widgets()
    
    def create_widgets(self):
        # Title
        title_label = tk.Label(self.root, text="Budget Tracker", font=("Arial", 16))
        title_label.pack(pady=10)

        # Transaction Frame
        transaction_frame = tk.Frame(self.root)
        transaction_frame.pack(pady=10)

        tk.Label(transaction_frame, text="Type:").grid(row=0, column=0, padx=5, pady=5)
        self.type_var = tk.StringVar(value="Income")
        ttk.Combobox(transaction_frame, textvariable=self.type_var, values=["Income", "Expense"], state="readonly").grid(row=0, column=1, padx=5, pady=5)

        tk.Label(transaction_frame, text="Category:").grid(row=1, column=0, padx=5, pady=5)
        self.category_entry = tk.Entry(transaction_frame)
        self.category_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(transaction_frame, text="Amount:").grid(row=2, column=0, padx=5, pady=5)
        self.amount_entry = tk.Entry(transaction_frame)
        self.amount_entry.grid(row=2, column=1, padx=5, pady=5)

        add_button = tk.Button(transaction_frame, text="Add Transaction", command=self.add_transaction)
        add_button.grid(row=3, column=0, columnspan=2, pady=10)

        # Summary Frame
        summary_frame = tk.Frame(self.root)
        summary_frame.pack(pady=10)

        tk.Button(summary_frame, text="View Summary", command=self.view_summary).grid(row=0, column=0, padx=10, pady=5)
        tk.Button(summary_frame, text="Save to CSV", command=self.save_to_csv).grid(row=0, column=1, padx=10, pady=5)
        tk.Button(summary_frame, text="Load from CSV", command=self.load_from_csv).grid(row=0, column=2, padx=10, pady=5)

        # Transactions Display
        self.tree = ttk.Treeview(self.root, columns=("Type", "Category", "Amount"), show="headings", height=10)
        self.tree.heading("Type", text="Type")
        self.tree.heading("Category", text="Category")
        self.tree.heading("Amount", text="Amount")
        self.tree.pack(pady=10)
    
    def add_transaction(self):
        transaction_type = self.type_var.get()
        category = self.category_entry.get()
        try:
            amount = float(self.amount_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Amount must be a number.")
            return

        if not category:
            messagebox.showerror("Error", "Category cannot be empty.")
            return

        new_entry = {"Type": transaction_type, "Category": category, "Amount": amount}
        self.data = pd.concat([self.data, pd.DataFrame([new_entry])], ignore_index=True)

        self.tree.insert("", "end", values=(transaction_type, category, amount))
        messagebox.showinfo("Success", "Transaction added successfully.")

        # Clear input fields
        self.category_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)
    
    def view_summary(self):
        income = self.data[self.data["Type"] == "Income"]["Amount"].sum()
        expenses = self.data[self.data["Type"] == "Expense"]["Amount"].sum()
        balance = income - expenses

        summary_message = f"Total Income: ${income}\nTotal Expenses: ${expenses}\nBalance: ${balance}"
        messagebox.showinfo("Summary", summary_message)
    
    def save_to_csv(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if file_path:
            self.data.to_csv(file_path, index=False)
            messagebox.showinfo("Success", f"Data saved to {file_path}")
    
    def load_from_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            self.data = pd.read_csv(file_path)
            # Refresh the treeview
            for item in self.tree.get_children():
                self.tree.delete(item)
            for _, row in self.data.iterrows():
                self.tree.insert("", "end", values=(row["Type"], row["Category"], row["Amount"]))
            messagebox.showinfo("Success", f"Data loaded from {file_path}")

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = BudgetAppGUI(root)
    root.mainloop()
