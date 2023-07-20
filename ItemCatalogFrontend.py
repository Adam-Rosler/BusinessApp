from ItemCatalogBackend import ItemCatalogBackend
import tkinter as tk
import tkinter.messagebox as messagebox


class ItemCatalogFrontend:
    def __init__(self):
        self.backend = ItemCatalogBackend()
        master = tk.Tk()
        master.title("Order Adder")

        self.supplierLabel = tk.Label(master, text="Enter Supplier:")
        self.supplierLabel.grid(row=0, column=0)

        self.supplierEntry = tk.Entry(master)
        self.supplierEntry.grid(row=0, column=1)

        self.asinLabel = tk.Label(master, text="Enter ASIN:")
        self.asinLabel.grid(row=1, column=0)

        self.asinEntry = tk.Entry(master)
        self.asinEntry.grid(row=1, column=1)

        self.productLabel = tk.Label(master, text="Enter Product:")
        self.productLabel.grid(row=2, column=0)

        self.productEntry = tk.Entry(master)
        self.productEntry.grid(row=2, column=1)

        self.individualUnitsLabel = tk.Label(master, text="Enter Individual Units:")
        self.individualUnitsLabel.grid(row=3, column=0)

        self.individualUnitEntry = tk.Entry(master)
        self.individualUnitEntry.grid(row=3, column=1)

        self.individualUnitsPerBundleLabel = tk.Label(master, text="Enter Individual Units Per Bundle:")
        self.individualUnitsPerBundleLabel.grid(row=4, column=0)

        self.individualUnitsPerBundleEntry = tk.Entry(master)
        self.individualUnitsPerBundleEntry.grid(row=4, column=1)

        self.feePercentLabel = tk.Label(master, text="Enter Fee as a percent:")
        self.feePercentLabel.grid(row=5, column=0)

        self.feePercentEntry = tk.Entry(master)
        self.feePercentEntry.grid(row=5, column=1)

        self.listPriceLabel = tk.Label(master, text="Enter List Price:")
        self.listPriceLabel.grid(row=6, column=0)

        self.listPriceEntry = tk.Entry(master)
        self.listPriceEntry.grid(row=6, column=1)

        self.submitButton = tk.Button(master, text="Submit", command=self.submit)
        self.submitButton.grid(row=8, column=1)
        master.mainloop()

    def submit(self):
        try:
            #grabs all the data from the entries
            supplier = self.supplierEntry.get()
            asin = self.asinEntry.get()
            product = self.productEntry.get()
            individualUnits = int(self.individualUnitEntry.get())
            individualUnitsPerBundle = int(self.individualUnitsPerBundleEntry.get())
            feePercent = float(self.feePercentEntry.get()) / 100
            listPrice = float(self.listPriceEntry.get())
            

            # call backend's addItem() method with the input values
            self.backend.addItem(supplier, asin, product, individualUnits, individualUnitsPerBundle, feePercent, listPrice)

            # display a success message to the user
            messagebox.showinfo("Success", "Item added successfully!")
        except Exception as e:
            #print error to message box if there is an error
            messagebox.showinfo("ERROR", e)

