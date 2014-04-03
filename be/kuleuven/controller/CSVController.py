'''
Created on 27 Mar 2014

@author: EwoutVE
'''
from be.kuleuven.model import CSVModel
import csv

class CSVController:

    def __init__(self, location):
        self.csvModel = CSVModel.CSVModel(location)
    
    def getLocation(self):
        return self.csvModel.getLocation()
        
    def setLocation(self, location):
        self.csvModel.setLocation(location)
    
    def getFileName(self):
        return self.csvModel.getFileName()
    
    def setFileName(self, fileName):
        self.csvModel.setFileName(fileName)
        
    def getReader(self, withHeader):
        data_initial = self.csvModel.getDataHandler()
        hasHeader = csv.Sniffer().has_header(data_initial.read(1024))
        data_initial.seek(0)
        dialect = csv.Sniffer().sniff(data_initial.read(1024))
        data_initial.seek(0)
        reader = csv.reader((line.replace('\0', '') for line in data_initial), dialect)
        
        if not withHeader:
            if hasHeader:
                next(reader, None) # skip the headers
        
        return reader