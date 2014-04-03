'''
Created on 30 Mar 2014

@author: EwoutVE
'''

class SequenceController:

    def __init__(self):
        self.cutProtease = [23, 24, 30, 32, 46, 47, 48, 50, 53, 54, 73, 76, 82, 83, 84, 85, 88, 90]
        self.cutRT = [41, 65, 67, 69, 70, 74, 75, 77, 100, 101, 103, 106, 115, 116, 151, 179, 181, 184, 188, 190, 210, 215, 219, 225, 230]
 
        
    def removeNucleotidesHighlyMutableRegions(self, sequence):
        mutable = sequence.tomutable()
        for i in reversed(self.cutRT):
            mutable.__delitem__((i*3)+297 - 1)
            mutable.__delitem__((i*3)+297 - 2)
            mutable.__delitem__((i*3)+297 - 3)
        for i in reversed(self.cutProtease):
            mutable.__delitem__((i*3) - 1)
            mutable.__delitem__((i*3) - 2)
            mutable.__delitem__((i*3) - 3)
        return mutable.toseq()
