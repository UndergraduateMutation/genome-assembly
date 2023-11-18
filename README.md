# Genome assembly

### Setting up
1. Create a virtual environment
```sh
python -m venv venv
```

2. Activate the virtual environment
```sh
source venv/bin/activate
```

3. Install the dependencies
```sh
pip install -r requirements.txt
```

### Usage
1. Assemble contigs from the reads
```sh
python src/genome-assembly/main.py --reads <read-file_path> --target <output-file-path>
```

For more information about plotting the graph and other parameters, run:
```sh
python src/genome-assembly/main.py --help
```

2. Visualize the generated contigs
```sh
python src/visualization/visualize_contigs.py --file <contigs-file-path>
```

3. Measure the Blast score
Use the [NCBI](https://blast.ncbi.nlm.nih.gov/Blast.cgi) website or the blast command line tool

4. Generate reads from a genome
```sh
python src/data-generation/main.py -g <genome-file-path> -t <output-file-path> -r <read-size> -e <error-probability>
```
