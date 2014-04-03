'''
Created on 27 Mar 2014

@author: EwoutVE
'''
from sqlalchemy import create_engine, Date, Column, Integer, String, ForeignKey

class Event(Base):
    __tablename__ = 'events'
    
    patientId = Column(Integer, ForeignKey('patients.id'), primary_key=True)
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