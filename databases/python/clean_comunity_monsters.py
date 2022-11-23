from argparse import ArgumentParser
from json import dump, dumps, load
from pathlib import Path
from sys import stdout
from typing import cast

from loguru import logger


def set_up_parser():
    parser = ArgumentParser(
        prog="clean monsters",
        description="Clean monsters.json generatored by running monsters-1668973282154.json though jq with monsters.jq as the filters",
    )
    parser.add_argument("input")
    parser.add_argument("-o", "--output")
    parser.add_argument("-v", "--verbose", action="store_true")
    return parser


tag_path = Path("")

anti_patterns = ["model"]
patterns = ["Creature_Tags", "Alignment"]


def convert(value):
    p_str = value
    value = str.title(value)
    logger.debug(f"{p_str} -> {value}")
    return value


if __name__ == "__main__":
    args = set_up_parser().parse_args()
    verbose = args.verbose
    path = Path(args.input)
    if not verbose:
        logger.disable(__name__)
    logger.configure(handlers=[{"sink": stdout, "format": "<blue>{message}</blue>"}])
    monsters: dict = {"error": "error"}
    with open(path) as monsters_f:
        monsters = load(monsters_f)
        for monster in monsters:
            monster = cast(dict, monster)
            fields = monster.get("fields")
            for k, v in fields.items():
                if k in anti_patterns:
                    continue
                if k not in patterns:
                    continue
                match v:
                    case [*values]:
                        fields[k] = list(map(convert, values))
                    case value:
                        fields[k] = convert(value)
    output_path = args.output
    if output_path:
        output_path = Path(output_path)
        with open(output_path, "w") as of:
            dump(monsters, of, indent=4)
    else:
        print(dumps(monsters))
