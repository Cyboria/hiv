'''
Created on 27 Mar 2014

@author: EwoutVE
'''
#from be.kuleuven.controller import CSVController
from be.kuleuven.model import SQLModel
from be.kuleuven.model.SQLModel import Patient, Therapy, Test, Event, Sample
from sqlalchemy import func, and_
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import exists
from sqlalchemy.exc import IntegrityError
import glob
import difflib
import logging

import time

class SQLController:

    def __init__(self, csvController):
        logging.basicConfig()
        self.csvController = csvController
        self.engine = SQLModel.engine
        self.Base = SQLModel.Base
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        
        self.patientSkippedCounter = 0
        self.therapySkippedCounter = 0
        self.testSkippedCounter = 0
        self.eventSkippedCounter = 0
        self.sampleSkippedCounter = 0
        
        self.logger = logging.getLogger('SQLAlchemy')
        self.logger.setLevel(logging.DEBUG)
    
    def createTables(self):
        self.Base.metadata.create_all(bind=self.engine, checkfirst=True)
    
    def insertPatients(self, fileName):
        '''Inserts the patients from the dump into the database'''
                
        self.csvController.setFileName(fileName)
        reader = self.csvController.getReader(False)
        
        for row in reader:            
            patientId = 0
            try:
                patientId = int(row[0])
            except ValueError:
                self.logger.warn("ValueError in method insertPatients while converting patientID: " + row[0] + " is no int")
            birthdate = '1800-01-01'
            diagnosis_date = None
            birthday = row[2].split('/')
            if len(birthday) > 1:
                birthdate = birthday[2] + '-' + birthday[1] + '-' + birthday[0]
            diag_date = row[4].split('/')
            if len(diag_date) > 1:
                diagnosis_date = diag_date[2] + '-' + diag_date[1] + '-' + diag_date[0]
            gender = row[7]
            if gender == 'male':
                gender = 'M'
            elif gender == 'female':
                gender = 'F'
            institution = row[12] 
            if patientId != 0:
                patient = Patient(patientId, birthdate, gender, institution, diagnosis_date)
#                if not self.session.query(exists().where(Patient.patientId==patientId)).scalar():
                try:
                    self.session.add(patient)
                    self.session.flush()
                except IntegrityError as err:
#                    print("Tried to add a duplicate entry for the Patient value "+str(patient.__repr__())+". Aborting")
                    self.patientSkippedCounter += 1
                    self.session.rollback()
        self.session.commit()
    
    def getDate(self, date):
        
        # TODO:
        # For Therapies
        # ['412759', '1001-01-01', '4/7/08', '', 'EFV AZT 3TC ']
        # ['60996', '0998-01-28', '7/15/99', 'Other', 'DDI AZT ']
        # ['590306', '0207-01-04', '', '', 'ABC EFV 3TC ']
        # For events
        # ['69505', 'Therapy Failure', '0200-04-05', '', 'Negative']
        # ['77067', 'Therapy Failure', '008-07-24', '', 'Negative']
        # ['634408', 'Therapy Failure', '009-12-18', '', 'Negative']
        # ['668470', 'Therapy Failure', '1010-10-21', '', 'Negative']
        
        #print date
        
        # Determine delimitor and the first element
        delimitor = ''
        firstElem = ''
        
        if date != '':
            if len(str(date).split('/')) >= 2:
                delimitor = '/'
                firstElem = str(date).split('/')[0]
            elif len(str(date).split('-')) >= 2:
                delimitor = '-'
                firstElem = str(date).split('-')[0]
            else:
                print "Date: " + date + " Unknown delimitor: " + delimitor

        if len(firstElem) > 2 and (date.startswith('10') or date.startswith('0')):
