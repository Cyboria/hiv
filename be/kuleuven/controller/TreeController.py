'''
Created on 31 Mar 2014

@author: EwoutVE
'''
import re
from decimal import *
import math
import time
from be.kuleuven.model.SQLModel import Sample

class TreeController:

    def __init__(self, sqlController):
        self.sqlController = sqlController
    
    def median(self, mylist):
        sorts = sorted(mylist)
        length = len(sorts)
        if not length % 2:
            return (sorts[length / 2] + sorts[length / 2 - 1]) / 2.0
        return sorts[length / 2]
    
    def getTransmissionClusters(self, treeLocation, allowedDistance, bootstrapSupport):
        ''''''
    def getAllowedDailyDistance(self, tree):
        time_start = time.time()
        patientsMultipleSamples = self.sqlController.getPatientsHavingMultipleSamplesSubtypeG()
        pattern = re.compile("^Node names")
        
        #print "PatientsMultipleSamples: " + str(patientsMultipleSamples.count())
        
        i = 0
        patientDistances = dict()
        patientDistancesNoChange = dict()
        patientDays = dict()
        
        nrOfItems = patientsMultipleSamples.count()
        while i < nrOfItems - 1:
            firstDate = patientsMultipleSamples[i][3]
            j = 1            
            while patientsMultipleSamples[i][1] == patientsMultipleSamples[i+j][1]:
                secondDate = patientsMultipleSamples[i+j][3]         
                difference = (abs(firstDate - secondDate)).days
                if difference != 0.0:
                    try:
                        leaf_1 = patientsMultipleSamples[i][0].split("-")[0]
                        leaf_2 = patientsMultipleSamples[i+j][0].split("-")[0]
                        distance = tree.get_distance(leaf_1, leaf_2)
                        
                        if str(patientsMultipleSamples[i][1]) == str(74341):
                            print "Leaf 1: " + str(patientsMultipleSamples[i][0].split("-")[0])
                            print "Leaf 2: " + patientsMultipleSamples[i+j][0].split("-")[0]
                            
                            print "Distance: " + str(distance)
                            print "Difference: " + str(difference)
                             
                        if not str(patientsMultipleSamples[i][1]) in patientDistances:
                            patientDistances[str(patientsMultipleSamples[i][1])] = []
                            
                        if not str(patientsMultipleSamples[i][1]) in patientDistancesNoChange:
                            patientDistancesNoChange[str(patientsMultipleSamples[i][1])] = []
                            
                        if not str(patientsMultipleSamples[i][1]) in patientDays:
                            patientDays[str(patientsMultipleSamples[i][1])] = []
                            
                        patientDistances[str(patientsMultipleSamples[i][1])].append(1000*float(distance)/float(difference))
                        patientDistancesNoChange[str(patientsMultipleSamples[i][1])].append(float(distance))
                        patientDays[str(patientsMultipleSamples[i][1])].append(difference)
                        
                    except ValueError as error:
                        if not pattern.match(str(error)):
                            print error
                if (i + j + 1) < nrOfItems:
                    j += 1
                else:
                    break
            i += 1
 
        avgDistanceAll = 0
        fileOut = open('/Users/EwoutVE/Documents/eclipse/workspace/SQLAlchemy/DataFiles/distancesBackup.txt', 'w')
        
        for patientId, value in patientDistances.items():
            if sum(value)/len(value) != 0:
                fileOut.write(str(patientId) + ";" + str(Decimal((sum(value)/len(value))*365/1000)) + ";" + str(Decimal((sum(patientDistancesNoChange[str(patientId)])/len(patientDistancesNoChange[str(patientId)])))) + ";" + str(sum(patientDays[str(patientId)])/len(patientDays[str(patientId)])) + ";" + str(len(value)) + "\n")
                avgDistanceAll += sum(value)/len(value)
        fileOut.close()
        
        print (str((avgDistanceAll/len(patientDistances.values()))/1000) + ' AVERAGE DISTANCE PER DAY' + '\n')
        print (str((avgDistanceAll/len(patientDistances.values()))*365/1000) + ' TOTAL DISTANCE PER YEAR')
        print ("The method stopped running after: " + str(int(time.time() - time_start)) + " seconds")

