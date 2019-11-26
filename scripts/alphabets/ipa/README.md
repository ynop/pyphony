# IPA Alphabet

The list of symbols was taken from [https://www.internationalphoneticassociation.org](https://www.internationalphoneticassociation.org/sites/default/files/phonsymbol.pdf). The unicode code points were manually extracted (copied) into the json-file ``ipa_symbols_unicode.json``.
Entries without a hex value were ignored.

Errors corrected manually:
* In vowels 2050 changed to 0250
* In pulmonic-consonants 0067 to 0066

Then the alphabet-file is generated.
```sh
python scripts/alphabets/ipa/create_alphabet_file.py
```
