import string
import re
import xml.etree.ElementTree as ET

from tqdm import tqdm

import pyphony


DE_IPA_PATTERN = re.compile(r'\{\{IPA\}\} \{\{Lautschrift\|(.*?)\}\}')
DE_TITLE_PATTERN = re.compile(r'== (.*?) \(\{\{Sprache\|(.*?)\}\}\) ==')
DE_WORD_CHARS = list(string.ascii_lowercase)
DE_WORD_CHARS.extend(['ö', 'ü', 'ä'])


class WiktionaryParser:

    def __init__(self, valid_characters, ipa_pattern, title_lang_pattern):
        self.ns = {
            'mn': 'http://www.mediawiki.org/xml/export-0.10/'
        }
        self.valid_characters = valid_characters
        self.ipa_pattern = ipa_pattern
        self.title_lang_pattern = title_lang_pattern

    def parse_xml_dump(self, path):
        tree = ET.parse(path)
        root = tree.getroot()

        print('Get all pages')
        pages = root.findall('./mn:page', self.ns)

        print('Parse pages')
        result = []

        for page in tqdm(pages, total=len(pages)):
            res = self.parse_page(page)

            if res is not None:
                result.append(res)

        print('Filter results')
        result = self.filter_entries(result)
        print('Found {} pronunciations'.format(len(result)))

        print('Create lexicon')
        lex = pyphony.Lexicon()

        for word, transcription in result:
            lex.add(word, [transcription])

        return lex

    def parse_page(self, page):
        title = page.find('mn:title', self.ns).text.lower().strip()
        text = page.find('mn:revision/mn:text', self.ns).text

        if text is None or title is None:
            return

        if type(text) != str:
            return

        title_2, lang, pron = self.find_page_text_elements(text)

        if title_2 is None or lang is None or pron is None:
            return

        if title_2 != title:
            return

        words = [w.strip() for w in title.split(' ')]
        transcripts = [p.strip() for p in pron.split(' ')]

        if len(words) != len(transcripts):
            return

        return (title, lang, list(zip(words, transcripts)))

    def find_page_text_elements(self, text):
        pronunciation = None
        m = self.ipa_pattern.search(text)

        if m is not None:
            pronunciation = m.group(1)

        title = None
        lang = None
        m = self.title_lang_pattern.search(text)

        if m is not None:
            title = m.group(1).lower().strip()
            lang = m.group(2).lower().strip()

        return title, lang, pronunciation

    def filter_entries(self, entries):
        result = []

        for entry in tqdm(entries):
            res = self.filter_entry(
                entry[0],
                entry[1],
                entry[2]
            )

            if res is not None:
                result.extend(res)

        return result

    def filter_entry(self, title, lang, words):
        if ':' in title:
            # Ignore pages with titles like:
            # Vorlage: Lit-Duden
            # Wiktionary:Deutsche ...
            return

        if lang.lower() != 'deutsch':
            return

        filtered_words = []

        for word, transcript in words:
            res = self.filter_transcript(word, transcript)
            if res is not None:
                filtered_words.append((word, transcript))

        return filtered_words

    def filter_transcript(self, word, transcript):
        if len(transcript) <= 0:
            return

        for c in word:
            if c not in self.valid_characters:
                return

        return (word, transcript)


class DeWiktionaryParser(WiktionaryParser):

    def __init__(self):
        super(DeWiktionaryParser, self).__init__(
            DE_WORD_CHARS,
            DE_IPA_PATTERN,
            DE_TITLE_PATTERN
        )
