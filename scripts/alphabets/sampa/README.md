# SAMPA Alphabet

The list of symbols was taken from [https://www.phon.ucl.ac.uk/home/sampa/index.html](https://www.phon.ucl.ac.uk/home/sampa/index.html). The unicode code points were manually extracted (copied) into the json-file ``sampa_symbols_unicode.json``.

Then the alphabet-file is generated using:
```sh
python scripts/alphabets/sampa/create_alphabet_file.py
```
