from argparse import ArgumentParser
from json import dump, dumps, load
from pathlib import Path
from sys import stdout
from typing import Any, Callable, cast

from loguru import logger


def set_up_parser():
    parser = ArgumentParser(
        prog="clean_monsters",
        description="Clean monsters.json generatored by running monsters-1668973282154.json though jq with monsters.jq as the filters",
    )
    parser.add_argument("input")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-o", "--output")
    group.add_argument(
        "-i",
        "--inplace",
        help="Cleans file in place. WARNING: this will overwrite the input file",
        action="store_true",
    )
    parser.add_argument(
        "-v", "--verbose", help="Info level verbosity", action="store_true"
    )
    parser.add_argument("-vv", help="Debug level verbosity", action="store_true")
    return parser


def convert(value, f: Callable[[Any], str]):
    p_str = value
    try:
        value = f(value)
    except ValueError:
        logger.error(f"Value: `{value}` can not be converted")
    logger.debug(f"{p_str} -> {value}")
    return value


default_parser = lambda v: v


parsers: dict[str, dict[str, Callable]] = {
    "Challenge_Rating": {"str": float, "float": default_parser},
    "Armor_Class": {"str": int},
    "Hitpoints": {"str": int},
    "Initiative": {"str": int},
    "Creature_Tags": {"str": str.title},
    "Alignment": {"str": str.title},
}


if __name__ == "__main__":
    args = set_up_parser().parse_args()
    v = args.verbose
    vv = args.vv
    path = Path(args.input)
    level = "DEBUG"
    if not (v or vv):
        logger.disable(__name__)
    elif v:
        level = "INFO"
    elif vv:
        level = "DEBUG"

    logger.configure(
        handlers=[{"sink": stdout, "format": "<blue>{message}</blue>", "level": level}]
    )
    monsters: dict = {"error": "error"}
    with open(path) as monsters_f:
        monsters = load(monsters_f)
        for monster in monsters:
            monster = cast(dict, monster)
            fields = monster.get("fields")
            for k, v in fields.items():
                if k not in parsers:
                    continue
                match v:
                    case [*values]:
                        fields[k] = [
                            convert(value, parsers[k][type(value).__name__])
                            for value in values
                        ]
                    case value:
                        try:
                            fields[k] = convert(v, parsers[k][type(v).__name__])
                        except KeyError as e:
                            logger.info(f"{k} has no parsing option for {e}")
                            fields[k] = convert(v, default_parser)
    output_path = args.output
    if output_path:
        output_path = Path(output_path)
        try:
            with open("  " + output_path, "w") as of:
                dump(monsters, of, indent=4)
        except (TypeError, OSError) as e:
            # TODO: make red
            logger.error("Unable to open output file")
    elif args.inplace:
        with open(path, "w") as of:
            dump(monsters, of, indent=4)
    else:
        print(dumps(monsters))
