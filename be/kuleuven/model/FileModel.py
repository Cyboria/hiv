'''
Created on 30 Mar 2014

@author: EwoutVE
'''
from Bio import AlignIO
from Bio import SeqIO

class FileModel:
    
    def __init__(self):
        '''No init'''
        
    def getLocation(self):
        return self.location
        
    def setLocation(self, location):
        self.location = location
    
    def getFileName(self):
        return self.fileName    
    
    def setFileName(self, fileName):
        self.fileName = fileName
        
    def getAlignmentFileHandler(self):
        locationString = self.location + self.fileName
        return AlignIO.read(locationString, "fasta")
    
    def getFileHandler(self):
        locationString = self.location + self.fileName
        return open(locationString, "w")
    
    def writeAlignmentToFile(self, alignment, fileType):
        locationString = self.location + self.fileName
        SeqIO.write(alignment, locationString, fileType)