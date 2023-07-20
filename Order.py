class Order:
    def __init__(self, supplier, asin, description, individualUnitsPerBundle, listPrice):
        self.notAdded = []
        self.supplier = supplier
        self.asin = asin
        self.description = description
        self.individualUnitsPerBundle = individualUnitsPerBundle
        self.listPrice = listPrice
        self.totalIndividualUnits = 0
        self.totalBundleUnits = 0
        self.totalCost = 0
        self.costPerBundleUnit = 0
        self.remainder = 0

    def add(self, orderKey, individualUnitsReceived, costPerIndividualUnit):
        # calculate how many units can be bundled
        remainder = individualUnitsReceived % self.individualUnitsPerBundle
        totalIndividualUnitsBundable = (individualUnitsReceived - remainder)
        self.totalIndividualUnits += totalIndividualUnitsBundable

        # calculate the total cost
        totalCost = costPerIndividualUnit * totalIndividualUnitsBundable
        self.totalCost += totalCost

        # this would be if there exists a remainder
        # update the individual units left to represent the remainder
        if remainder > 0:
            self.notAdded.append([orderKey, remainder, costPerIndividualUnit])

    def combineRemainders(self):
        # keep track of the indexs checked
        currentUnitsAdded = 0
        totalCost = 0
        for index, order in enumerate(self.notAdded):
            individualUnitsReceived = order[1]
            pricePerIndividualUnit = order[2]
            currentUnitsAdded += individualUnitsReceived

            if currentUnitsAdded >= self.individualUnitsPerBundle:
                remainder = currentUnitsAdded % self.individualUnitsPerBundle
                totalIndividualUnits = currentUnitsAdded - remainder
                individualUnitsReceived -= remainder
                totalCost += individualUnits * pricePerIndividualUnit
                # add the quantity and total costs to main adder
                self.totalIndividualUnits += totalIndividualUnits
                self.totalCost += totalCost
                # reset counters
                currentUnitsAdded = 0
                totalCost = 0

                # update remainder
                order[1] = remainder

                # update list
                # checks whether or not to include current element
                if remainder == 0:
                    self.notAdded = self.notAdded[index+1:]
                else:
                    self.notAdded = self.notAdded[index:]

            # grab number of units still available
            individualUnits = order[1]
            # calculate cost of these units
            cost = pricePerIndividualUnit * individualUnits
            totalCost += cost

        # anything remaining is a remainder
        self.remainder = currentUnitsAdded

    def calculateAverages(self):
        # ensure it is at least 1 unit
        if self.totalIndividualUnits > 0:
            # calculate price per individual unit
            self.costPerUnit = self.totalCost / self.totalIndividualUnits
            # calculate price per bundle
            self.costPerBundleUnit = self.costPerUnit * self.individualUnitsPerBundle
            # add total amount of bundle units made
            self.totalBundleUnits += (self.totalIndividualUnits /
                                      self.individualUnitsPerBundle)
