import json
import click

import pyphony


@click.command()
@click.argument('in_path', type=click.Path(exists=True))
@click.argument('out_path', type=click.Path())
@click.argument('report_path', type=click.Path())
@click.argument('in_alphabet',
                type=click.Choice(['ipa', 'sampa', 'xsampa', 'marytts_de']))
@click.argument('out_alphabet',
                type=click.Choice(['ipa', 'sampa', 'xsampa', 'marytts_de']))
def run(in_path, out_path, report_path, in_alphabet, out_alphabet):
    with open(in_path, 'r') as f:
        in_map = json.load(f)

    src_abc = pyphony.Alphabet.with_name(in_alphabet)
    target_abc = pyphony.Alphabet.with_name(out_alphabet)

    out_map = []
    mapped_symbols = set()
    report = {
        'not_mapped': [],
    }

    for k, v in in_map.items():
        in_sym = src_abc.decode(k)
        out_sym = target_abc.decode(v)

        if len(in_sym) == 1:
            mapped_symbols.add(in_sym[0])

        out_map.append((in_sym, out_sym))

    report['not_mapped'] = list(
        set(src_abc.symbols.keys()) - set(in_map.keys())
    )

    with open(out_path, 'w') as f:
        json.dump(out_map, f, ensure_ascii=False, indent=1)

    with open(report_path, 'w') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)


if __name__ == '__main__':
    run()
