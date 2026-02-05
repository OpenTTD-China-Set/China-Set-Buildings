#!/usr/bin/env python
import grf
import argparse
from house.lib.docgen import gen_docs
from house.lib.parameters import parameter_list
from house.houses.test.houses import houses


def get_string_manager():
    s = grf.StringManager()
    s.import_lang_dir("house/lang", default_lang_file="english-uk.lng")

    return s


def gen(args):
    s = get_string_manager()
    g = grf.NewGRF(
        grfid=b"__\03\06",
        name=s["STR_GRF_NAME"],
        description=s["STR_GRF_DESC"],
        version=0,
        min_compatible_version=0,
        id_map_file="house/id_map.json",
        sprite_cache_path="house/.cache",
        url="https://www.tt-forums.net/viewtopic.php?t=91092",
        strings=s,
        preferred_blitter=grf.NewGRF.BLITTER_BPP_32,
    )

    g.add(
        grf.ComputeParameters(
            target=0x40,
            operation=0x00,
            if_undefined=False,
            source1=0x11,
            source2=0xFE,
            value=b"\xff\xff\x00\x00",
        )
    )

    g.add_int_parameter(
        name=s["STR_PARAM_VANILLA"],
        description=s["STR_PARAM_VANILLA_DESC"],
        default=0,
        limits=(0, 1),
        enum={0: s["STR_PARAM_VANILLA_DISABLED"], 1: s["STR_PARAM_VANILLA_ENABLED"]},
    )
    g.add(
        grf.If(is_static=True, variable=0, condition=0x02, value=1, skip=1, varsize=4)
    )
    g.add(
        grf.DefineMultiple(
            feature=grf.HOUSE, first_id=0, props={"substitute": [0xFF] * 0x6E}
        )
    )

    parameter_list.add(g, s)
    for house in houses:
        g.add(house)

    g.write("building.grf")


def docs(args):
    gen_docs(get_string_manager(), houses)


def main():
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(required=True)

    gen_parser = subparsers.add_parser("gen")
    gen_parser.set_defaults(func=gen)

    doc_parser = subparsers.add_parser("doc")
    doc_parser.set_defaults(func=docs)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