#            self.counter = self.counter + 1
#            print "Counter is %d" % self.counter + " : " + date + " is wrong format."
            return date
        else:
            try:
                tempDate = time.strptime(date, "%m"+delimitor+"%d"+delimitor+"%y")
            except:
                try:
                    tempDate = time.strptime(date, "%d"+delimitor+"%m"+delimitor+"%y")
                except:
                    try:
                        tempDate = time.strptime(date, "%d"+delimitor+"%m"+delimitor+"%Y")
                    except:
                        raise ValueError('Wrong date format')

        return time.strftime("%Y-%m-%d", tempDate)

    def insertTherapies(self, fileName):
        '''Insert the therapies from the original database to the new database from the dump'''
        
        self.csvController.setFileName(fileName)
        reader = self.csvController.getReader(False)
    
        for row in reader:
            # print row
    
            drugNames = ''
            patientId = 0
            startDate = ''
    
            stopDate = ''
            
            # TODO: What to do with patientID's which are no int's
            # ['ACMAS', '7/1/04', '11/9/11', '', 'NVP 3TC AZT ']
            # ACMAS is no int
            # ['MESFAC', '6/1/11', '12/27/11', '', '3TC EFV AZT ']
            # MESFAC is no int
            try:
                patientId = int(row[0])
            except ValueError:
                self.logger.warn("ValueError in method insertTherapies while converting patientID: " + row[0] + " is no int")
                
            try:
                startDate = self.getDate(row[1])
            except:
                # print row[1]
                startDate = time.strftime("%Y-%m-%d", time.strptime(row[1], "%Y-%m-%d"))
            try:
                stopDate = self.getDate(row[2])
            except:
                stopDate = None
    
            drugNames = row[4]
            drugNames = str.replace(drugNames, ' ', ',')
            drugNames = str.replace(drugNames, '/r', '')
            drugNames = drugNames.rstrip(',\n')
            drugs = drugNames.split(',')
            drugType = ''
            for i in range(len(drugs)):
                if (drugs[i] == 'ABC') or (drugs[i] == 'DDI') or (drugs[i] == 'FTC') or (drugs[i] == '3TC') or (drugs[i] == 'D4T') or (drugs[i] == 'TDF') or (drugs[i] == 'AZT') or (drugs[i] == 'DDC'):
                    if drugType.count('_nRTI') == 0:
                        drugType += '_nRTI'
                elif (drugs[i] == 'EFV') or (drugs[i] == 'ETV') or (drugs[i] == 'NVP'):
                    if drugType.count('_NNRTI') == 0:
                        drugType += '_NNRTI'
                elif (drugs[i] == 'ATV') or (drugs[i] == 'DRV') or (drugs[i] == 'FPV') or (drugs[i] == 'IDV') or (drugs[i] == 'LPV') or (drugs[i] == 'NFV') or (drugs[i] == 'SQV') or (drugs[i] == 'TPV') or (drugs[i] == 'RTV') or (drugs[i] == 'APV'):
                    if drugType.count('_PI') == 0:
                        drugType += '_PI'
                elif (drugs[i] == 'T20') or (drugs[i] == 'MVC'):
                    if drugType.count('_EI') == 0:
                        drugType += '_EI'
                elif (drugs[i] == 'RTG'):
                    if drugType.count('_INI') == 0:
                        drugType += '_INI'
                else:
                    pass
            drugTypes = drugType.lstrip('_')
            drugNames = str.replace(drugNames, ',', '_')
            
            if(patientId != 0):
                therapy = Therapy(patientId, startDate, stopDate, drugNames, drugTypes)
                try:
                    self.session.add(therapy)
                    self.session.flush()
                except IntegrityError as err:
#                    print("Tried to add a duplicate entry for the Therapy value "+str(therapy.__repr__())+". Aborting")
                    self.therapySkippedCounter += 1
                    self.session.rollback()
        self.session.commit()
        
    def insertTests(self, fileName):
        '''Insert the CD4 counts and viral loads in the database.
    
        This method will insert the CD4 counts and the viral loads into
        the database from a csv file.
    
        @param: fileName: The path to the csv file containing the test data.
        '''
    
        self.csvController.setFileName(fileName)
        reader = self.csvController.getReader(False)

        for row in reader:
            testType = ''
            patientId = 0
            sampleId = ''
            testValue = ''
            
            try:
                patientId = int(row[0])
            except ValueError:
                self.logger.warn("ValueError in method insertTests while converting patientID: " + row[0] + " is no int")
            
            if row[2].startswith('Viral'):
                testType = 'Viral_load'
            elif row[2].startswith('CD4'):
                testType = 'CD4'
            else:
                testType = "None"
            testDate = row[3]
            sampleId = row[4]
            # What is done here is the replacement of the str values <>= by their respective numerical values
            try:
                # Was before testValue = int(row[5].translate(None, '<>=')) but changed now
                testValue = int(row[5].translate(None, '<>=.'))
            except:
                testValue = None
                
            if (testType == 'Viral_load' or testType == 'CD4') and patientId != 0:
                # Duplicate rows are ignored
                # print "PatientId: " + str(patientId) + " SampleId: " + str(sampleId) + " TestDate: " + testDate + " TestType: " + testType + " TestValue: " + str(testValue)
                test = Test(patientId, sampleId, testDate, testType, testValue)
                try:
                    self.session.add(test)
                    self.session.flush()
                except IntegrityError as err:
#                    print("Tried to add a duplicate entry for the Test value "+str(test.__repr__())+". Aborting")
                    self.testSkippedCounter += 1
                    self.session.rollback()
            self.session.commit()
            
    def insertEvents(self, fileName):
        self.csvController.setFileName(fileName)
        reader = self.csvController.getReader(False)

        for row in reader:
            patientId = 0
            value = ''
            event = ''
            
            try:
                patientId = int(row[0])
            except ValueError:
                self.logger.warn("ValueError in method insertEvents while converting patientID: " + row[0] + " is no int")
            
            # TODO:
            # There are rows with an empty start date. What to do with those.
            # The problem is that empty start date is not allowed in the database.
            if row[2] != '':
                try:
                    startDate = self.getDate(row[2])
                except:
                    startDate = time.strftime("%Y-%m-%d", time.strptime(row[2], "%Y-%m-%d"))
            
            if str(row[3]) != '':
                try:
                    stopDate = self.getDate(row[3])
                except:
                    stopDate = time.strftime("%Y-%m-%d", time.strptime(row[3], "%Y-%m-%d"))
            else:
                stopDate = None
            
            event = row[1]
            value = row[4]
            
