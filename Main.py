'''
Created on 27 Mar 2014

@author: EwoutVE
'''

from be.kuleuven.controller import SQLController
from be.kuleuven.controller import CSVController
from be.kuleuven.controller import FileController
from be.kuleuven.controller import TreeController
from be.kuleuven.controller import ClusterController
from be.kuleuven.controller import SequenceController

from ete2 import Tree

class Main:

    def __init__(self):
        # Location of all the csv files
        
        #This is used for debugging
        
        local = True
       
        location = "/Users/EwoutVE/Documents/eclipse/workspace/SQLAlchemy/DataFiles/"
        locationSubtypedFiles = "/Users/EwoutVE/Documents/eclipse/workspace/SQLAlchemy/DataFiles/subtyped/"
        multipleAlignmentFileLocation = "/Users/EwoutVE/Documents/eclipse/workspace/SQLAlchemy/DataFiles/"
        multipleAlignmentFileName = "mafft_result.fa"
        outputSubTypeGSelectionFileName = "subTypeG.fa"
        outputNoGapsFileName = "outputNoGaps.fa"
        outputNoHighlyMutRegFileName = "outputSubGRemovedHighMutRegion.fa"
        
        if not local:
            location = "/home/anaabecasis/Ewout/thesis/SQLAlchemy/DataFiles/"
            locationSubtypedFiles = "/home/anaabecasis/Ewout/thesis/SQLAlchemy/DataFiles/subtyped/"
            multipleAlignmentFileLocation = "/home/anaabecasis/Ewout/thesis/SQLAlchemy/DataFiles/"
            multipleAlignmentFileName = "mafft_result.fa"
            outputSubTypeGSelectionFileName = "subTypeG.fa"
            outputNoGapsFileName = "outputNoGaps.fa"
            outputNoHighlyMutRegFileName = "outputSubGRemovedHighMutRegion.fa"
        
        
        self.csvController = CSVController.CSVController(location)
        self.sqlController = SQLController.SQLController(self.csvController)
        self.fileController = FileController.FileController(self.sqlController)
        self.treeController = TreeController.TreeController(self.sqlController)
        self.sequenceController = SequenceController.SequenceController()
        self.clusterController = ClusterController.ClusterController(self.sqlController, self.treeController, self.sequenceController)
        
#         print "Controller instantiated"
#         self.sqlController.createTables()
#         print "Tables created"
#         self.sqlController.insertPatients('patients.csv')
#         print "Patients inserted. " + str(self.sqlController.patientSkippedCounter) + " patient entries were skipped."
#         self.sqlController.insertTherapies('therapies.csv')
#         print "Therapies inserted. " + str(self.sqlController.therapySkippedCounter) + " therapies entries were skipped."
#         self.sqlController.insertTests('tests.csv')
#         print "Tests inserted. " + str(self.sqlController.testSkippedCounter) + " tests entries were skipped."
#         self.sqlController.insertEvents('events.csv')
#         print "Events inserted. " + str(self.sqlController.eventSkippedCounter) + " event entries were skipped."
#         self.sqlController.insertSamples('viral_isolates.csv', locationSubtypedFiles, True)
#         print "Samples inserted. " + str(self.sqlController.sampleSkippedCounter) + " sample entries were skipped."
#         self.sqlController.insertAlignedSeq(self.fileController, self.treeController, multipleAlignmentFileLocation, outputNoGapsFileName)
#         print "AlignedSeq added to samples."
#         self.sqlController.insertEditedSeq(self.fileController, self.treeController, multipleAlignmentFileLocation, outputNoHighlyMutRegFileName)
#         print "EditedSeq added to samples."

#        self.fileController.filterSubtypeGFromFastaFileToFastaFile(multipleAlignmentFileLocation, multipleAlignmentFileName, multipleAlignmentFileLocation, outputSubTypeGSelectionFileName)
#        print "Sequences with subtype G have been selected from: " + multipleAlignmentFileLocation + multipleAlignmentFileName + " and are written to: " + multipleAlignmentFileLocation + outputSubTypeGSelectionFileName

#        '''Remove the gaps '''
#        self.fileController.removeGapsFromFastaFileToFastaFile(multipleAlignmentFileLocation, outputSubTypeGSelectionFileName, multipleAlignmentFileLocation, outputNoGapsFileName)
#        print "The gaps in the sequences have been removed."
        
