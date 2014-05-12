'''
Created on 30 Mar 2014

@author: EwoutVE
'''
from Bio import AlignIO
from Bio import SeqIO
from Bio.Alphabet import IUPAC
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio.Data import CodonTable
from Bio.Data import IUPACData

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

    def getNucleotidesHighlyMutableRegions(self, sequence):
        mutable = sequence.tomutable()
        
        for i in reversed(self.cutRT):
            mutable.__getitem__((i*3)+297 - 1)
            mutable.__getitem__((i*3)+297 - 2)
            mutable.__getitem__((i*3)+297 - 3)
        for i in reversed(self.cutProtease):
            mutable.__getitem__((i*3) - 1)
            mutable.__getitem__((i*3) - 2)
            mutable.__getitem__((i*3) - 3)
        return mutable.toseq()
    
    def generateProtFromAmbiguousDNA(self, s):
        standard_nucleotide = CodonTable.unambiguous_dna_by_name["Standard"]
        non_standard_nucleotide = IUPACData.ambiguous_dna_values
        aaTranslations = []
        for i in range(0,len(s),3):
            codon = s.tostring()[i:i+3]
            # list_possible_proteins(codon, forward_table, ambiguous_nucleotide_values)
            if codon.count('-') == 3:
                aa = ['-']
            elif codon.count('-') == 1 and codon.index('-') == 2:
                if codon[0] == 'U':
                    # UC- : Serine (S)
                    if codon [1] == 'C':
                        aa = ['S']
                elif codon[0] == 'C':
                    # CU- : Leucine (L)
                    if codon[1] == 'U':
                        aa = ['L']
                    # CC- : Proline (P)
                    elif codon[1] == 'C':
                        aa = ['P']
                    # CG- : Arginine (R)
                    elif codon[1] == 'G':
                        aa = ['R']
                elif codon[0] == 'A':
                    # AC- : Threonine (T)
                    if codon[1] == 'C':
                        aa = ['T']
                elif codon[0] == 'G':
                    # GU- : Valine (V)
                    if codon[1] == 'U':
                        aa = ['V']
                    # GC- : Alanine (A)
                    elif codon[1] == 'C':
                        aa = ['A']
                    # GG- : Glycine (G)
                    elif codon[1] == 'G':
                        aa = ['G']
            elif codon.count('-') < 3 and codon.count('-') > 0:
                aa = ['X']
            else:
                try:
                    aa = CodonTable.list_possible_proteins(codon,standard_nucleotide.forward_table,non_standard_nucleotide)
                except:
                    aa = ['X']
            aaTranslations.append(aa)
        return aaTranslations
    
    def compare(self, referenceSequence, other):
        mutableRefSeq = referenceSequence.tomutable()
        mutableOtherSeq = other.tomutable()
        
        mutatedLocationsRT = []
        mutatedLocationsProtease = []
        
        for i in reversed(self.cutRT):
            refAA = self.generateProtFromAmbiguousDNA(Seq(str(mutableRefSeq.__getitem__((i*3)+297 - 3) +
                                                         mutableRefSeq.__getitem__((i*3)+297 - 2) +
                                                         mutableRefSeq.__getitem__((i*3)+297 - 1)), IUPAC.ambiguous_dna))
            otherAA = self.generateProtFromAmbiguousDNA(Seq(str(mutableOtherSeq.__getitem__((i*3)+297 - 3) + 
                                                         mutableOtherSeq.__getitem__((i*3)+297 - 2) + 
                                                         mutableOtherSeq.__getitem__((i*3)+297 - 1)), IUPAC.ambiguous_dna))
            if refAA != otherAA:
                print "Location RT:" + str(i) + ": RefAA: " + str(refAA) + " OtherAA: " + str(otherAA)
                mutatedLocationsRT.append(i)
               
        for i in reversed(self.cutProtease):
            refAA = self.generateProtFromAmbiguousDNA(Seq(str(mutableRefSeq.__getitem__((i*3) - 1) +
                                                         mutableRefSeq.__getitem__((i*3) - 2) +
                                                         mutableRefSeq.__getitem__((i*3) - 3)), IUPAC.ambiguous_dna))
            otherAA = self.generateProtFromAmbiguousDNA(Seq(str(mutableOtherSeq.__getitem__((i*3) - 1) + 
                                                         mutableOtherSeq.__getitem__((i*3) - 2) + 
                                                         mutableOtherSeq.__getitem__((i*3) - 3)), IUPAC.ambiguous_dna))
            if refAA != otherAA:
                print "Location Protease:" + str(i) + ": RefAA: " + str(refAA) + " OtherAA: " + str(otherAA)
                mutatedLocationsProtease.append(i)
            
        return mutatedLocationsRT, mutatedLocationsProtease