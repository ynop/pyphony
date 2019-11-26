import json
import click

import pyphony


@click.command()
@click.argument('alphabet',
                type=click.Choice(['ipa', 'sampa', 'xsampa', 'marytts_de']))
@click.argument('out_path', type=click.Path())
@click.option('--reverse', is_flag=True)
def run(alphabet, out_path, reverse):
    abc = pyphony.Alphabet.with_name(alphabet)

    out_map = {}

    for symbol in abc.symbols.values():
        if symbol.ipa_counterpart is not None:
            if reverse:
                out_map[symbol.value] = symbol.ipa_counterpart
            else:
                out_map[symbol.ipa_counterpart] = symbol.value

    with open(out_path, 'w') as f:
        json.dump(out_map, f, ensure_ascii=False, indent=1)


if __name__ == '__main__':
    run()
