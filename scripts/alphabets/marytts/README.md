# MaryTTS Alphabet
MaryTTS [http://mary.dfki.de/](http://mary.dfki.de/) provides lexica for different languages.
For every language they defined a set of phones (symbols) in a xml-file.
This can be downloaded from the github repository for a given language (e.g.
[https://github.com/marytts/marytts-lexicon-de](https://github.com/marytts/marytts-lexicon-de)).
In the repository the xml file is called ``allophones.[lang].xml``.
To convert it to an alphabet file:

```sh
# Example for german
python scripts/alphabets/marytts/marytts_xml_to_alphabet.py \
    scripts/alphabets/marytts/de/allophones.de.xml \
    scripts/alphabets/marytts/de/alphabet.json
```
