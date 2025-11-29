import csv
from datetime import date

currentYear = date.today().strftime('%Y')

class Santa:

    def __init__(self, rawSanta):
        self.invalidGiftees = []
        self.gifteeName = None
        self.gifteeWishList = ""

        self.id = rawSanta["id"]
        self.name = rawSanta["name"]
        self.email = rawSanta["email"]
        self.parent = rawSanta["parentName"]
        
        self.addInvalidGiftee(rawSanta["houseMemberID"])

        self.addGifteeWishList()

    def getID(self):
        return self.id

    def getName(self):
        return self.name
    
    def getEmail(self):
        return self.email
    
    def getGifteeName(self):
        return self.gifteeName
    
    def getParent(self):
        return self.parent

    def addInvalidGiftee(self, gifteeID):
        if gifteeID not in self.invalidGiftees:
            self.invalidGiftees.append(gifteeID)

    def printInvalidGiftees(self):
        print('santa ' + self.name)
        for i in self.invalidGiftees:
            print(i)
        print('\n')
        
    def getInvalidGiftees(self):
        return self.invalidGiftees

    def checkGiftee(self, tempGiftee):
        for i in self.invalidGiftees:
            if i == tempGiftee:
                return False
        return True
    
    def setGifteeName(self, gifteeName):
        self.gifteeName = gifteeName
        self.addGifteeWishList()

    def printAssignment(self):
        print(self.name, " is giving to ", self.giftee)

    def addGifteeWishList(self):
        with open('./santaConfigs/santaWishList.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['name'] == self.gifteeName and row['year'] == currentYear:
                    self.gifteeWishList = row['wishList']

    def getGifteeWishList(self):
        if self.gifteeWishList == "":
            return self.gifteeWishList
        wishListText = f"\nHere is what {self.gifteeName} wanted to tell you:\n{self.gifteeWishList}\n"
        return wishListText
        
