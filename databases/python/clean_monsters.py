import re
from argparse import ArgumentParser
from fractions import Fraction
from json import dump, dumps, load
from pathlib import Path
from sys import stdout
from typing import Any, Callable, cast

from loguru import logger


def set_up_arg_parser():
    """Sets up the cmd line argument parser"""
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


def convert(v, f: Callable[[Any], str]):
    """
    Tries to call f on the input value. Printing the before and after or an error message if it failed. returns the
    input value if it failed
    """
    p_str = v
    r_value = v
    try:
        r_value = f(v)
    except ValueError:
        logger.error(f"Value: `{v}` can not be converted")
    logger.debug(f"{p_str} -> {r_value}")
    return r_value


def default_parser(v):
    """Used to ignore type or when type can not be converted"""
    return v


@logger.catch
def parse_ac(v: str):
    """Parse armor class field"""
    try:
        r = int(v)
    except ValueError:
        values = v.split(" ")[0].split(",")
        return parse_ac(values[0])
    return r


def parse_frac(v: str):
    """Parse strings that could be a fraction"""
    fraction = r"\d+\/\d+"
    if re.match(fraction, v):
        return float(Fraction(v))
    return float(v)


parsers: dict[str, dict[str, Callable]] = {
    "Challenge_Rating": {"str": parse_frac, "float": default_parser},
    "Armor_Class": {"str": parse_ac, "int": default_parser},
    "Hitpoints": {"str": int, "int": default_parser},
    "Initiative": {"str": parse_frac, "int": default_parser},
    "Creature_Tags": {"str": str.title},
    "Alignment": {"str": str.title},
}


if __name__ == "__main__":
    args = set_up_arg_parser().parse_args()
    verbose = args.verbose
    vverbose = args.vv
    path = Path(args.input)
    level = "DEBUG"
    if not (verbose or vverbose):
        logger.disable(__name__)
    elif verbose:
        level = "INFO"
    elif vverbose:
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
            for k, value in fields.items():
                if k not in parsers:
                    continue
                if isinstance(value, list):
                    fields[k] = [
                        convert(val, parsers[k][type(val).__name__]) for val in value
                    ]
                else:
                    parser = parsers[k].get(
                        type(verbose).__name__,
                        parsers[k].get("default", default_parser),
                    )
                    fields[k] = convert(value, parser)
    output_path = args.output
    if output_path:
        output_path = Path(output_path)
        try:
            with open(output_path, "w") as of:
                dump(monsters, of, indent=4)
        except OSError as e:
            logger.error(f"Unable to open output file `{output_path}`")
    elif args.inplace:
        with open(path, "w") as of:
            dump(monsters, of, indent=4)
    else:
        print(dumps(monsters))
