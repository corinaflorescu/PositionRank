# PositionRank

An Unsupervised Approach to Keyphrase Extraction from Scholarly Documents

### Usage

```
$PositionRank --input_data data/KDD/docs/ --input_gold data/KDD/docs/
```
--input_data : directory with text documents to extract the keyphrases for
--input_gold: directory with text documents containing the annotations for each file in the input data (if you want to evaluate)
The full list of command line options is available with $PositionRank --help

### Installation
```
cd PositionRank
pip install -r requirements.txt
python setup.py install
```

### Citing
If you find PositionRank useful in your research, we ask that you cite the following paper:

```
@inproceedings{florescu2017positionrank,
  title={Positionrank: An unsupervised approach to keyphrase extraction from scholarly documents},
  author={Florescu, Corina and Caragea, Cornelia},
  booktitle={Proceedings of the 55th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)},
  volume={1},
  pages={1105--1115},
  year={2017}
}
```

