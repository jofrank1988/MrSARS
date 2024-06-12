MrSARS is a flexible, python (3.12.1) program that calculates sequence similarity scores between given sequences and a set of predefined reference sequences. 
MrSARS takes an input multifasta file and a list of reference sequence headers, which must be present in the input multifasta file. MrSARS utilizes Biopython’s (1.83)
SeqIO and PairwiseAligner modules to generate pairwise alignments between every ordered pair of sequences using the BLOSUM62 substitution matrix. MrSARS output
is a csv file where rows denote query sequences and columns denote pairwise min-max normalized similarity scores for each provided reference sequence. Additionally, 
an aggregate similarity score (i.e. sum of all pairwise scores) for each query sequence is provided in a separate column. 
We additionally developed a modified version of MrSARS (MrSARS-sampler) that runs the same logic as MrSARS, but with 1000 sets of 5 randomly sampled references 
from the input multifasta. The program then provides an output CSV file where every column represents a species, with each row storing the AS scores against one 
set of randomly sampled references. Finally, the last row stores true MrSARS AS scores against the provided reference species. 

Within this repository 'bin' contains scripts and programs implemented in the manuscript associated with this repository (journal article doi TBD). This encompasses 
MrSARS, MrSARS-sampler, and helper scripts used in data aquisition and processing.  The 'code' directory contains R-markdown files outlining explicit data acquisiton 
and processing steps conducted to generate data presented in our manuscript. These files encompass bash, python and R code used to generate and process all data. 

Please email john.frank@yale.edu or jofrank@linfield.edu if you have any questions. 
