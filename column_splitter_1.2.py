import csv
import re
import sys

def split_accession_species(s):
    # Find the pattern of a digit followed by an underscore and a capital letter
    match = re.search(r'\d_([A-Z])', s)
    if match:
        # Split the string at the found index and only keep the part starting from the capital letter
        index = match.start(1)
        species_name = s[index:]
    else:
        species_name = s

    # Remove '_Damas2020' if present
    return species_name.replace('_Damas2020', '')

def process_file(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w', newline='') as outfile:
        reader = csv.reader(infile, delimiter='\t')
        writer = csv.writer(outfile, delimiter='\t')

        for i, row in enumerate(reader):
            if i == 0:
                # For the header row, add a new column title
                row.append('Species')
            else:
                # Split the first column based on the pattern and remove '_Damas2020' if present
                species_name = split_accession_species(row[0])
                row.append(species_name)
            writer.writerow(row)
    print(f'File has been processed and saved as {output_file}')

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script_name.py input_file.tsv")
    else:
        input_file = sys.argv[1]
        output_file = 'modified_' + input_file
        process_file(input_file, output_file)
