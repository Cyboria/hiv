'''
Created on 27 Mar 2014

@author: EwoutVE
'''
from sqlalchemy import create_engine, Text, Date, Column, Integer, String, ForeignKey

class Therapy(Base):
    __tablename__ = 'therapies'
    
    patientId = Column(Integer, ForeignKey('patients.id'))
    startDate = Column(Date)
    stopDate = Column(Date)
    drugNames = Column(Text)
    drugTypes = Column(String(length=45))
    id = Column(Integer, autoincrement=True, primary_key=True)
    
    def __init__(self, patientId, startDate, stopDate, drugNames, drugTypes):
        self.patientId = patientId
        self.startDate = startDate
        self.stopDate = stopDate
        self.drugNames = drugNames
        self.drugTypes = drugTypes
    
    def __repr__(self):
        return "<Test(patientId='%s', startDate='%s', stopDate='%s', drugNames='%s', drugTypes='%s')>" % (self.patientId, self.startDate, self.stopDate, self.drugNames, self.drugTypes)
