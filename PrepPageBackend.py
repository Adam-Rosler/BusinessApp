import sqlite3
from OrderAdderBackend import OrderAdderBackend
import datetime
import csv
from CreateDatabases import CreateDatabases
from Order import Order
from ItemCatalogBackend import ItemCatalogBackend


class PrepPageBackend:

    def __init__(self):
        self.currentBatch = {}
        self.orders = self.getAllOrders()
        self.itemCatalogBackend = ItemCatalogBackend()
        self.createDatabasesBackend = CreateDatabases()

    #gets all the orders
    def getAllOrders(self):
        # Connect to the database or create it if it doesn't exist
        conn = sqlite3.connect('orders.db')
        result = conn.execute("SELECT * FROM currentBatch")
        rows = result.fetchall()
        #close the database
        conn.close()
        return rows


    def updateBatches(self, orderKey, lenkUPC, remainder, costPerIndividualUnit):
        # Connect to the database or create it if it doesn't exist
        conn = sqlite3.connect('orders.db')
        # retrieve the current value of INDIVIDUAL_UNITS_RECEIVED
        result = conn.execute('SELECT INDIVIDUAL_UNITS_RECEIVED FROM currentBatch WHERE ORDER_KEY=? AND LENK_UPC=?', (orderKey, lenkUPC))
        currentUnitsReceived = result.fetchone()[0]

        # calculate the new value of INDIVIDUAL_UNITS_RECEIVED
        newUnitsReceived = currentUnitsReceived - remainder
        if newUnitsReceived == 0:
             # Delete the entry in current batch
            conn.execute('DELETE FROM currentBatch WHERE ORDER_KEY=? AND LENK_UPC=?', (orderKey, lenkUPC))
        else:
            # update the table with the new value of INDIVIDUAL_UNITS_RECEIVED
            conn.execute('UPDATE currentBatch SET INDIVIDUAL_UNITS_RECEIVED=? WHERE ORDER_KEY=? AND LENK_UPC=?', (newUnitsReceived, orderKey, lenkUPC))

        # commit the changes to the database
        conn.commit()

        self.createDatabasesBackend.createTempDatabase()
        query = '''INSERT INTO temp (
                        ORDER_KEY, LENK_UPC, INDIVIDUAL_UNITS_RECEIVED, COST_PER_INDIVIDUAL_UNIT)
                VALUES (?, ?, ?, ?)'''
        conn.execute(query, (orderKey, lenkUPC, remainder, costPerIndividualUnit))
        
        
        # commit the changes to the database
        conn.commit()
        
        #close the database
        conn.close()



    def renameDatabases(self):
        # Connect to the database or create it if it doesn't exist
        conn = sqlite3.connect('orders.db')
        
        # get the current date and time
        now = datetime.datetime.now()

        # convert the date and time to a string in the format of yyyy-mm-dd_HH-MM-SS
        #rename current batch
        datetimeString = now.strftime('%Y_%m_%d_%H_%M_%S')
        conn.execute(f"ALTER TABLE currentBatch RENAME TO '{datetimeString}'")

        conn.commit()

        #rename temp batch to current batch
        try:
            conn.execute("ALTER TABLE temp RENAME TO currentBatch")
            conn.commit()
        except Exception as e:
            #temp table was never created since all items were used
            #creates a new currentBatch table
            self.createDatabasesBackend.createCurrenBatchDatabase()


    def createCurrentBatch(self):
        for order in self.orders:
            orderKey = order[0]
            lenkUPC = order[1]
            individualUnitsReceived = order[2]
            costPerIndividualUnit = order[3]

            #if item does not exist in hashmap, add it
            if lenkUPC not in self.currentBatch:
                lenkUPCInfo = self.itemCatalogBackend.getItem(lenkUPC)
                supplier = lenkUPCInfo[1]
                asin = lenkUPCInfo[2]
                description = lenkUPCInfo[3]
                individualUnitsPerBundle = lenkUPCInfo[5]
                listPrice = lenkUPCInfo[7]
                self.currentBatch[lenkUPC] = Order(supplier, asin, description, individualUnitsPerBundle, listPrice)
            
            #add to current batch
            self.currentBatch[lenkUPC].add(orderKey, individualUnitsReceived, costPerIndividualUnit)


        #do all the calculations, and put in a list
        for lenkUPC in self.currentBatch:
            #combines all the remainders
            self.currentBatch[lenkUPC].combineRemainders()
            #calculate averages
            self.currentBatch[lenkUPC].calculateAverages()
            
        #iterate through, and keep the products that create at least 1 unit
        # Create a new list with the items you want to keep
        newCurrentBatch = {}
        for lenkUPC in self.currentBatch:
            if self.currentBatch[lenkUPC].totalBundleUnits > 0:
                newCurrentBatch[lenkUPC] = self.currentBatch[lenkUPC]
                
        self.currentBatch = newCurrentBatch


            
    def submitBatches(self):
        for lenkUPC in self.currentBatch:
        #update information based on remainders
            for order in self.currentBatch[lenkUPC].notAdded:
                orderKey = order[0]
                remainder = order[1]
                costPerIndividualUnit = order[2]
                self.updateBatches(orderKey, lenkUPC, remainder, costPerIndividualUnit)
            
        #rename databases
        #setup new batch
        #setup old batch
        self.renameDatabases()


    def createCSVFile(self):
        #this will grab the product data and get it in a csv file to be ready to import to inventory labs
        csvFile = open('productCsv.csv', 'w', newline='')
        writer = csv.writer(csvFile)
        fieldNames = ['ASIN', 'BUYCOST', 'LISTPRICE', 'QUANTITY', 'Supplier']
        writer = csv.DictWriter(csvFile, fieldnames=fieldNames)
        writer.writeheader()

        for product in self.currentBatch:
            product = self.currentBatch[product]
            supplier = product.supplier
            asin = product.asin
            quantity = product.totalBundleUnits
            buyCost = product.costPerBundleUnit
            listPrice = product.listPrice
            writer.writerow({'ASIN': asin, 'BUYCOST': buyCost, 'LISTPRICE' : listPrice, 'QUANTITY' : quantity, 'Supplier' : supplier})