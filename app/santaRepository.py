import csv
import random

from app.santa import Santa
import app.santaConfigs.config as config

class santaRepository:

    def __init__(self, exchange):
        self.exchange = exchange
        self.santasList = self.getSantas(exchange)
        self.santasIDList = []
        for s in self.santasList:
            self.santasIDList.append(s.getID())
        self.addHistory()

    def getSantabyID(self, santaID):
        for s in self.santasList:
            if s.getID() == santaID:
                return s
        
        return None
    
    def getSantabyName(self, name):
        for s in self.santasList:
            if s.getName() == name:
                return s
        
        return None

    def getSantaNamebyID(self, id):
        for s in self.santasList:
            if id == s.getID():
                return s.getName()

    def getNumSantas(self):
        return len(self.santasList)

    def getRandomSanta(self):
        return random.choice(self.santasList)

    def getSantaIDList(self):
        return self.santasIDList

    def addHistory(self):
        
        santaHistory = []
        
        with open('app/santaConfigs/santahistory.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                santaHistory.append(row)

        for h in santaHistory:
            for s in self.santasList:
                if h['santaID'] == s.getID():
                    s.addInvalidGiftee(h['gifteeID'])
                    break

        

    def getSantas(self, exchangeInput):

        exchange = config.exchanges[exchangeInput]
        
        rawSantas = []

        with open(exchange['fileName'], newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                rawSantas.append(Santa(row))
        
        return rawSantas
    
    def saveExchange(self, exchange, year):
        filename = f"./santaConfigs/{year}history-{self.exchange}.csv"
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["year", "santaID", "gifteeID"]) 
            for key, value in exchange.items():
                writer.writerow([year, key, value])
