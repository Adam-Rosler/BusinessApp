import tkinter as tk
import datetime
from tkinter import messagebox
from OrderAdderBackend import OrderAdderBackend
import traceback


class OrderAdderFrontend:

    def __init__(self):
        # set backend
        self.backend = OrderAdderBackend()

        # Create the main window
        self.root = tk.Tk()
        self.root.title("Order Form")
        # set background to black
        self.root.configure(bg="grey")
        # Set the default date to today's date
        self.today = datetime.date.today().strftime("%m/%d/%Y")

        # Create a search box
        searchLabel = tk.Label(
            self.root, text="Search for Item ID:", bg="LightSkyBlue1")
        searchLabel.grid(column=2, row=0, padx=5)

        searchVar = tk.StringVar()
        self.searchEntry = tk.Entry(
            self.root, textvariable=searchVar, width=50)
        self.searchEntry.grid(column=3, row=0, padx=5)

        # Bind KeyRelease event to search entry widget
        self.searchEntry.bind('<KeyRelease>', self.search)

        # Create a Listbox to display the search results
        self.searchResults = tk.Listbox(self.root, font=(
            "Arial", 10), width=150, bg="SlateGray", highlightcolor="black")
        self.searchResults.grid(row=1, column=0, columnspan=10, padx=5)

        # Bind the Listbox Select event to a handler function
        self.searchResults.bind('<<ListboxSelect>>', self.fillEntries)

        # Create a Label and Entry widget for the Date
        self.dateLabel = tk.Label(self.root, text="Date:", bg="LightSkyBlue1")
        self.dateLabel.grid(row=2, column=0, padx=5, pady=5)
        self.dateEntry = tk.Entry(self.root)
        self.dateEntry.grid(row=2, column=1, padx=5, pady=5)

        # Create a Label and Entry widget for the Supplier
        self.supplierLabel = tk.Label(
            self.root, text="Supplier:", bg="LightSkyBlue1")
        self.supplierLabel.grid(row=3, column=0, padx=5, pady=5)
        self.supplierEntry = tk.Entry(self.root)
        self.supplierEntry.grid(row=3, column=1, padx=5, pady=5)

        # Create a Label and Entry widget for the Order ID
        self.lenkUPCLabel = tk.Label(
            self.root, text="Item ID:",  bg="LightSkyBlue1")
        self.lenkUPCLabel.grid(row=4, column=0, padx=5, pady=5)
        self.lenkUPCEntry = tk.Entry(self.root)
        self.lenkUPCEntry.grid(row=4, column=1, padx=5, pady=5)

        # Create a Label and Entry widget for the Order Number
        self.orderNumberLabel = tk.Label(
            self.root, text="Order Number:", bg="LightSkyBlue1")
        self.orderNumberLabel.grid(row=6, column=0, padx=5, pady=5)
        self.orderNumberEntry = tk.Entry(self.root)
        self.orderNumberEntry.grid(row=6, column=1, padx=5, pady=5)

        # Create a Label and Entry widget for the Email
        self.emailLabel = tk.Label(
            self.root, text="Email:", bg="LightSkyBlue1")
        self.emailLabel.grid(row=7, column=0, padx=5, pady=5)
        self.emailEntry = tk.Entry(self.root)
        self.emailEntry.grid(row=7, column=1, padx=5, pady=5)

        # Create a Label and Entry widget for the Individual Units
        self.individualUnitsLabel = tk.Label(
            self.root, text="Individual Units:", bg="LightSkyBlue1")
        self.individualUnitsLabel.grid(row=8, column=0, padx=5, pady=5)
        self.individualUnitsEntry = tk.Entry(self.root)
        self.individualUnitsEntry.grid(row=8, column=1, padx=5, pady=5)

        # Create a Label and Entry widget for the Quantity Ordered
        self.quantityOrderedLabel = tk.Label(
            self.root, text="Quantity Ordered:", bg="LightSkyBlue1")
        self.quantityOrderedLabel.grid(row=9, column=0, padx=5, pady=5)
        self.quantityOrderedEntry = tk.Entry(self.root)
        self.quantityOrderedEntry.grid(row=9, column=1, padx=5, pady=5)

        # Create a Label and Entry widget for the Quantity Ordered
        self.totalCostLabel = tk.Label(
            self.root, text="Total Cost:", bg="LightSkyBlue1")
        self.totalCostLabel.grid(row=10, column=0, padx=5, pady=5)
        self.totalCostEntry = tk.Entry(self.root)
        self.totalCostEntry.grid(row=10, column=1, padx=5, pady=5)

        # Create a Label and Entry widget for the notes
        self.notesLabel = tk.Label(
            self.root, text="Notes:", bg="LightSkyBlue1")
        self.notesLabel.grid(row=11, column=0, padx=5, pady=5)
        self.notesEntry = tk.Entry(self.root)
        self.notesEntry.grid(row=11, column=1, padx=5, pady=5)

        self.submitButton = tk.Button(
            self.root, text="Submit", command=self.submitForm)
        self.submitButton.grid(row=12, column=1, padx=5, pady=5)
        self.root.mainloop()

    def search(self, key):
        # Clear the search results box
        self.searchResults.delete(0, tk.END)
        search = self.searchEntry.get()
        results = self.backend.lookupItemFromCatalog(search)
        # Add the results to the search results box
        for result in results:
            lenkUPC = str(result[0])
            asin = str(result[2])
            itemDescription = str(result[3])
            bundledUnits = str(result[5])
            listPrice = str(result[7])

            # result string
            result = "LENK UPC: " + lenkUPC + " | ASIN: " + asin + " | Description: " + \
                itemDescription + " | Bundled Units: " + \
                bundledUnits + " | List Price: " + listPrice

            self.searchResults.insert(tk.END, result)

    # Define a method to submit the form

    def submitForm(self):
        try:
            # Get the values from the Entry widgets
            date = self.dateEntry.get()
            supplier = self.supplierEntry.get()
            lenkUPC = self.lenkUPCEntry.get()
            orderNumber = self.orderNumberEntry.get()
            email = self.emailEntry.get()
            individualUnits = int(self.individualUnitsEntry.get())
            quantityOrdered = int(self.quantityOrderedEntry.get())
            totalCost = float(self.totalCostEntry.get())
            notes = self.notesEntry.get()

            # get info from catalog
            itemInfo = self.backend.idLookup(lenkUPC)
            asin = itemInfo[2]
            description = itemInfo[3]
            individualUnitsPerBundle = itemInfo[5]
            # calculates the total amount of orders possible with the indiviudalUnits and the required bundleUnits
            totalUnits = (individualUnits * quantityOrdered) / \
                individualUnitsPerBundle
            individualUnitsOrdered = individualUnits * quantityOrdered
            individualUnitsReceived = 0
            costPerUnit = totalCost / totalUnits
            # calculates profits
            fee = itemInfo[6]
            listPrice = itemInfo[7]
            potentialUnits = (
                individualUnits/individualUnitsPerBundle) * quantityOrdered
            totalProfit = ((listPrice * (1-fee)) -
                           costPerUnit) * potentialUnits
            roi = totalProfit / totalCost
            profitPerUnit = costPerUnit * roi

            # Print the values to the console (you could also save them to a file or database)
            # concatenate the information as a string
            message = f"Date: {date}\n" \
                f"Supplier: {supplier}\n" \
                f"lenk UPC: {lenkUPC}\n" \
                f"Order Number: {orderNumber}\n" \
                f"Email: {email}\n" \
                f"Individual Units: {individualUnits}\n" \
                f"Bundle Units: {individualUnitsPerBundle}\n" \
                f"Potential Units: {potentialUnits}\n" \
                f"Quantity Ordered: {quantityOrdered}\n" \
                f"Asin: {asin}\n" \
                f"Description: {description}\n" \
                f"Cost Per Unit: ${costPerUnit}\n" \
                f"List Price: ${listPrice}\n" \
                f"ROI: {round(roi,2)*100}%\n" \
                f"Total Profit: ${totalProfit}\n" \
                f"Profit Per Unit: ${profitPerUnit}\n" \
                f"Notes: {notes}"

            # ask the user to confirm the order information
            confirmed = messagebox.askokcancel(
                "Confirm Order Information", message)

            if confirmed == True:
                # call backend's insertOrderData() method with the input values
                self.backend.insertOrderData(date, supplier, lenkUPC, asin, description, orderNumber, individualUnits, individualUnitsPerBundle,
                                             individualUnitsReceived, individualUnitsOrdered, totalCost, totalProfit, listPrice, email, notes)

                # display a success message to the user
                messagebox.showinfo(
                    "Order Added!", "The order has been added!")

                # Clear the Entry widgets
                self.dateEntry.delete(0, tk.END)
                self.supplierEntry.delete(0, tk.END)
                self.lenkUPCEntry.delete(0, tk.END)
                self.orderNumberEntry.delete(0, tk.END)
                self.emailEntry.delete(0, tk.END)
                self.individualUnitsEntry.delete(0, tk.END)
                self.quantityOrderedEntry.delete(0, tk.END)
                self.totalCostEntry.delete(0, tk.END)
                self.notesEntry.delete(0, tk.END)
        except Exception as e:
            traceback.print_exc()
            messagebox.showinfo("ERROR", e)

    def fillEntries(self, event):
        # Get the selected item index
        selection = self.searchResults.curselection()
        if not selection:
            return
        index = selection[0]

        # put date into text entry
        self.dateEntry.delete(0, tk.END)
        self.dateEntry.insert(0, self.today)

        # insert id into textbox
        id = self.searchResults.get(index).split(' ')[2]
        self.lenkUPCEntry.delete(0, tk.END)
        self.lenkUPCEntry.insert(0, id)

        # Get the item data from the backend using the ID
        itemData = self.backend.idLookup(id)

        # insert supplier into textbox
        supplier = itemData[1]
        self.supplierEntry.delete(0, tk.END)
        self.supplierEntry.insert(0, supplier)

        # insert email into textbox
        self.emailEntry.delete(0, tk.END)
        self.emailEntry.insert(0, "email@gmail.com")

        # insert individual units
        individualUnits = itemData[4]
        self.individualUnitsEntry.delete(0, tk.END)
        self.individualUnitsEntry.insert(0, individualUnits)