#        print ('MEDIAN: ' + str(self.median(patientDistances)))
        
    def getDistances(self, tree):
        print "Calculating Distance.\n"
        pattern = re.compile("^Node names")
        samplesFromPatientHavingMultipleSamples = self.sqlController.getPatientsHavingMultipleSamplesSubtypeG()
        maxSamplesDict = dict()
        
        nrOfItems = samplesFromPatientHavingMultipleSamples.count()
        i = 0
        
        currentPatientId = samplesFromPatientHavingMultipleSamples[0].patientId
        maxDifference = 0
        maxDistance = 0
        sample1 = 0
        sample2 = 1
        
        while i < nrOfItems - 1:
            firstDate = samplesFromPatientHavingMultipleSamples[i].sampleDate
            j = 1
            
            if samplesFromPatientHavingMultipleSamples[i].patientId != currentPatientId:
                print "PatientId: " + str(samplesFromPatientHavingMultipleSamples[i].patientId)
                currentPatientId = samplesFromPatientHavingMultipleSamples[i].patientId
                
                try:
                    leaf_1 = str(str(samplesFromPatientHavingMultipleSamples[sample1].patientId) + "_" + str(samplesFromPatientHavingMultipleSamples[sample1].sampleId) + \
                                 "_" + str(samplesFromPatientHavingMultipleSamples[sample1].sampleDate).split("-")[0])
                    leaf_2 = str(str(samplesFromPatientHavingMultipleSamples[sample2].patientId) + "_" + str(samplesFromPatientHavingMultipleSamples[sample2].sampleId) + \
                                 "_" + str(samplesFromPatientHavingMultipleSamples[sample2].sampleDate).split("-")[0])
                    
                    print "Leaf1: " + str(leaf_1) + "Leaf2: " + str(leaf_2)
                    
                    maxDistance = tree.get_distance(leaf_1, leaf_2)
                    maxSamplesDict[str(samplesFromPatientHavingMultipleSamples[i].patientId)] = (maxDifference, maxDistance)
                    print "Max Difference: " + str(maxDifference) + " Max Distance: " + str(maxDistance)
                except ValueError as error:
                    if not pattern.match(str(error)):
                        print error
                
                maxDifference = 0
                maxDistance = 0
                
            while samplesFromPatientHavingMultipleSamples[i].patientId == samplesFromPatientHavingMultipleSamples[i+j].patientId:
                secondDate = samplesFromPatientHavingMultipleSamples[i+j].sampleDate
                difference = (abs(firstDate - secondDate)).days
                
                if difference > maxDifference:
                    maxDifference = difference
                    sample1 = i
                    sample2 = i+j

                if (i + j + 1) < nrOfItems:
                    j += 1
                else:
                    break
            i += 1
                
        fileOut = open('/Users/EwoutVE/Documents/eclipse/workspace/SQLAlchemy/DataFiles/overview.txt', 'w')
        fileOut.write("PatientId;DaysDifference;intra_patient_distance;log(intra_patient_distance)"+ "\n")

        for key, value in maxSamplesDict.items():
            fileOut.write(str(key) + ";" + str(value[0]) + ";" + str(value[1]) + ";" + str(math.log(value[1])) + "\n")
        fileOut.close()
 
    def getAverageViralLoad(self, fileName, csvController):
        csvController.setFileName(fileName)
        reader = csvController.getReader(False)
         
        patientDict = dict()
        for row in reader:
            patientDict[str(row[1])] = row[2]
         
        reader = csvController.getReader(False)
        patientDictAvgLoad = dict()
         
        avgLoad = self.sqlController.getAverageLoadPatient()
        for avgLoadSpecific in avgLoad:
            patientDictAvgLoad[str(avgLoadSpecific[0])] = avgLoadSpecific[1]
             
        fileOut = open('/Users/EwoutVE/Documents/eclipse/workspace/SQLAlchemy/DataFiles/overview.txt', 'w')
        fileOut.write("PatientId;Max Viral Load;IntraPatientDistance \n")
        for row in reader:
            if row[1] in patientDictAvgLoad.keys():
                fileOut.write(str(row[1]) + ';' + str(patientDictAvgLoad[str(row[1])])+ ';' + str(patientDict[str(row[1])]) + "\n")
        fileOut.close()
         
    def getPatientIdNrSamplesIntPatDistLog(self, fileName, csvController):
        csvController.setFileName(fileName)
        reader = csvController.getReader(False)
         
        patientDict = dict()
        for row in reader:
            patientDict[str(row[1])] = row[2]
         
        patientsMultipleSamples = self.sqlController.getPatientSampleCountHavingMultipleSamplesSubtypeG()
         
        fileOut = open('/Users/EwoutVE/Documents/eclipse/workspace/SQLAlchemy/DataFiles/overview.txt', 'w')
        fileOut.write("PatientId;#Samples;intraPatientDist;Log \n")
        for element in patientsMultipleSamples:
            if str(element[0]) in patientDict.keys():
                fileOut.write(str(element[0]) + ';' + str(element[1]) + ';' + patientDict[str(element[0])] + ';' + str(math.log(Decimal(patientDict[str(element[0])]))) + "\n")
        fileOut.close()
        
