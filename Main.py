'''
Created on 27 Mar 2014

@author: EwoutVE
'''

from be.kuleuven.controller import SQLController
from be.kuleuven.controller import CSVController
from be.kuleuven.controller import FileController

class Main:

    def __init__(self):
        # Location of all the csv files
        location = "/Users/EwoutVE/Documents/eclipse/workspace/SQLAlchemy/DataFiles"
        locationSubtypedFiles = "/Users/EwoutVE/Documents/eclipse/workspace/SQLAlchemy/DataFilessubtyped/"
        multipleAlignmentFileLocation = "/Users/EwoutVE/Documents/eclipse/workspace/SQLAlchemy/DataFiles/"
        multipleAlignmentFileName = "mafft_result.fa"
        outputSubTypeGSelectionFileName = "subTypeG.fa"
        outputNoGapsFileName = "outputNoGaps.fa"
        outputNoHighlyMutRegFileName = "outputSubGRemovedHighMutRegion.fa"
        
        
        self.csvController = CSVController.CSVController(location)
        self.sqlController = SQLController.SQLController(self.csvController)
        self.fileController = FileController.FileController(self.sqlController)
        
        print "Controller instantiated"
        #self.sqlController.createTables()
        print "Tables created"
        #self.sqlController.insertPatients('patients.csv')
        print "Patients inserted. " + str(self.sqlController.patientSkippedCounter) + " patient entries were skipped."
#        self.sqlController.insertTherapies('therapies.csv')
        print "Therapies inserted. " + str(self.sqlController.therapySkippedCounter) + " therapies entries were skipped."
#        self.sqlController.insertTests('tests.csv')
        print "Tests inserted. " + str(self.sqlController.testSkippedCounter) + " tests entries were skipped."
#        self.sqlController.insertEvents('events.csv')
        print "Events inserted. " + str(self.sqlController.eventSkippedCounter) + " event entries were skipped."
#        self.sqlController.insertSamples(locationSubtypedFiles, True)
        print "Samples inserted. " + str(self.sqlController.sampleSkippedCounter) + " sample entries were skipped."
        
#        self.fileController.filterSubtypeGFromFastaFileToFastaFile(multipleAlignmentFileLocation, multipleAlignmentFileName, multipleAlignmentFileLocation, outputSubTypeGSelectionFileName)
        print "Sequences with subtype G have been selected from: " + multipleAlignmentFileLocation + multipleAlignmentFileName + " and are written to: " + multipleAlignmentFileLocation + outputSubTypeGSelectionFileName

        '''Remove the gaps '''
#        self.fileController.removeGapsFromFastaFileToFastaFile(multipleAlignmentFileLocation, outputSubTypeGSelectionFileName, multipleAlignmentFileLocation, outputNoGapsFileName)
        print "The gaps in the sequences have been removed."
        
        '''Remove the highly mutable regions'''
#        self.fileController.removeHighlyMutRegionsFromFastaFileToFastaFile(multipleAlignmentFileLocation, outputNoGapsFileName, multipleAlignmentFileLocation, outputNoHighlyMutRegFileName)
        print "The highly mutable regions in the sequences have been removed."
        
        patientsMultipleSamples = self.sqlController.getPatientsHavingMultipleSamplesSubtypeG()
        
        for sample in patientsMultipleSamples:
            #if sample[1] > 1:
            print sample
Main()