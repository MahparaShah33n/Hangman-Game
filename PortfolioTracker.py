import tkinter as tk
from tkinter import messagebox, filedialog
import csv

# Hardcoded stock prices
stock_prices = {
    "AAPL": 180,
    "TSLA": 250,
    "GOOG": 2800,
    "AMZN": 3400,
    "NFLX": 450
}

portfolio = []

def add_stock():
    symbol = entry_symbol.get().upper()
    try:
        quantity = int(entry_quantity.get())
    except ValueError:
        messagebox.showerror("Error", "Enter a valid number for quantity.")
        return

    if symbol not in stock_prices:
        messagebox.showerror("Error", f"{symbol} not in stock price list.")
        return

    price = stock_prices[symbol]
    investment = price * quantity
    portfolio.append((symbol, quantity, price, investment))

    listbox.insert(tk.END, f"{symbol}: {quantity} x ${price} = ${investment}")
    entry_symbol.delete(0, tk.END)
    entry_quantity.delete(0, tk.END)
    update_total()

def update_total():
    total = sum(item[3] for item in portfolio)
    label_total.config(text=f"Total Investment: ${total}")

def save_file():
    if not portfolio:
        messagebox.showwarning("Warning", "Portfolio is empty.")
        return

    file_type = var_filetype.get()
    file_ext = 'csv' if file_type == 'CSV' else 'txt'
    file_path = filedialog.asksaveasfilename(defaultextension=f".{file_ext}",
                                             filetypes=[(f"{file_type} files", f"*.{file_ext}")])
    if not file_path:
        return

    try:
        with open(file_path, 'w', newline='') as file:
            if file_ext == 'csv':
                writer = csv.writer(file)
                writer.writerow(["Stock", "Quantity", "Price", "Investment"])
                for row in portfolio:
                    writer.writerow(row)
                writer.writerow(["", "", "Total", sum(i[3] for i in portfolio)])
            else:
                for row in portfolio:
                    file.write(f"{row[0]}: {row[1]} x ${row[2]} = ${row[3]}\n")
                file.write(f"\nTotal Investment: ${sum(i[3] for i in portfolio)}")
        messagebox.showinfo("Saved", f"File saved to:\n{file_path}")
    except Exception as e:
        messagebox.showerror("Error", str(e))


# GUI Setup
root = tk.Tk()
root.title("📈 Stock Portfolio Tracker")
root.geometry("500x550")
root.config(bg="white")

title = tk.Label(root, text="📊 Stock Portfolio Tracker", font=("Arial", 20, "bold"), fg="green", bg="white")
title.pack(pady=10)

frame_input = tk.Frame(root, bg="white")
frame_input.pack(pady=10)

tk.Label(frame_input, text="Stock Symbol:", font=("Arial", 12), bg="white").grid(row=0, column=0, padx=5, pady=5)
entry_symbol = tk.Entry(frame_input, font=("Arial", 12), width=10)
entry_symbol.grid(row=0, column=1)

tk.Label(frame_input, text="Quantity:", font=("Arial", 12), bg="white").grid(row=0, column=2, padx=5, pady=5)
entry_quantity = tk.Entry(frame_input, font=("Arial", 12), width=5)
entry_quantity.grid(row=0, column=3)

btn_add = tk.Button(root, text="Add Stock", command=add_stock, font=("Arial", 12), bg="#28a745", fg="white")
btn_add.pack(pady=10)

listbox = tk.Listbox(root, font=("Courier", 12), width=50, height=10)
listbox.pack(pady=10)

label_total = tk.Label(root, text="Total Investment: $0", font=("Arial", 14, "bold"), fg="blue", bg="white")
label_total.pack(pady=10)

frame_save = tk.Frame(root, bg="white")
frame_save.pack(pady=10)

var_filetype = tk.StringVar(value="CSV")
tk.Radiobutton(frame_save, text="CSV", variable=var_filetype, value="CSV", bg="white", font=("Arial", 10)).pack(side=tk.LEFT, padx=10)
tk.Radiobutton(frame_save, text="TXT", variable=var_filetype, value="TXT", bg="white", font=("Arial", 10)).pack(side=tk.LEFT)

btn_save = tk.Button(root, text="💾 Save to File", command=save_file, font=("Arial", 12), bg="#007bff", fg="white")
btn_save.pack(pady=15)

root.mainloop()
