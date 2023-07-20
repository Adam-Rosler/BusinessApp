import sqlite3
from ItemCatalogBackend import ItemCatalogBackend

class OrderAdderBackend:
    def __init__(self):
        #create a catalog connector
        self.catalogBackend = ItemCatalogBackend()
        

  
    def lookupItemFromCatalog(self, query):
        return self.catalogBackend.lookupItemFromCatalog(query)

    def idLookup(self, id):
        #returns the data corresponding to this ID
        return self.catalogBackend.getItem(id)


    def insertOrderData(self, date, supplier, lenkUPC, asin, product, orderNumber, individualUnits, individualUnitsPerBundle, individualUnitsReceived, 
                        individualUnitsOrdered, totalCost, totalProfit, listPrice, email, notes):
        # Connect to the database or create it if it doesn't exist
        conn = sqlite3.connect('orders.db')
        #adds the order to main data table and returns its key
        query = '''INSERT INTO orders (
                                    DATE, SUPPLIER, LENK_UPC, ASIN, PRODUCT, ORDER_NUMBER, INDIVIDUAL_UNITS, 
                                    INDIVIDUAL_UNITS_PER_BUNDLE, INDIVIDUAL_UNITS_RECEIVED, 
                                    INDIVIDUAL_UNITS_ORDERED, TOTAL_COST, TOTAL_PROFIT, 
                                    LIST_PRICE, EMAIL, NOTES) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''        
        # Execute the query with the provided values
        conn.execute(query, (date, supplier, lenkUPC, asin, product, orderNumber, individualUnits, individualUnitsPerBundle, 
                                    individualUnitsReceived, individualUnitsOrdered, totalCost, totalProfit,
                                    listPrice, email, notes))
        
        #commit the data
        conn.commit()
        
        #close database
        conn.close()
        
        
        
        
        
  
            
   
        
        
        
        