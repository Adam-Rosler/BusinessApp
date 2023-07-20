import tkinter as tk

def calculate():
    unit_price = float(price_entry.get())
    total_units = int(units_entry.get())
    discount = float(discount_entry.get())
    tax = float(tax_entry.get())

    # Calculate total cost before discount and tax
    total_cost = unit_price * total_units

    # Calculate discount
    discount_amount = total_cost * (discount / 100)
    total_cost -= discount_amount

    # Calculate tax
    tax_amount = total_cost * (tax / 100)
    total_cost += tax_amount

    # Update result labels
    total_cost_label.config(text="Total Cost: $" + str(round(total_cost, 2)))
    price_per_unit_label.config(text="Price per Unit: $" + str(round(total_cost / total_units, 2)))

# Create GUI window
window = tk.Tk()
window.title("Cost Calculator")

# Create input fields and labels
price_label = tk.Label(window, text="Unit Price: $")
price_label.grid(column=0, row=0)
price_entry = tk.Entry(window)
price_entry.grid(column=1, row=0)

units_label = tk.Label(window, text="Total Units:")
units_label.grid(column=0, row=1)
units_entry = tk.Entry(window)
units_entry.grid(column=1, row=1)

discount_label = tk.Label(window, text="Discount (%):")
discount_label.grid(column=0, row=2)
discount_entry = tk.Entry(window)
discount_entry.grid(column=1, row=2)

tax_label = tk.Label(window, text="Tax (%):")
tax_label.grid(column=0, row=3)
tax_entry = tk.Entry(window)
tax_entry.grid(column=1, row=3)

# Create calculate button
calculate_button = tk.Button(window, text="Calculate", command=calculate)
calculate_button.grid(column=1, row=4)

# Create result labels
total_cost_label = tk.Label(window, text="Total Cost: $0.00")
total_cost_label.grid(column=0, row=5)

price_per_unit_label = tk.Label(window, text="Price per Unit: $0.00")
price_per_unit_label.grid(column=1, row=5)

# Run GUI window
window.mainloop()
