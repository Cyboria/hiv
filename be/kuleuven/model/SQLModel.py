'''
Created on 27 Mar 2014

@author: EwoutVE
'''

from sqlalchemy import Text, Date, Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('mysql+mysqldb://ewout:tux2012@localhost:3306/HIV_TEST', encoding='latin1')
Base = declarative_base()

class Patient(Base):
    __tablename__ = 'patients'
    
    patientId = Column(Integer, primary_key=True, autoincrement=False)
    birthdate = Column(Date)
    gender = Column(String(length=1))
    institution = Column(String(length=10))
    diagnosis_date = Column(Date)

    def __init__(self, patientId, birthdate, gender, institution, diagnosis_date):
        self.patientId = patientId
        self.birthdate = birthdate
        self.gender = gender
        self.institution = institution
        self.diagnosis_date = diagnosis_date
    
    def __repr__(self):
        return "<Patient(patientId='%s', birthdate='%s', gender='%s', institution='%s', diagnosis_date='%s')>" % (self.patientId, self.birthdate, self.gender, self.institution, self.diagnosis_date)

class Event(Base):
    __tablename__ = 'events'
    
    patientId = Column(Integer, ForeignKey('patients.patientId', onupdate="CASCADE", ondelete="CASCADE"), primary_key=True)
    event = Column(String(length=45), primary_key=True)
    start_date = Column(Date, primary_key=True)
    end_date = Column(Date)
    value = Column(String(length=45))
    
    def __init__(self, patientId, event, start_date, end_date, value):
        self.patientId = patientId
        self.event = event
        self.start_date = start_date
        self.end_date = end_date
        self.value = value
    
    def __repr__(self):
        return "<Event(patientId='%s', event='%s', start_date='%s', end_date='%s', value='%s')>" % (self.patientId, self.event, self.start_date, self.end_date, self.value)

class Sample(Base):
    __tablename__ = 'samples'
    
    patientId = Column(Integer, ForeignKey('patients.patientId', onupdate="CASCADE", ondelete="CASCADE"), primary_key=True)
    sampleId = Column(String(length=45), primary_key=True)
    sampleDate = Column(String(length=4))
    subType = Column(String(length=40))
    rawSeq = Column(Text)
    alignedSeq = Column(Text)
    editedSeq = Column(Text)
    protSeq = Column(Text)
    
    def __init__(self, patientId, sampleId, sampleDate, subType, rawSeq, alignedSeq, editedSeq, protSeq):
        self.patientId = patientId
        self.sampleId = sampleId
        self.sampleDate = sampleDate
        self.subType = subType
        self.rawSeq = rawSeq
        self.alignedSeq = alignedSeq
        self.editedSeq = editedSeq
        self.protSeq = protSeq
    
    def __repr__(self):
        return "<Sample(patientId='%s', sampleId='%s', sampleDate='%s', subType='%s', rawSeq='%s', alignedSeq='%s', editedSeq='%s', protSeq='%s')>" % (self.patientId, self.sampleId, self.sampleDate, self.subType, self.rawSeq, self.alignedSeq, self.editedSeq, self.protSeq)

class Test(Base):
    __tablename__ = 'tests'
    
    patientId = Column(Integer, ForeignKey('patients.patientId', onupdate="CASCADE", ondelete="CASCADE"), primary_key=True)
    sampleId = Column(String(length=15))
    testDate = Column(Date, primary_key=True)
    testType = Column(String(length=15), primary_key=True)
    testValue = Column(Integer, nullable=False)
    
    def __init__(self, patientId, sampleId, testDate, testType, testValue):
        self.patientId = patientId
        self.sampleId = sampleId
        self.testDate = testDate
        self.testType = testType
        self.testValue = testValue
    
    def __repr__(self):
        return "<Test(patientId='%s', sampleId='%s', testDate='%s', testType='%s', testValue='%s')>" % (self.patientId, self.sampleId, self.testDate, self.testType, self.testValue)

class Therapy(Base):
    __tablename__ = 'therapies'
    
    patientId = Column(Integer, ForeignKey('patients.patientId', onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    startDate = Column(Date, nullable=False)
    stopDate = Column(Date)
    drugNames = Column(String(length=90))
    drugTypes = Column(String(length=45))
    id = Column(Integer, autoincrement=True, primary_key=True)
    
    __table_args__ = (UniqueConstraint('patientId', 'startDate', 'drugNames', 'drugTypes', name='_therapy_uc_'),
                      )
    
    def __init__(self, patientId, startDate, stopDate, drugNames, drugTypes):
        self.patientId = patientId
        self.startDate = startDate
        self.stopDate = stopDate
        self.drugNames = drugNames
        self.drugTypes = drugTypes
    
    def __repr__(self):
        return "<Therapy(patientId='%s', startDate='%s', stopDate='%s', drugNames='%s', drugTypes='%s')>" % (self.patientId, self.startDate, self.stopDate, self.drugNames, self.drugTypes)

# Session = sessionmaker(bind=engine)
# session = Session()
#  
# session.add(patient1)
# session.commit()
# Base.metadata.create_all(engine)