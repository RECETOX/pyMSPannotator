## MSMetaEnhancer

[![Python package](https://github.com/RECETOX/MSMetaEnhancer/actions/workflows/python-package.yml/badge.svg)](https://github.com/RECETOX/MSMetaEnhancer/actions/workflows/python-package.yml)
[![Python package using Conda](https://github.com/RECETOX/MSMetaEnhancer/actions/workflows/python-package-conda.yml/badge.svg)](https://github.com/RECETOX/MSMetaEnhancer/actions/workflows/python-package-conda.yml)
[![docs](https://readthedocs.org/projects/msmetaenhancer/badge/?version=latest)](https://msmetaenhancer.readthedocs.io/en/latest/)

**MSMetaEnhancer** is a tool used for `.msp` files annotation.
It adds metadata like SMILES, InChI, and CAS number fetched from the following services: [CIR](https://cactus.nci.nih.gov/chemical/structure_documentation), [CTS](https://cts.fiehnlab.ucdavis.edu/), [NLM](https://chem.nlm.nih.gov), and [PubChem](https://pubchem.ncbi.nlm.nih.gov/).
The app uses asynchronous implementation of annotation process allowing for optimal fetching speed.

## Usage

```python
import asyncio

from MSMetaEnhancer import Application

app = Application()

# import your .msp file
app.load_spectra('tests/test_data/sample.msp', file_format='msp')

# curate given metadata (e.g. fix CAS numbers)
app.curate_spectra()

# specify requested services (these are supported)
services = ['CTS', 'CIR', 'NLM', 'PubChem']

# specify requested jobs
jobs = [('name', 'inchi', 'PubChem'), ('inchi', 'formula', 'PubChem'), ('inchi', 'inchikey', 'PubChem'),
        ('inchi', 'iupac_name', 'PubChem'), ('inchi', 'smiles', 'PubChem')]

# run asynchronous annotations of spectra data
asyncio.run(app.annotate_spectra(services, jobs))

# execute without jobs parameter to run all possible jobs
asyncio.run(app.annotate_spectra(services))

# export .msp file 
app.save_spectra('tests/test_data/sample_out.msp', file_format='msp')
```

### Installation

Prerequisites:

- Python 3.7 or 3.8
- Anaconda

Install `MSMetaEnhancer` from Bioconda with:

```
# install MSMetaEnhancer in a new virtual environment to avoid dependency clashes
conda create --name MSMetaEnhancer python=3.8
conda activate MSMetaEnhancer
conda install --channel bioconda --channel conda-forge MSMetaEnhancer
```

### Developer Documentation

#### Setup

Create your development environment using the provided [script](conda/environment-dev.yml) via conda to install all required dependencies.

#### Contributing

We appreciate contributions - feel free to open an issue on our repository, create your own fork, work on the problem and post a PR. 
Please add your contributions to the [changelog](CHANGELOG.md) and to adhere to the [versioning](https://semver.org/spec/v2.0.0.html).

#### Testing

All functionality is tested with the [pytest](https://docs.pytest.org/en/6.2.x/contents.html) framework.
