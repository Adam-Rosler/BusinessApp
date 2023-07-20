import tkinter as tk
from OrderTrackerBackend import OrderTrackerBackend
from tkinter import messagebox

class OrderTrackerFrontend():
    def __init__(self):
        self.backend = OrderTrackerBackend()
        self.orderNumbers = self.backend.missingTrackingNumber()
        #check if it is empty
        if len(self.orderNumbers) < 1:
            messagebox.showinfo("ERROR", "All tracking numbers are accounted for!")
            return
        self.trackings = {}
        
        self.root = tk.Tk()
        self.root.title("Tracking Numbers")

        # create frame
        frame = tk.Frame(self.root)
        frame.pack()
        # create labels and entry boxes for each item
        for i, item in enumerate(self.orderNumbers):
            tk.Label(frame, text=item).grid(row=i, column=0)
            trackingEntry = tk.Entry(frame)
            trackingEntry.insert(0, "N/A")
            trackingEntry.grid(row=i, column=1)
            self.trackings[item] = trackingEntry

        # create submit button
        submitButton = tk.Button(frame, text="Submit", command=self.submit)
        submitButton.grid(row=len(self.orderNumbers), column=0, columnspan=2)
        
        self.root.mainloop()
        
    def submit(self):
        # retrieve tracking numbers and print them
        for orderNumber, entry in self.trackings.items():
            trackingNumber = entry.get()
            self.backend.insertTrackingData(orderNumber, trackingNumber)
        messagebox.showinfo("Tracking Updated", "tracking has been updated")
        # close the GUI window
        self.root.destroy()

