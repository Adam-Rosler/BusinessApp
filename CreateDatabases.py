import sqlite3


class CreateDatabases:



    def createDatabases(self):
        #creates main DBS for program
        self.createCatalogDatabase()
        self.createOrderDatabase()
        self.createCurrenBatchDatabase()
        
        
    def createCatalogDatabase(self):
        # Connect to the database
        conn = sqlite3.connect('orders.db')
        
        # Create catalog table
        conn.execute('''CREATE TABLE IF NOT EXISTS catalog
                    (LENK_UPC INTEGER PRIMARY KEY,
                    SUPPLIER TEXT,
                    ASIN TEXT,
                    PRODUCT TEXT,
                    INDIVIDUAL_UNITS INTEGER,
                    INDIVIDUAL_UNITS_PER_BUNDLE INTEGER,
                    FEE DECIMAL,
                    LIST_PRICE DECIMAL
                    );''')
        #commit changes
        conn.commit()
        #close connection
        conn.close()




    def createOrderDatabase(self):
        # Connect to the database
        conn = sqlite3.connect('orders.db')
        
        # Create orders table
        conn.execute('''CREATE TABLE IF NOT EXISTS orders
                    (
                    KEY INTEGER PRIMARY KEY,
                    DATE TEXT, 
                    SUPPLIER TEXT,
                    LENK_UPC INTEGER,
                    ASIN TEXT,
                    PRODUCT TEXT,
                    ORDER_NUMBER TEXT,
                    INDIVIDUAL_UNITS INTEGER,
                    INDIVIDUAL_UNITS_PER_BUNDLE INTEGER,
                    INDIVIDUAL_UNITS_RECEIVED INTEGER,
                    INDIVIDUAL_UNITS_ORDERED INTEGER,
                    TOTAL_COST DECIMAL,
                    TOTAL_PROFIT DECIMAL,
                    LIST_PRICE DECIMAL,
                    POTENTIAL_TRACKING_NUMBER TEXT,
                    EMAIL TEXT,
                    NOTES TEXT
                    );''')
        #commit changes
        conn.commit()
        #close connection
        conn.close()




    def createCurrenBatchDatabase(self):
        # Connect to the database
        conn = sqlite3.connect('orders.db')
        
        # Create current batch table
        conn.execute('''CREATE TABLE IF NOT EXISTS currentBatch
                    (
                    ORDER_KEY INTEGER,
                    LENK_UPC INTEGER,
                    INDIVIDUAL_UNITS_RECEIVED INTEGER,
                    COST_PER_INDIVIDUAL_UNIT DECIMAL
                    );''')
        #commit changes
        conn.commit()
        #close connection
        conn.close()
 


    def createTempDatabase(self):
        # Connect to the database
        conn = sqlite3.connect('orders.db')
        
        # Create current batch table
        conn.execute('''CREATE TABLE IF NOT EXISTS temp
                    (
                    ORDER_KEY INTEGER,
                    LENK_UPC INTEGER,
                    INDIVIDUAL_UNITS_RECEIVED INTEGER,
                    COST_PER_INDIVIDUAL_UNIT DECIMAL
                    );''')
        #commit changes
        conn.commit()
        #close connection
        conn.close()
        
    
        
        