#     def getAllTransmissionClusters(self, tree):
#         print "This tree has" + len(tree) + "terminal nodes [proper way: len(tree) ]"
#         for node in self._tree.traverse("postorder"):
#             children = node.get_children()
#             if len(children) != 0:
    
#     def branchesBootstrap(self, node, bootstrap):
#         if node.support >= bootstrap:
#             return True
#         else:
#             return False
    
    def getAllTransmissionClusters(self, tree, bootstrapTreshold, distanceTreshold, includingDays):
        #print tree.get_distance("574878_BM11979_2008","574878_BM34627_2010", topology_only=True)
        #print tree.get_distance("574878_BM11979_2008","574878_BM25772_2009", topology_only=True)
        #print len(tree.search_nodes(support=70))
        tree.set_outgroup(tree&"Ref.B.FR.83.HXB2_LAI_IIIB_BRU.K03455")
        # matches = filter(lambda n: self.branchesBootstrap(n,70), tree.traverse("preorder"))
        # print len(matches)
        # print "Root: " + str(tree.get_tree_root().is_root())
        self.clusters = []
        self.samplesSubtypeG = self.sqlController.getSamplesSubtypeG()
        self.preorder(tree.get_tree_root(), bootstrapTreshold, distanceTreshold, includingDays)
        return self.clusters
    
    def leafNameToObjects(self, leafName):
        sample = leafName.split("_")
        patientId = int(sample[0])
        arrayLength= len(sample)
        sampleId = ""
        if(arrayLength > 3):
            # print "ArrayLength: " + str(arrayLength)
            sampleId = sample[1]
            for i in range(2,arrayLength - 1):
                # print "Item: " + str(i) + " Content: " + str(splitted_id[i])
                sampleId = sampleId + "_" + sample[i]
        else:
            sampleId = sample[1]
        
        return patientId, sampleId
    
    def isTransmissionCluster(self, node, distanceTreshold, includingDays):
        leaves = node.get_leaves()
        totalDistance = 0.0
  #      totalDayDistance = 0.0
        count = 0
        
        for i in range(len(leaves) - 1):
            #print "i: " + str(i) + " leaf i: " + str(leaves[i])
            for j in range(i+1, len(leaves)):
                #print "j: " + str(j) + " leaf j: " + str(leaves[j])
                
                if includingDays:
                    try:
                        #print "Sample: " + str(sample1) + " or sample: " + str(sample2)
                        #print abs(self.samplesSubtypeG[self.samplesSubtypeG.index(Sample(sample1[0], sample1[1], None, None, None, None, None, None))].sampleDate -\
                        #self.samplesSubtypeG[self.samplesSubtypeG.index(Sample(sample2[0], sample2[1], None, None, None, None, None, None))].sampleDate).days
                        
                            patientId1, sampleId1 = self.leafNameToObjects(leaves[i].name)
                            patientId2, sampleId2 = self.leafNameToObjects(leaves[j].name)
                            daysDifference = abs(self.samplesSubtypeG[self.samplesSubtypeG.index(Sample(patientId1, sampleId1, None, None, None, None, None, None))].sampleDate -\
                            self.samplesSubtypeG[self.samplesSubtypeG.index(Sample(patientId2, sampleId2, None, None, None, None, None, None))].sampleDate).days
                        
                            if daysDifference > 0:
                                totalDistance += (node.get_distance(leaves[i],leaves[j]) / daysDifference)
                    except ValueError:
                        #print "Sample: " + str(sample1) + " or sample: " + str(sample2) + " not found in the database."
                        pass
                else:
                    totalDistance += node.get_distance(leaves[i],leaves[j])
                count += 1
                
        if count != 0:
            #print totalDayDistance
            meanDistance = totalDistance/count
            
            if meanDistance < distanceTreshold:
                return True
            else:
                return False
        else:
            return False
    
    def preorder(self, node, bootstrapTreshold, distanceTreshold, includingDays):
        if node.is_leaf(): 
            return  
        if node.support > bootstrapTreshold:
            if self.isTransmissionCluster(node, distanceTreshold, includingDays):
                self.clusters.append(node)
                return
        self.preorder(node.get_children()[0], bootstrapTreshold, distanceTreshold, includingDays)
        self.preorder(node.get_children()[1], bootstrapTreshold, distanceTreshold, includingDays)