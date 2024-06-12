#!/bin/bash

output_file="taxonomy_table.tsv"
echo -e "Species\tKingdom\tPhylum\tClass\tClade\tOrder\tFamily\tGenus" > "$output_file"
#echo -e "Species\tClass\tOrder\tFamily" > "$output_file"

# Read file contents into an array
IFS=$'\n' read -d '' -r -a species_array < "111323_DAMASsbr_ACE2_species.txt"

counter=0

for species in "${species_array[@]}"; do
    ((counter++))
    species=$(echo "$species" | tr -d '\r' | xargs)
    
    echo "Processing $counter: $species"

    {
        tax_data=$(esearch -db taxonomy -query "$species" | \
                   efetch -format xml | \
                   xtract -pattern Taxon -element ScientificName -division LineageEx -group Taxon -sep "|" -element Rank,ScientificName)

        kingdom=$(echo "$tax_data" | grep -o 'kingdom|[^|]*' | tail -n 1)
        phylum=$(echo "$tax_data" | grep -o 'phylum|[^|]*' | tail -n 1)
        class=$(echo "$tax_data" | grep -o 'class|[^|]*' | tail -n 1)
        clade=$(echo "$tax_data" | grep -o 'clade|[^|]*' | tail -n 1)
        order=$(echo "$tax_data" | grep -o 'order|[^|]*' | tail -n 1)
        family=$(echo "$tax_data" | grep -o 'family|[^|]*' | tail -n 1)
        genus=$(echo "$tax_data" | grep -o 'genus|[^|]*' | tail -n 1)

        echo -e "$species\t$kingdom\t$phylum\t$class\t$clade\t$order\t$family\t$genus" >> "$output_file"
#        echo -e "$species\t$class\t$order\t$family" >> "$output_file"
    } || {
        echo "An error occurred with $species"
    }
done

echo "Processed $counter species in total."
