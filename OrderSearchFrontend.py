import tkinter as tk
from OrderSearchBackend import OrderSearchBackend
from tkinter import messagebox


class OrderSearchFrontend:
    def __init__(self):
        # Create root window and start GUI
        self.backend = OrderSearchBackend()
        self.master = tk.Tk()
        self.master.title("Search GUI")
        
        # Set size of window
        self.master.geometry("800x600")

        # Create search label and entry box
        self.searchLabel = tk.Label(self.master, text="Enter search text:")
        self.searchLabel.pack()
        self.searchEntry = tk.Entry(self.master, width=60)
        self.searchEntry.pack()


        # Bind KeyRelease event to search entry widget
        self.searchEntry.bind('<KeyRelease>', self.search)

        # Create results box and scrollbar
        self.resultsFrame = tk.Frame(self.master)
        self.resultsFrame.pack(fill=tk.BOTH, expand=True)
        self.resultsScrollbar = tk.Scrollbar(self.resultsFrame)
        self.resultsScrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.resultsListbox = tk.Listbox(self.resultsFrame, yscrollcommand=self.resultsScrollbar.set)
        self.resultsListbox.pack(fill=tk.BOTH, expand=True)
        self.resultsScrollbar.config(command=self.resultsListbox.yview)

        # Bind double-click event to results listbox
        self.resultsListbox.bind('<Double-Button-1>', self.openFrame)

        self.newFrame = ""

        # Start loop
        self.master.mainloop()




    
    def search(self, event=None):
        # Clear existing results
        self.resultsListbox.delete(0, tk.END)

        # Perform search
        searchText = self.searchEntry.get()
        results = self.performSearch(searchText, "ALL")

        # Display results
        for result in results:
            orderDetails = f"SUPPLIER: {result['supplier']} | LENK UPC: {result['lenkUpc']} | ITEMS: {result['description']} | ORDER NUMBER: {result['orderNumber']} | TRACKING NUMBER: {result['trackingNumber']}"
            self.resultsListbox.insert(tk.END, orderDetails)

    def performSearch(self, searchText, type):
        # Placeholder function to perform search
        # Returns a list of dictionaries representing each order
        if type == "ALL":
            #does a main search
            orders = self.backend.searchDatabase(searchText)

            #search tracking numbers
            potentialTrackingNumbers = self.backend.generatePotentialTrackingNumbers(searchText)
            for potentialTrackingNumber in potentialTrackingNumbers:
                results = self.backend.searchDatabase(potentialTrackingNumber)
                if results != []:
                    for result in results:
                        if result not in orders:
                            orders.append(result)
        elif type == "MATCH":
            orders = self.backend.getAllMatchingOrders(searchText)

        ordersFormatted = []
        for order in orders:
            orderDetails = {
                "key": order[0],
                "date": order[1],
                "supplier": order[2],
                "lenkUpc": order[3],
                "description": order[5],
                "orderNumber": order[6],
                "individualUnits": order[7],
                "trackingNumber": order[14],
                "quantityReceived": order[9] // order[7], #individualUnitsReceived / individualUnits
                "quantityOrdered": order[10] // order[7] #individualUnitsOrdered / individualUnits
            }
            #checks if the individual units remaining to receive is less then individual units ordered
            if order[9] < order[10]:
                ordersFormatted.append(orderDetails)
        return ordersFormatted

    def openFrame(self, event):
        #represents the index of the choice
        selection = self.resultsListbox.curselection()
        if len(selection) == 1:
            # grabs all the orders based on the search
            orders = self.performSearch(self.searchEntry.get(), "ALL")
            #grabs the order choice using the selected index
            selectedChoiceIndex = selection[0]
            selectedOrder = orders[selectedChoiceIndex]
            #grabs the order number from the selected order
            orderNumber = selectedOrder['orderNumber']
            #searches for all the matching orders
            matchingOrders = self.performSearch(orderNumber, "MATCH")

            # Create new frame and display order details

            self.newFrame = tk.Toplevel(self.master)


            # Add column headers
            headers = ["date", "supplier", "lenkUpc", "description", "orderNumber", "trackingNumber", "individualUnits", "quantityReceived", "quantityOrdered"]
            for col, header in enumerate(headers):
                label = tk.Label(self.newFrame, text=header, font=("Helvetica", 12, "bold"))
                label.grid(row=0, column=col, padx=10, pady=10)

            #holds the data of how much was received
            quantityReceivedEntries = {}
            # Add quantity received text box to each row
            for row, order in enumerate(matchingOrders):
                for col, field in enumerate(headers):
                    if col == 7:  # add text box in 7th column for quantity received
                        quantityReceivedEntry = tk.Entry(self.newFrame, width=10)
                        quantityReceivedEntry.insert(0, order[field])
                        quantityReceivedEntry.grid(row=row+1, column=col)
                        quantityReceivedEntries[order["key"]] = quantityReceivedEntry
                    else:
                        label = tk.Label(self.newFrame, text=order[field], font=("Helvetica", 10))
                        label.grid(row=row+1, column=col)

            # Add submit button
            submitButton = tk.Button(self.newFrame, text="Submit", font=("Helvetica", 12), bg="green", fg="white", command=lambda: self.saveEntries(quantityReceivedEntries))
            submitButton.grid(row=0, column=len(headers), padx=10, pady=10, sticky="e")
        
    def saveEntries(self, quantityReceivedEntries):
        for key, entry in quantityReceivedEntries.items():
            quantityReceived = entry.get()
            # Do something with the quantity_received, like save it to a file or database
            self.backend.updateOrderQuantity(key, quantityReceived)
        
        # Create a pop-up message box to confirm the update
        messagebox.showinfo("Quantity Updated", "The order quantity has been updated successfully!")
        # Close the current frame
        self.newFrame.destroy()

