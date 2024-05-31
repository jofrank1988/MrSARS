#code workflow idea: Create object for every species, give attributes for ACE2 encoding, self-similarity, and similarities dictionary. Will create computational inefficiency but be most human-readable
#competing idea: Create n x n matrix for number of species, calculate and clone upper triangle, divide columns by diagonal values to get full normalized matrix

#randomly sample m objects or columns, create aggregated score for all species. Repeat i times
#most likely simply export csv from there for R analysis

import os
import tkinter as tk
from tkinter import filedialog
from tkinter.filedialog import asksaveasfilename
from Bio import SeqIO
from io import StringIO
from Bio.Align import PairwiseAligner
from Bio.Align.substitution_matrices import load as load_matrix
import random
import pandas
from collections import Counter
import sys

window = tk.Tk()
window.geometry("600x600")
my_font1=('times', 18, 'bold')
my_font2=('times', 14, 'bold')
#a few global properties
window.grid_propagate(0)
window.grid_rowconfigure(1, weight=1)
window.grid_rowconfigure(2, weight=1)
window.grid_rowconfigure(3, weight=1)
window.grid_columnconfigure(0, weight=1)
#more global properties

var = tk.IntVar()
b3 = tk.Button(window, text='Run', 
width=20,command = lambda:var.set(1))

random.seed(10)
aligner = PairwiseAligner()
aligner.substitution_matrix = load_matrix("BLOSUM62")
aligner.open_gap_score = -5
aligner.extend_gap_score = -0.5
aligner.mode = 'global'

#Object class corresponding to a single species in the data
class Species:
    def __init__(self, name, encoding, init_scores, ref):
        self.encoding = encoding
        self.name = name
        self.scores = init_scores
        self.mirror_score = None
        self.is_ref = ref

    #calculates self-reference score to normalize, and then calculates all normalized homology scores
    def scores_calc(self):
        alignments = list(aligner.align(self.encoding, self.encoding))
        best_alignment = max(alignments, key=lambda a: a.score)
        self.mirror_score = best_alignment.score

        for key in self.scores:
            alignments = list(aligner.align(self.encoding, self.scores[key]))
            best_alignment = max(alignments, key=lambda a: a.score)
            self.scores[key] = best_alignment.score / self.mirror_score


#main function, just runs the relevant functions in order
def main():
    initial_ui()
    b3.wait_variable(var)
    file_process()
    sampler()
    output()

def cli_main():
    upload_fasta(1)
    upload_txt(1)
    file_process()
    sampler()
    output(1)
    

#uploads the fasta file
def upload_fasta(cli = 0):
    global seqs
    f_types = [('Fasta', '*.fasta')]
    if cli == 1:
        with open(input_file, 'r') as f:
            seqs = f.read()
    else:
        file_try = filedialog.askopenfile(mode='r', filetypes=f_types)
        if file_try is not None:
            seqs = file_try.read()

#uploads the text file, dubious if I needed two different functions but made things easier
def upload_txt(cli = 0):
    global refs
    f_types = [('Text Files', '*.txt')]
    if cli == 1:
        with open(ref_list_file, 'r') as f:
            refs = f.read()
    else:
        file_try = filedialog.askopenfile(mode='r', filetypes=f_types)
        if file_try is not None:
            refs = file_try.read()

#Creates the initial UI
def initial_ui():
    global var

    b1 = tk.Button(window, text='Upload Seqs', 
    width=20,command = lambda:upload_fasta())
    b1.grid(row=1, column = 1)

    b2 = tk.Button(window, text='Upload Refs', 
    width=20,command = lambda:upload_txt())
    b2.grid(row=1, column = 2)
    
    b3.grid(row=1, column = 3)

#processes the input, creating a list of objects
def file_process(): 
    global obs_list
    global seqs_dict
    global refs_list
    #breaks apart file into names and encodings
    fasta_io = StringIO(seqs) 
    seqs_dict = SeqIO.to_dict(SeqIO.parse(fasta_io, 'fasta'))

    refs_list = refs.splitlines()

    #creates list of objects
    obs_list = []
    for key in seqs_dict:
        obs_list.append(Species(key, seqs_dict[key], seqs_dict.copy(), 1 if key in refs_list else 0))
    
    #calculates normalized homology scores for all species (slightly computationally inefficient)
    for elt in obs_list:
        elt.scores_calc()

#for a set number of iterations, samples 5 random species to be the references, and then calculates the aggregate scores
def sampler():
    global main_m
    main_m = dict.fromkeys(seqs_dict,[])
    for i in range(1000):
        indices = random.sample(range(len(seqs_dict)),len(refs_list))
        temp = None
        for elt in indices:
            if temp == None:
                temp = Counter(obs_list[elt].scores)
            else:
                temp += Counter(obs_list[elt].scores)

        for key in temp:
            main_m.update({key:main_m[key]+[temp[key]]})
    
    #calculates and then appends the reference aggregate score to the end
    temp = None
    for elt in obs_list:
        if elt.is_ref == 1:
            if temp == None:
                temp = Counter(elt.scores)
            else:
                temp += Counter(elt.scores)
    for key in temp:
            main_m.update({key:main_m[key]+[temp[key]]})

def output(cli = 0):
    df = pandas.DataFrame.from_dict(main_m)
    #print(df)
    if cli == 1:
        df.to_csv(similarity_file, index=False)
    else:
        out = df.to_csv(index=False)
        filename = asksaveasfilename(initialfile = 'Untitled.csv',defaultextension=".csv",filetypes=[("All Files","*.*"),("CSV","*.csv")])
        f = open(filename, 'w')
        f.write(out)
        f.close()
    

def on_close():
     #Allows program to close "properly", if using os._exit is proper.

     close = tk.messagebox.askokcancel("Close", "Would you like to close the program?")
     if close:
        window.destroy()
        os._exit(1)  


window.protocol("WM_DELETE_WINDOW",  on_close)

if __name__ == "__main__":
    input_file = None   
    ref_list_file = None
    similarity_file = None
    if len(sys.argv) == 4:
        input_file = sys.argv[1]  # Input FASTA file
        ref_list_file = sys.argv[2]  # File containing list of reference IDs
        similarity_file = sys.argv[3]  # Output file for similarity scores
        cli_main()
        sys.exit(1)

    elif len(sys.argv) == 1:        
        main()
        sys.exit(1)
    else:
        print("Usage: python pairwise_similarity.py <input_seqs.fasta> <ref_list_file.txt> <dir/similarity_scores.csv>")
        sys.exit(1)  # Exit if the number of arguments is incorrect

window.mainloop()