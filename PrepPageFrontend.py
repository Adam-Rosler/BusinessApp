import tkinter as tk
from PrepPageBackend import PrepPageBackend
from tkinter import messagebox

class PrepPageFrontend:
    def __init__(self):
        # setup backend
        self.backend = PrepPageBackend()
        # create the current batch
        self.backend.createCurrentBatch()
        self.items = self.backend.currentBatch
        self.keys = list(self.items.keys())
        # check if items is empty and display a message box if it is
        if not self.items:
            messagebox.showinfo("Error", "There are no orders to prep!")
            return
        self.currentFrameIndex = 0
        self.isLastItem = False

        # create main window
        self.root = tk.Tk()
        self.root.title("Prep Page Frontend")

        # create frame to hold item details
        self.frame = tk.Frame(self.root)
        self.frame.pack()

        # create label to display item details
        self.label = tk.Label(self.frame, text="")
        self.label.pack()

        # create next button to go to the next item
        self.nextButton = tk.Button(self.frame, text="Next", command=self.showNextItem)
        self.nextButton.pack(side=tk.RIGHT)

        # create submit button to show all items
        self.submitButton = tk.Button(self.frame, text="Submit", command=self.showAllItems)
        self.submitButton.pack(side=tk.BOTTOM)
        self.submitButton.pack_forget()  # hide submit button initially

        # create close button to close the window
        self.closeButton = tk.Button(self.frame, text="Close", command=self.root.destroy)
        self.closeButton.pack(side=tk.BOTTOM)
        self.closeButton.pack_forget()  # hide close button initially

        # show the first item
        self.showCurrentItem()

        # run the program
        self.root.mainloop()

    def showCurrentItem(self):
        # display the details of the current item
        lenkUPC = self.keys[self.currentFrameIndex]
        item = self.items[lenkUPC]
        # grab the info from the backend on the current batch
        remainder = item.remainder
        description = item.description
        totalBundleUnits = item.totalBundleUnits
        individualUnitsPerBundle = item.individualUnitsPerBundle
        remainder  = item.remainder

        # create the packing steps message
        packingSteps = f"(INDIVIDUAL UNITS REFERS TO HOW MANY ITEMS A PACKAGE MAY HAVE, 1 PACKAGE OF SOAP MAY HAVE 10 INDIVIDUAL UNITS)\n\nPackage in individual units of {individualUnitsPerBundle}, you must also remove {remainder} individual units, this should create a quantity of {totalBundleUnits}"
        self.label.config(text="ID: {}\n\nDescription: {}\n\nPackingSteps: {}".format(lenkUPC, description, packingSteps))

        # check if this is the last item
        if self.currentFrameIndex == len(self.items) - 1:
            self.isLastItem = True
            self.nextButton.pack_forget()  # hide next button on last item
            self.submitButton.pack()  # show submit button on last item


    def showNextItem(self):
        # show the next item
        if self.currentFrameIndex < len(self.items) - 1:
            self.currentFrameIndex += 1
            self.showCurrentItem()

    def showAllItems(self):
        #create the next batch
        self.backend.submitBatches()

        #creates a csv file
        self.backend.createCSVFile()

        # display all items
        allItems = ""
        for lenkUPC, order in self.items.items():
            allItems += "ID: {}\nASIN: {} \nName: {} \nQuantity: {}\n\n".format(lenkUPC, order.asin, order.description, order.totalBundleUnits)
        self.label.config(text=allItems)

        # hide next button and show close button
        self.nextButton.pack_forget()
        self.submitButton.pack_forget()
        self.closeButton.pack()

        # update isLastItem flag to true
        self.isLastItem = True


