import tkinter as tk
from PrepPageFrontend import PrepPageFrontend
from ItemCatalogFrontend import ItemCatalogFrontend
from OrderSearchFrontend import OrderSearchFrontend
from OrderAdderFrontend import OrderAdderFrontend
from OrderTrackerFrontend import OrderTrackerFrontend
from tkinter import messagebox
from CreateDatabases import CreateDatabases


class NavigatorGUI:

    def __init__(self):

        # Create a main window
        root = tk.Tk()
        root.title("BusinessApp 2.1")
        # set the size of the window to 800 x 600 pixels
        root.geometry("400x400")

        # create databases
        CreateDatabases().createDatabases()

        # Create buttons for navigating to different GUIs
        self.prepButton = tk.Button(
            root, text="Prep Page (EMPLOYEE)", command=self.openPrepPage)
        self.orderButton = tk.Button(
            root, text="Order Search (EMPLOYEE)", command=self.openOrderSearch)
        self.catalogButton = tk.Button(
            root, text="Item Catalog (ADMIN)", command=self.openItemCatalog)
        self.orderAdderButton = tk.Button(
            root, text="Order Adder (ADMIN)", command=self.openOrderAdder)
        self.orderTrackerButton = tk.Button(
            root, text="Order Tracker (ADMIN)", command=self.openOrderTracker)

        # Create a label for displaying text
        self.statusLabel = tk.Label(
            root, text="Employees: Please only use programs that say \"EMPLOYEE\"")
        # Pack the buttons neatly in the main window
        self.statusLabel.pack(pady=10)
        self.prepButton.pack(pady=10)
        self.orderButton.pack(pady=10)
        self.catalogButton.pack(pady=10)
        self.orderAdderButton.pack(pady=10)
        self.orderTrackerButton.pack(pady=10)

        # Start the GUI
        root.mainloop()

    def openOrderTracker(self):
        try:
            OrderTrackerFrontend()
        except Exception as e:
            messagebox.showinfo("Error", e)

    # Define functions for opening different GUIs

    def openPrepPage(self):
        try:
            prepPage = PrepPageFrontend()
        except Exception as e:
            messagebox.showinfo("Error", e)

    def openOrderSearch(self):
        try:
            # Create a callback function to enable the buttons
            orderSearch = OrderSearchFrontend()
        except Exception as e:
            messagebox.showinfo("Error", e)

    def openItemCatalog(self):
        try:
            itemcatalog = ItemCatalogFrontend()
        except Exception as e:
            messagebox.showinfo("Error", e)

    def openOrderAdder(self):
        try:
            orderAdder = OrderAdderFrontend()
        except Exception as e:
            messagebox.showinfo("Error", e)


NavigatorGUI()
