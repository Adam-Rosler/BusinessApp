import sqlite3

class ItemCatalogBackend:
    
    def addItem(self, supplier, asin, product, individualUnits, individualUnitsPerBundle, fee, listPrice):
        # Connect to the database or create it if it doesn't exist
        conn = sqlite3.connect('orders.db')

        #adds item to the catalog
        query = """
            INSERT INTO catalog (SUPPLIER, ASIN, PRODUCT, INDIVIDUAL_UNITS, INDIVIDUAL_UNITS_PER_BUNDLE, FEE, LIST_PRICE)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        conn.execute(query, (supplier, asin, product, individualUnits, individualUnitsPerBundle, fee, listPrice))
        #commit changes
        conn.commit()
        #close the database
        conn.close()

    


    def lookupItemFromCatalog(self, query):
        # Connect to the database or create it if it doesn't exist
        conn = sqlite3.connect('orders.db')
        result = conn.execute('''SELECT * FROM catalog WHERE 
                        ASIN LIKE ? OR 
                        PRODUCT LIKE ?''', 
                    ('%'+query+'%', '%'+query+'%'))
        results = result.fetchall()
        #close the database
        conn.close()
        #grab order number from the table
        return results


    def getItem(self, lenkUPC):
        # Connect to the database or create it if it doesn't exist
        conn = sqlite3.connect('orders.db')
        # Define the SQL query to retrieve data for a specific item
        query = "SELECT * FROM catalog WHERE LENK_UPC = ?"
        # Execute the query with the provided ID value
        result = conn.execute(query, (lenkUPC,))
        # Fetch the first row of the result set
        item = result.fetchone()
        #close the database
        conn.close()
        return item
    
    


