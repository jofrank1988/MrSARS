import sys
import re
from Bio import SeqIO

def main(input_fasta, output_fasta):
    seen_sequences = {}
    species_regex = re.compile(r'([A-Z][a-z]+(?:_[a-z]+)+)')

    for record in SeqIO.parse(input_fasta, "fasta"):
        header = record.description
        sequence = str(record.seq)

        # Try to extract species name from header using regex
        species_match = species_regex.search(header)
        if species_match:
            species = species_match.group(1)
        else:
            print(f"Warning: Unable to extract species from header: {header}")
            continue

        # Initialize species dictionary if not present
        if species not in seen_sequences:
            seen_sequences[species] = {}
        
        # Store unique sequences with their original headers
        if sequence not in seen_sequences[species]:
            seen_sequences[species][sequence] = record

    # Write retained sequences to output file
    with open(output_fasta, "w") as output_handle:
        for species_records in seen_sequences.values():
            for record in species_records.values():
                SeqIO.write(record, output_handle, "fasta")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py input.fasta output.fasta")
        sys.exit(1)
    
    input_fasta = sys.argv[1]
    output_fasta = sys.argv[2]
    main(input_fasta, output_fasta)
    print("Process completed. Unique and first instance of duplicate sequences retained.")
