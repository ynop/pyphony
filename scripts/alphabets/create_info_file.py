import click
import json
import unicodedata


@click.command()
@click.argument('in_path', type=click.Path(exists=True))
@click.argument('out_path', type=click.Path())
@click.option(
    '--encoding',
    default='unicode',
    type=click.Choice(['unicode', 'ascii'], case_sensitive=False)
)
def run(in_path, out_path, encoding):
    with open(in_path, 'r') as f:
        data = json.load(f)

    groups = {}

    for k, v in data.items():
        phones = []

        for code in v:
            sym = {}

            if encoding == 'ascii':
                sym['symbol'] = chr(int(code, 10))
                sym['ascii'] = code
            else:
                sym['symbol'] = chr(int(code, 16))
                sym['hex'] = code

            sym['name'] = unicodedata.name(sym['symbol'])

            phones.append(sym)
            groups[k] = phones

    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(groups, f, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    run()