#            TODO: Do we only want the events with a stopDate?
#            TODO: What to do with entries which are exactly the same? e.g. 698848-Pregnancy-2001-10-01
#            if stopDate != None:
#            print "PatientId: " + str(patientId) + " Event: " + event + " StartDate: " + str(startDate) + " StopDate: " + str(stopDate) + " Value: " + str(value)
            if patientId != 0:
                event = Event(patientId, event, startDate, stopDate, value)
                try:
                    self.session.add(event)
                    self.session.flush()
                except IntegrityError as err:
#                    print("Tried to add a duplicate entry for the Event value "+str(event.__repr__())+". Aborting")
                    self.eventSkippedCounter += 1
                    self.session.rollback()
            self.session.commit()
            
    def insertSamples(self, locationSubtypedFiles, calledFromMain):
        # print file
        if(calledFromMain):
            self.csvController.setLocation(locationSubtypedFiles)
            csvFiles = glob.glob(locationSubtypedFiles + "*.csv")
            
            for i in csvFiles:
                diff = difflib.ndiff(i, locationSubtypedFiles)
                delta = ''.join(x[2:] for x in diff if x.startswith('- '))
                self.insertSamples(delta, False)
            return
        
#        fileName = locationSubtypedFiles.split('.csv')
        self.csvController.setFileName(locationSubtypedFiles)
        reader = self.csvController.getReader(False)
        
        # row[0] = patientID_sequenceID_year
        # row[1] = sequence length
        # row[2] = subtype assignment
        # row[4] = subtype support percentage
        
        for row in reader:
            splitted_id = row[0].split("_")
            patientId = 0
            try:
                patientId = int(splitted_id[0])
            except ValueError:
                self.logger.warn("ValueError in method fillSamples while converting patientID: " + splitted_id[0] + " is no int")
            
            arrayLength= len(splitted_id)
            sampleId = ""
            if(arrayLength > 3):
                # print "ArrayLength: " + str(arrayLength)
                sampleId = splitted_id[1]
                for i in range(2,arrayLength - 1):
                    # print "Item: " + str(i) + " Content: " + str(splitted_id[i])
                    sampleId = sampleId + "_" + splitted_id[i]
            else:
                sampleId = splitted_id[1]
            
            try:
                sampleYear = splitted_id[arrayLength - 1]
            except:
                sampleYear = None
            # print "Patient ID: " + splitted_id[0] + " Sequence: " + splitted_id[1] + " Year: " + splitted_id[2]
        
            subType = None
            
            # Only give them a subtype if it has a 100% support
            
            try:
                if(row[4] != "" and int(float(row[4])) > 70):
                    subType = row[2]
                    subType = str(subType).replace("Subtype","")
                    subType = subType.replace("  "," ")
            except:
                self.logger.warn(row[4] + " can't be converted into an int.")
            
            # TODO: These patients do not exists:
            # Error on the following command: INSERT INTO samples (patientId, sampleId, sampleDate) VALUES (780065, BM78573, 2013)
            # Error on the following command: INSERT INTO samples (patientId, sampleId, sampleDate) VALUES (785556, BM89391, 2014)
            if patientId != 0:
                sample = Sample(patientId, sampleId, sampleYear, subType, None, None, None, None)
                try:
                    self.session.add(sample)
                    self.session.flush()
                except IntegrityError as err:
#                    print("Tried to add a duplicate entry for the Sample value "+str(sample.__repr__())+". Aborting")
                    self.sampleSkippedCounter += 1
                    self.session.rollback()
            self.session.commit()
            
    def getSamplesSubtypeG(self):
        return self.session.query(Sample).filter(Sample.subType.like('HIV-1 G%')).all()
    
    def getPatientsHavingMultipleSamplesSubtypeG(self):
        subquery = self.session.query(Sample.patientId, func.count(Sample.patientId)).group_by(Sample.patientId).having(func.count(Sample.patientId) > 1).filter(Sample.subType.like('HIV-1 G%')).subquery('subquery')
        return self.session.query(func.concat(Sample.patientId, '_', Sample.sampleId, '_', Sample.sampleDate)).filter(and_(Sample.patientId == subquery.c.patientId,))
    
#    def getAllSamplesFromPatients(self,query):
#        return self.session.query(func.concat(Sample.patientId, '_', Sample.sampleId, '_', Sample.sampleDate)).filter(and_(Sample.patientId == subquery.c.patientId,))