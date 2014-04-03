'''
Created on 27 Mar 2014

@author: EwoutVE
'''

class CSVModel:
    
    def __init__(self, location):
        self.location = location
        
    def getLocation(self):
        return self.location
        
    def setLocation(self, location):
        self.location = location
    
    def getFileName(self):
        return self.fileName    
    
    def setFileName(self, fileName):
        self.fileName = fileName
        
    def getDataHandler(self):
        locationString = self.location + self.fileName
        return open(locationString, 'rU')