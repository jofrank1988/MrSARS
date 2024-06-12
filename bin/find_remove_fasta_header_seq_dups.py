# Import necessary modules from BioPython and sys
from Bio import SeqIO
import sys

# Define a function to remove duplicate sequences based on headers and sequence lengths
def remove_duplicate_sequences(input_fasta, output_fasta, min_length, max_length, seq_type):
    # Check if the sequence type is valid, raise an error if not
    if seq_type not in ["nucleotide", "protein"]:
        raise ValueError("Invalid sequence type. Please choose 'nucleotide' or 'protein'.")

    # Initialize a dictionary to keep track of seen sequences
    seen = {}
    # Initialize a list to store unique records
    unique_records = []

    # Open the input fasta file for reading
    with open(input_fasta, "r") as file:
        # Iterate over each sequence record in the fasta file
        for record in SeqIO.parse(file, "fasta"):
            # Get the length of the sequence
            seq_length = len(record.seq)
            # Check if the sequence length is within the specified range
            if min_length <= seq_length <= max_length:
                # Create a unique identifier for each sequence based on its header and sequence
                identifier = (record.id, str(record.seq))
                # If this sequence has not been seen before, add it to the dictionary and list
                if identifier not in seen:
                    seen[identifier] = True
                    unique_records.append(record)

    # Open the output fasta file for writing
    with open(output_fasta, "w") as output:
        # Write the unique records to the output file
        SeqIO.write(unique_records, output, "fasta")

# Check if the script is being run as the main module
if __name__ == "__main__":
    # Check if the correct number of command line arguments have been provided
    if len(sys.argv) != 6:
        # If not, print the usage information and exit
        print("Usage: python script.py <input_fasta> <output_fasta> <min_length> <max_length> <seq_type>")
        sys.exit(1)

    # Get the input fasta file path from command line arguments
    input_fasta = sys.argv[1]
    # Get the output fasta file path from command line arguments
    output_fasta = sys.argv[2]
    # Get the minimum sequence length from command line arguments and convert it to an integer
    min_length = int(sys.argv[3])
    # Get the maximum sequence length from command line arguments and convert it to an integer
    max_length = int(sys.argv[4])
    # Get the sequence type from command line arguments and convert it to lower case
    seq_type = sys.argv[5].lower()
    # Call the function to remove duplicate sequences
    remove_duplicate_sequences(input_fasta, output_fasta, min_length, max_length, seq_type)
    # Print a completion message
    print(f"Done. Duplicate sequences with duplicate headers removed. {seq_type.capitalize()} sequences shorter than {min_length} or longer than {max_length} bases were filtered out.")
