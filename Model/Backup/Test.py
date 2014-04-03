'''
Created on 27 Mar 2014

@author: EwoutVE
'''
from sqlalchemy import create_engine, Date, Column, Integer, String, ForeignKey

class Test(Base):
    __tablename__ = 'tests'
    
    patientId = Column(Integer, ForeignKey('patients.id'), primary_key=True)
    sampleId = Column(String(length=15))
    testDate = Column(Date, primary_key=True)
    testType = Column(String(length=15), primary_key=True)
    testValue = Column(Integer)
    
    def __init__(self, patientId, sampleId, testDate, testType, testValue):
        self.patientId = patientId
        self.sampleId = sampleId
        self.testDate = testDate
        self.testType = testType
        self.testValue = testValue
    
    def __repr__(self):
        return "<Test(patientId='%s', sampleId='%s', testDate='%s', testType='%s', testValue='%s')>" % (self.patientId, self.sampleId, self.testDate, self.testType, self.testValue)
    
    class Meta:
        unique_together = ("patientId", "testDate", "testType")