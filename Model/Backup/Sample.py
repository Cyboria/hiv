'''
Created on 27 Mar 2014

@author: EwoutVE
'''
from sqlalchemy import create_engine, Text, Column, Integer, String, ForeignKey

class Sample(Base):
    __tablename__ = 'samples'
    
    patientId = Column(Integer, ForeignKey('patients.id'), primary_key=True)
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

    
    class Meta:
        unique_together = ("patientId", "sampleId")