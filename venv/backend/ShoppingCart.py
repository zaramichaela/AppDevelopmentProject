class ShoppingCart:

    def _init_(self, productName, ID, price, quantity):
        self.__productName = productName
        self.__ID = ID
        self.__price = price
        self.__quantity = quantity

    def set_productName(self, productName):
        self.__productName = productName
    def set_ID(self, ID):
        self.__ID = ID
    def set_price(self, price):
        self.__price = price
    def set_quantity(self, quantity):
        self.__quantity = quantity

    def get_productName(self):
        return self.__productName
    def get_ID(self):
        return self.__ID
    def get_price(self):
        return self.__price
    def get_quantity(self):
        return self.__quantity

    def computeTotalProduct(self):
            return (self._price * self._quantity)

#Item1 = ShoppingCart("Medicine1", "D11", 4.00, 1)
#Item2 = ShoppingCart("Medicine2", "D12", 2.00, 3)
#Item3 = ShoppingCart("Medicine3", "D13", 1.00, 2)

#userList = [Item1, Item2, Item3]


#for u in userList:
    #print(u.get_productName(), u.get_ID(), u.get_price(), u.get_quantity())
    #print(u.computeTotalProduct())
