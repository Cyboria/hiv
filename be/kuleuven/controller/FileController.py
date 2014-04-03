'''
Created on 30 Mar 2014

@author: EwoutVE
'''

from be.kuleuven.model import FileModel
from be.kuleuven.controller import SequenceController
import re
import operator
from Bio.SeqRecord import SeqRecord

class FileController:
    
    def __init__(self, sqlController):
        self.sqlController = sqlController
        self.sequenceController = SequenceController.SequenceController()
        self.fileModel = FileModel.FileModel()
        
    def getLocation(self):
        return self.fileModel.getLocation()
        
    def setLocation(self, location):
        self.fileModel.setLocation(location)
    
    def getFileName(self):
        return self.fileModel.getFileName()
    
    def setFileName(self, fileName):
        self.fileModel.setFileName(fileName)
        
    def filterSubtypeGFromFastaFileToFastaFile(self, multipleAlignmentFileLocation, multipleAlignmentFile, outputFileLocation, outputFile):
        subtypeG = self.sqlController.getSamplesSubtypeG()
        subTypeGids = list()
    
        for sample in subtypeG:
            subTypeGids.append(str(sample.patientId) + '_' + str(sample.sampleId) + '_' + str(sample.sampleDate))
        
        self.fileModel.setLocation(multipleAlignmentFileLocation)
        self.fileModel.setFileName(multipleAlignmentFile)
        align = self.fileModel.getAlignmentFileHandler()
        
        self.fileModel.setLocation(outputFileLocation)
        self.fileModel.setFileName(outputFile)
        
        subTypeG = list()
        
        for sequence in list(align):
            if(sequence.id in subTypeGids):
                subTypeG.append(sequence.upper())
            elif(re.search("Ref",sequence.id)):
                subTypeG.append(sequence.upper())
        
        self.fileModel.writeAlignmentToFile(subTypeG, "fasta")
        
    def removeGapsFromFastaFileToFastaFile(self, multipleAlignmentFileLocation, multipleAlignmentFile, outputFileLocation, outputFile):
        self.fileModel.setLocation(multipleAlignmentFileLocation)
        self.fileModel.setFileName(multipleAlignmentFile)
        align = self.fileModel.getAlignmentFileHandler()
        
        self.fileModel.setLocation(outputFileLocation)
        self.fileModel.setFileName(outputFile)
        
        goodAlignments = list()
        gapLocation = list()
        sequence_lengths = {}
        
        i = 0
        for char in align[0].seq:
            if char == '-':
                gapLocation.append(i)
            i = i + 1
        
        for sequence in list(align):
            if not (('IN' in sequence.id) or ('env' in sequence.id)):
                length = len(sequence.seq.ungap(gap='-'))
                if length > 1000:
                    if length in sequence_lengths:
                        sequence_lengths[length] = sequence_lengths[length] + 1
                    else:
                        sequence_lengths[length] = 1
        
        sorted_x = sorted(sequence_lengths.iteritems(), key=operator.itemgetter(1))
        
#        output.seek(0)
        
        for sequence in list(align):
            if not (('IN' in sequence.id) or ('env' in sequence.id)):
                length = len(sequence.seq.ungap(gap='-'))
                if length > 1000:
                    
                    mutable = sequence.seq.tomutable()
                    
                    for i in reversed(gapLocation):
                        mutable.__delitem__(i)
        
                    mutable = mutable[0:sorted_x[-1][0]]
        
                    goodAlignments.append(SeqRecord(mutable.toseq(), sequence.id, sequence.name, sequence.description).upper())
        
        self.fileModel.writeAlignmentToFile(goodAlignments, "fasta")
        
    def removeHighlyMutRegionsFromFastaFileToFastaFile(self, multipleAlignmentFileLocation, multipleAlignmentFile, outputFileLocation, outputFile):
        '''
        Rules to implement: 
        UC- : Serine (S)
        CU- : Leucine (L)
        CC- : Proline (P)
        CG- : Arginine (R)
        AC- : Threonine (T)
        GU- : Valine (V)
        GC- : Alanine (A)
        GG- : Glycine (G)
        '''
        
        goodAlignments = list()
        
        self.fileModel.setLocation(multipleAlignmentFileLocation)
        self.fileModel.setFileName(multipleAlignmentFile)
        align = self.fileModel.getAlignmentFileHandler()
        
        self.fileModel.setLocation(outputFileLocation)
        self.fileModel.setFileName(outputFile)
        
        for sequence in list(align):
            updatedSeq = self.sequenceController.removeNucleotidesHighlyMutableRegions(sequence.seq)
            goodAlignments.append(SeqRecord(updatedSeq, sequence.id, sequence.name, sequence.description).upper())

        self.fileModel.writeAlignmentToFile(goodAlignments, "fasta")