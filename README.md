# protScraper
Author: Max Stritzinger

Generates list of related proteins based on an NCBI GeneID

# Usage

    git clone https://github.com/maxstr/protScraper.git
    cd protScraper
    ./initialize.sh
    source bin/activate
    ./protScraper geneID destination

# Requirements:

- Python

This will place an a.txt with related 3D proteins and their chains in the destination directory.
