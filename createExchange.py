from datetime import date

from santa import Santa
from emailUtils import sendEmails
from santaRepository import santaRepository

class exchange:
        
    def __init__(self, exchangeInput):
        self.exchangeType = exchangeInput
        self.historicalSantas = santaRepository(self.exchangeType)
        self.numSantas = self.historicalSantas.getNumSantas()
        self.exchangeSantas = []
        self.firstSantaID = None
        self.year = date.today().strftime('%Y')

    
    def exploreSantas(self, exchangeDict, santaID):
        # print(f'entered function with santaid: {santaID}\nexchange: {exchangeDict}\n\n')
        # doing everything with ids
        eligibleSantas = self.historicalSantas.getSantaIDList().copy()
        
        # remove previous santas in exchange
        for s in list(exchangeDict):
            if s in eligibleSantas:
                eligibleSantas.remove(s)
        
        # get and remove ineligible giftees
        currentSanta = self.historicalSantas.getSantabyID(santaID)
        for s in currentSanta.getInvalidGiftees():
            if s in eligibleSantas:
                eligibleSantas.remove(s)

        # test if all santas already in list
        if (len(exchangeDict) == self.numSantas):
            # print('in base case!')
            exchangeDict[santaID] = self.firstSantaID
            return exchangeDict

        # print(f'eligibleSantas: {eligibleSantas}\n\n')
        for g in eligibleSantas:
            # print(f'{eligibleSantas}')
            exchangeDict[g] = None
            exchangeDict = self.exploreSantas(exchangeDict, g)
            if exchangeDict[g] is None:
                # print(f'failed excursion: {eligibleSantas}')
                del exchangeDict[g]
                continue
            else:
                # print('success excursion')
                exchangeDict[santaID] = g
                return exchangeDict
        # print(f'about to return a failed {santaID}')
        return exchangeDict
            

    def addGifteestoSantas(self, santaIDList):
        for s in santaIDList:
            santa = self.historicalSantas.getSantabyID(s)
            gifteeSantaName = self.historicalSantas.getSantaNamebyID(
                santaIDList[s]
            )
            santa.setGifteeName(gifteeSantaName)
            self.exchangeSantas.append(santa)

    def runExchange(self):
        
        firstSanta = self.historicalSantas.getRandomSanta()
        self.firstSantaID = firstSanta.getID()
        exchangeDict = {firstSanta.getID(): None}
        exchangeDict = self.exploreSantas(exchangeDict, self.firstSantaID)
        
        self.addGifteestoSantas(exchangeDict)
        self.historicalSantas.saveExchange(exchangeDict, self.year)

        sendEmails(self.exchangeSantas, self.exchangeType)



    


        # print(f'santaDict: {exchangeDict}')


        # if self.exchangeType == 'test':
        #     self.santas.printGiftees()
        # else:
        #     sendEmails(santas, config.exchanges[exchangeInput])


# psuedocode for recursion:

#         set firstsanta - use first in list
#         call exploratorySanta(firstsanta, ?)

#         returns santaidlist with or without santaid. if it has santaid, then it's successful, if it doesn't, then try another santaid
#         def exploreSanta(currentechange, santaid)
#             create list of eligiblegiftees for santa - consider previousSantas
            
#             check santaidlist for base case
#                 return this is why i need the dictionary
            

#             loop list of test santas
#                 add value for test santa to dict? 
#                 current echange? = exploreSanta(eligible, current exchange)
#                 if current exchange contains testsanta
#                       set value for santaid = test santa
#                       add test santa
#                       return current exchange
#                 else 
#                       remove test santa from dict?
#                                  
# 
#                 
            
#             return currentechange