#        '''Remove the highly mutable regions'''
#        self.fileController.removeHighlyMutRegionsFromFastaFileToFastaFile(multipleAlignmentFileLocation, outputNoGapsFileName, multipleAlignmentFileLocation, outputNoHighlyMutRegFileName)
#        print "The highly mutable regions in the sequences have been removed."
        
#        self.treeController.getAllowedDailyDistance(Tree(location+'newickTree.nh' ))


#         allowedDistanceList = [0.015]
#         bootstrapSupportList = [90]
#          
#         for allowedDistance in allowedDistanceList:
#             for bootstrapSupport in bootstrapSupportList:
#                 print "Allowed distance: " + str(allowedDistance) + " Bootstrap support: " + str(bootstrapSupport)
#                 clusters = self.treeController.getAllTransmissionClusters(Tree(location+'newickTree.nh'), bootstrapSupport, allowedDistance, False)
#                 print "Number of clusters: " + str(len(clusters))
#                 
#                 for cluster in clusters:
#                     amountPatients = self.clusterController.countPatients(cluster)
#                     amountTreated, amountNonTreated = self.clusterController.countTreatedNonTreatedPatients(cluster)
#                 
#                     print "Cluster has " + str(amountPatients) + " patient(s) from which " + str(amountTreated) + " are treated and " + str(amountNonTreated) + " are not treated."



#                clusters1 = [Tree("(A:1,(B:1,(E:1,D:1):0.5):0.5);" )]
#                clusters2 = [Tree("(A:1,(B:1,(E:1,D:1):0.5):0.5);" )]
          
#                 count = 0
#                 booleanFound = False
#                 for cluster in clusters2:
#                     for cluster2 in clusters1:
#                         if set(cluster.get_leaf_names()) == set(cluster2.get_leaf_names()):
#                             count += 1
#                             booleanFound = True
#                             break
#                     if not booleanFound:
#                         #print cluster
#                         pass
#                     else:
#                         booleanFound = False
#                 print "Number of overlapping clusters: " + str(count)
#                  
#                 if not str(bootstrapSupport) in bootstrapDict:
#                     bootstrapDict[str(bootstrapSupport)] = []
#                  
#                 bootstrapDict[str(bootstrapSupport)].append(len(clusters1))
#                 bootstrapDict[str(bootstrapSupport)].append(len(clusters2))
#                 bootstrapDict[str(bootstrapSupport)].append(count)
        
#         bootstrapDict = dict()
#         bootstrapDict['90'] = [574,329,242,574,378,284]
#         bootstrapDict['85'] = [605,343,241,605,395,283]
        
#         fileOut = open('/Users/EwoutVE/Documents/eclipse/workspace/SQLAlchemy/DataFiles/resultOverview2.csv', 'w')
#         fileOut.write(";")
#         for i in allowedDistanceList:
#             fileOut.write("With_Days;Without_Days;Overlaps;")
#         fileOut.write("\nClusters;")
#         for i in allowedDistanceList:
#             for j in range(0,3):
#                 fileOut.write(str(i) + ";")
#         fileOut.write("\n")
#         for element in bootstrapSupportList:
#             fileOut.write(str(element) + ";")
#             for i in bootstrapDict[str(element)]:
#                 fileOut.write(str(i) + ";")
#             fileOut.write("\n")
#         fileOut.close()
        
#        self.treeController.test(Tree(location+'newickTree.nh'))
#        self.treeController.getDistances("subsetRight.txt", self.csvController)
#        self.treeController.getAverageViralLoad("subsetRight.txt", self.csvController)
#        self.treeController.getPatientIdNrSamplesIntPatDistLog("subsetRight.txt", self.csvController)
#        print patients[4]
#         patientList = []
#         for patient in patients:
#             patientList.append(patient[1])
#         print len(list(set(patientList)))
#        print self.sqlController.getPatientIdMaxViralLoadTreated()[553]
#        self.treeController.getDistances("subsetLeft.txt", self.csvController)

#        self.treeController.getDistances(Tree(location+'newickTree.nh' ))
        
#        print Tree(location+'newickTree.nh').get_distance('43215_76045_2002', '43215_E76045_2002')

        print self.clusterController.getResistanceMutations(Tree(location+'newickTree.nh' ))

Main()