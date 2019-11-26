import click
import json
import xml.etree.ElementTree as ET


@click.command()
@click.argument('xml_path', type=click.Path(exists=True))
@click.argument('out_path', type=click.Path())
def run(xml_path, out_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()
    symbols = {}

    for c in root:
        if c.tag in ['silence', 'vowel', 'consonant']:
            ph = c.attrib['ph']

            if 'ipa' in c.attrib:
                ipa = c.attrib['ipa']
            else:
                ipa = None

            symbols[ph] = {
                'ipa': ipa
            }

    symbols["'"] = {
        'ipa': 'ˈ'
    }

    abc = {
        'symbols': symbols,
        'ignore': ['-', ','],
    }

    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(abc, f, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    run()
