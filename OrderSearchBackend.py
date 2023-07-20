import sqlite3
from ItemCatalogBackend import ItemCatalogBackend

class OrderSearchBackend:
    def __init__(self):
        #create a catalog backend
        itemCatalogBackend = ItemCatalogBackend()
       

    def searchDatabase(self, query):
        # Connect to the database or create it if it doesn't exist
        conn = sqlite3.connect('orders.db')
        # Search the database for the query string in potential_tracking_number,
        # order_number, product, and supplier fields
        result = conn.execute('''SELECT * FROM orders WHERE 
                        POTENTIAL_TRACKING_NUMBER LIKE ? OR 
                        ORDER_NUMBER LIKE ? OR 
                        PRODUCT LIKE ? OR 
                        SUPPLIER LIKE ?''', 
                    ('%'+query+'%', '%'+query+'%', '%'+query+'%', '%'+query+'%'))
        #fetch all results
        results = result.fetchall()
        #close database
        conn.close()
        #grab order number from the table
        return results

    def getAllMatchingOrders(self, orderNumber):
        # Connect to the database or create it if it doesn't exist
        conn = sqlite3.connect('orders.db')
        #find where orders match
        query = "SELECT * FROM orders WHERE ORDER_NUMBER = ?"
        # Search the database for the query string using orderNumber
        result = conn.execute(query, (orderNumber,))
        #fetch all results
        results = result.fetchall()
        #close database
        conn.close()  
        #grab order number from the table
        return results


    def generatePotentialTrackingNumbers(self, search):
        #possible lengths of a tracking number
        possibleLengths = [8, 10, 12, 16, 20, 22, 30, 34]
        possibleTrackingNumbers = []

        for length in possibleLengths:
            if len(search) >= length:
                possibleTrackingNumbers.append(search[-length:])

        return possibleTrackingNumbers



    def lookupKey(self, key):
        # Connect to the database or create it if it doesn't exist
        conn = sqlite3.connect('orders.db')
        #find where orders match
        query = "SELECT * FROM orders WHERE KEY = ?"
        result = conn.execute(query, (key,))
        #fetch one result
        results = result.fetchone()
        #close database
        conn.close()
        return results

    def updateOrderQuantity(self, orderKey, quantity):
        #fetch order
        order = self.lookupKey(orderKey)
        lenkUPC = order[3]
        individualUnits = order[7]
        individualUnitsReceived = order[9]
        individualUnitsOrdered = order[10]
        totalCost = order[11]
        costPerIndividualUnit = totalCost / individualUnitsOrdered
        #calculates the total amount of units
        totalIndividualUnits = int(quantity) * individualUnits
        #calculates the difference in the previous amount of units to see how many have just been added
        totalIndividualUnitsAdded = totalIndividualUnits - individualUnitsReceived
        #updates the main order table
        self.updateOrderTable(orderKey, totalIndividualUnits)
        # #updates the current batch table
        self.insertIntoCurrentBatchTable(orderKey, lenkUPC, totalIndividualUnitsAdded, costPerIndividualUnit)
        

    def lookupKeyAndLenkUPC(self, key, lenkUPC):
        # Connect to the database or create it if it doesn't exist
        conn = sqlite3.connect('orders.db')
        query = '''SELECT INDIVIDUAL_UNITS_RECEIVED, COST_PER_INDIVIDUAL_UNIT 
               FROM currentBatch 
               WHERE ORDER_KEY = ? AND LENK_UPC = ?'''
        result = conn.execute(query, (key, lenkUPC))
        
        row = result.fetchone()
        #close database
        conn.close()
        return row

    def updateOrderTable(self, orderKey, totalUnits):
        # Connect to the database or create it if it doesn't exist
        conn = sqlite3.connect('orders.db')
        # Define the SQL query to update the data
        query = "UPDATE orders SET INDIVIDUAL_UNITS_RECEIVED = ? WHERE KEY = ?"
        # Execute the query with the provided values
        conn.execute(query, (totalUnits, orderKey))
        # Commit the changes to the database
        conn.commit()
        #close database
        conn.close()

    def insertIntoCurrentBatchTable(self, orderKey, lenkUPC, totalIndividualUnitsAdded, costPerIndividualUnit):
        # Connect to the database or create it if it doesn't exist
        conn = sqlite3.connect('orders.db')
        
        #checks for a matching row
        order = self.lookupKeyAndLenkUPC(orderKey, lenkUPC)
        
        if order != None:
            currentIndividualUnitsReceived = order[0]
            individualUnitsReceived = totalIndividualUnitsAdded + currentIndividualUnitsReceived 
            # If a matching row exists, update the values
            query = '''UPDATE currentBatch SET 
                    INDIVIDUAL_UNITS_RECEIVED = ?, 
                    COST_PER_INDIVIDUAL_UNIT = ?
                    WHERE ORDER_KEY = ? AND LENK_UPC = ?'''
            conn.execute(query, (individualUnitsReceived, costPerIndividualUnit, orderKey, lenkUPC))
        else:
            # If a matching row doesn't exist, insert a new row
            query = '''INSERT INTO currentBatch (
                        ORDER_KEY, LENK_UPC, INDIVIDUAL_UNITS_RECEIVED, COST_PER_INDIVIDUAL_UNIT)
                VALUES (?, ?, ?, ?)'''
            conn.execute(query, (orderKey, lenkUPC, totalIndividualUnitsAdded, costPerIndividualUnit))
        #commit changes
        conn.commit()
        #close database
        conn.close()


