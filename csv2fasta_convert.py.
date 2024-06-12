import csv

input_file = 'pnas_2010146117_sd01_ACE2_sbr_acc.csv'  # Replace with your CSV file path
output_file = 'pnas_2010146117_sd01_ACE2_sbr_acc.fasta'  # Output file name

with open(input_file, newline='') as csvfile, open(output_file, 'w') as fastafile:
    reader = csv.reader(csvfile)
    for row in reader:
        species_name = row[0]
        sequence = ''.join(row[1:26])
        identifier = row[26]
        fasta_header = f'>{identifier}_{species_name}'
        fastafile.write(f'{fasta_header}\n{sequence}\n')

print(f'FASTA file created: {output_file}')
