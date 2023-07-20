import re
from EmailFetcher import EmailFetcher
import sqlite3


class OrderTrackerBackend:

    def insertTrackingData(self, orderNumber, trackingNumber):
        # Connect to the database or create it if it doesn't exist
        conn = sqlite3.connect('orders.db')
        # Define the SQL query to insert the data
        query = "UPDATE orders SET POTENTIAL_TRACKING_NUMBER = ? WHERE ORDER_NUMBER = ?"
        # Execute the query with the provided values
        conn.execute(query, (trackingNumber, orderNumber))
        # Commit the changes to the database
        conn.commit()
        # close database
        conn.close()

    # searches for the emails containing the order Number
    # param: orderNumber - the order number to be searched for

    def searchOrderNumber(self, emailFetcher, orderNumber):
        # call imap search function here
        email = emailFetcher.searchEmail(orderNumber)
        # return the email containing the order numbers
        return email

    # parses the email finding all the tracking numbers
    # param: emailText - refers to the raw email data that is going to be parsed

    def parseEmailForTrackingNumbers(self, email):
        # Define the regular expression to search for tracking numbers, looks for tracking numbers
        if ("FEDEX" in email):
            # print("FEDEX")
            trackingNumberRegex = re.compile(r'\b(?!https?:\/\/)[0-9]{12}\b')
        elif ("UPS" in email):
            # print("UPS")
            trackingNumberRegex = re.compile(
                r'(?<!\S)1Z[\dA-Z]{16}(?!\S)(?!(?:[^<]+>|[^>]+<\/a>))')
        elif ("USPS" in email):
            # print("USPS")
            trackingNumberRegex = re.compile(
                r'(?<!https?://)\b(?:[0-9]{12}|[0-9]{20}|[0-9]{22}|[0-9]{30}|[0-9]{34})\b')
        elif ("DHL" in email):
            # print("DHL")
            trackingNumberRegex = re.compile(r'\b(?!https?:\/\/)[0-9]{10}\b')

        # Find all matching tracking numbers in the email text
        trackingNumbers = trackingNumberRegex.findall(email)

        # return the list of tracking numbers found
        return trackingNumbers

    def findTrackingNumber(self, emailFetcher, orderNumber):
        # grabs the tracking numbers based on the orderNumber
        email = self.searchOrderNumber(emailFetcher, orderNumber)
        # set to hold all the tracking numbers
        trackingNumbers = set()
        # add the tracking numbers to the string
        trackingNumbers.update(self.parseEmailForTrackingNumbers(email))

        trackingNumbersString = ""
        # put into a string
        for trackingNumber in trackingNumbers:
            trackingNumbersString += trackingNumber + "\n"
        # returns the list of tracking numbers
        return trackingNumbersString

    def getOrderNumbers(self):
        # Connect to the database or create it if it doesn't exist
        conn = sqlite3.connect('orders.db')
        # get the distinct order numbers (no duplicates)
        # Define the query with the WHERE clause to ensure INDIVIDUAL_UNITS_RECEIVED is less than INDIVIDUAL_UNITS_ORDERED
        query = "SELECT DISTINCT ORDER_NUMBER FROM orders WHERE INDIVIDUAL_UNITS_RECEIVED < INDIVIDUAL_UNITS_ORDERED"
        orders = conn.execute(query).fetchall()
        # put into a set
        orderNumber = {orderNumber[0] for orderNumber in orders}
        # close database
        conn.close()
        # Return orders
        return orderNumber

    def missingTrackingNumber(self):
        # Connect to the database or create it if it doesn't exist
        conn = sqlite3.connect('orders.db')
        # execute the query to select order values with tracking number 'N/A', meaning its been checked
        result = conn.execute(
            "SELECT DISTINCT ORDER_NUMBER FROM orders WHERE POTENTIAL_TRACKING_NUMBER = 'N/A'")
        # fetch all the rows returned by the query
        rows = result.fetchall()
        # seperate the orderNumbers
        orderNumbers = [row[0] for row in rows]
        # close database
        conn.close()
        # returns the order numbers
        return orderNumbers

    def main(self):
        # Fetch orders missing inside of tracking table
        orderNumbers = self.getOrderNumbers()
        # Create an email searcher connection
        emailFetcher = EmailFetcher()
        # Loop through every missing order, extracting data
        for orderNumber in orderNumbers:
            # Find the tracking numbers corresponding to order
            try:
                potentialTrackingNumbers = self.findTrackingNumber(
                    emailFetcher, orderNumber)
            except:
                # if no tracking is found, tracking number gets set to being N/A
                potentialTrackingNumbers = "N/A"
            # Insert tracking numbers into table
            # print(potentialTrackingNumbers)
            self.insertTrackingData(orderNumber, potentialTrackingNumbers)
