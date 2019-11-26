# Conversion

For a mapping first a initial mapping has to be created manually (dict with str -> str).
Then the following scripts can be used to convert the out strings to a list of single symbols.
It furthermore checks which symbols from the input alphabet are not mapped.

```sh
python scripts/conversion/create.py \
    scripts/conversion/ipa_to_xsampa/src.json \
    scripts/conversion/ipa_to_xsampa/map.json \
    scripts/conversion/ipa_to_xsampa/missing.json \
    ipa \
    xsampa
```

If the conversion is from ipa to x, the initial mapping can be created via script.
This only works if the given alphabet contains ipa-references.

```sh
python scripts/conversion/create_ipa_to_x_src_map.py \
    xsampa \
    scripts/conversion/ipa_to_xsampa/src.json
```

## IPA to X-SAMPA
The base map in ``ipa_to_xsampa/src.json`` was taken from [https://github.com/dohliam/xsampa](https://github.com/dohliam/xsampa).
