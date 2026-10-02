"""Configuration file parser for the A-maze-ing maze generator.

Reads key-value parameters from a plain text file,
validates coordinate bounds, parses boolean values and numeric seeds,
produces a strongly-typed configuration
dictionary used to initialize the Maze model.
"""


import sys
from typing import TypedDict


class ParsedConfig(TypedDict):
    """Typed dictionary representing a fully parsed configuration file.

    Attributes:
        WIDTH: Number of horizontal cells in the maze.
        HEIGHT: Number of vertical cells in the maze.
        ENTRY: Tuple of (x, y) coordinates for the entry cell.
        EXIT: Tuple of (x, y) coordinates for the exit cell.
        OUTPUT_FILE: Filesystem destination path for the serialized maze.
        PERFECT: Boolean flag indicating whether the maze has a unique path.
        SEED: Optional integer seed for repeatable random generation.
    """
    WIDTH: int
    HEIGHT: int
    ENTRY: tuple[int, int]
    EXIT: tuple[int, int]
    OUTPUT_FILE: str
    PERFECT: bool
    SEED: int | None


def read_config(path: str | None) -> ParsedConfig:
    """Read and parse a maze configuration file.

    The file must contain one ``KEY=VALUE`` pair per line. Lines starting
    with ``#`` are treated as comments and ignored, as are blank lines.
    Whitespace within a line is stripped before parsing.

    The following keys are mandatory and are parsed/validated into typed
    values:
        WIDTH: Maze width in cells (e.g. ``WIDTH=20``).
        HEIGHT: Maze height in cells (e.g. ``HEIGHT=15``).
        ENTRY: Entry coordinates as ``x,y`` (e.g. ``ENTRY=0,0``).
        EXIT: Exit coordinates as ``x,y`` (e.g. ``EXIT=19,14``).
        OUTPUT_FILE: Path the generated maze will be written to.
        PERFECT: Whether the maze must be perfect, ``True``/``False``.

    The following key is optional:
        SEED: Integer RNG seed for reproducible generation. Defaults to
            ``None`` (random) if not provided.

    Args:
        path: Path to the config file. If falsy, defaults to
            ``"./config.txt"``.

    Returns:
        A dict mapping each mandatory key (plus ``SEED``) to its parsed
        value: ``int`` for WIDTH/HEIGHT/SEED, ``tuple[int, int]`` for
        ENTRY/EXIT, ``str`` for OUTPUT_FILE, ``bool`` for PERFECT, and
        ``None`` for SEED when absent.

    Raises:
        KeyError: If a mandatory key is missing from the file.
        ValueError: If a value is present but malformed (e.g. WIDTH is
            not an integer, ENTRY is not in ``x,y`` form, PERFECT is not
            a recognized boolean string, SEED is not an integer).

    Note:
        If the file itself cannot be opened (not found, permission
        denied, etc.), the error is printed to stderr and parsing
        proceeds against an empty config — which will then raise
        ``KeyError`` on the first mandatory key lookup below.
    """
    if not path:
        path = "./config.txt"
    config: dict[str, str] = {}
    parsed_config: ParsedConfig

    try:
        with open(path, "r") as file:
            for line in file:
                line = line.strip()
                line = line.replace(" ", "")
                if not line or line.startswith("#"):
                    continue

                param, value = line.split("=")
                config[param] = value
    except (FileNotFoundError, FileExistsError, PermissionError) as e:
        print(f"Config file read error: {e}", file=sys.stderr)
        raise

    width = int(config["WIDTH"])
    height = int(config["HEIGHT"])
    entry_coordinates = parse_coord(config["ENTRY"], "ENTRY")
    exit_coordinates = parse_coord(config["EXIT"], "EXIT")
    output_file = config["OUTPUT_FILE"]
    perfect = parse_bool(config["PERFECT"], "PERFECT")
    seed = parse_seed(config)

    parsed_config = {
        "WIDTH": width,
        "HEIGHT": height,
        "ENTRY": entry_coordinates,
        "EXIT": exit_coordinates,
        "OUTPUT_FILE": output_file,
        "PERFECT": perfect,
        "SEED": seed
        }
    return parsed_config


def parse_coord(raw: str, key: str) -> tuple[int, int]:
    """Transforms data from config file into usable data.
    Args:
        raw: The raw string coordinate representation (e.g. '0,0').
        key: The configuration parameter name (e.g. 'ENTRY' or 'EXIT')
        for error messages.

    Returns:
        A tuple of (x, y) coordinates as integers.

    Raises:
        ValueError: If the string does not contain two values
        or if either value cannot be parsed as an integer.
    """
    parts = raw.split(",")
    if len(parts) != 2:
        raise ValueError(f"{key} must be in the form x,y, got: {raw}")
    try:
        x, y = int(parts[0]), int(parts[1])
    except ValueError:
        raise ValueError(f"{key} coordinates must be integers, got: {raw}")
    return (x, y)


def parse_bool(raw: str, key: str) -> bool:
    """Tranforms raw str from config into usable boolian value.
    Args:
        raw: The raw configuration string.
        key: The parameter name for error reporting.

    Returns:
        True or False corresponding to the parsed input.

    Raises:
        ValueError: If the string does not match any recognized
        boolean representation.
    """
    normalized = raw.strip().lower()
    if normalized in ("true", "1", "yes"):
        return True
    if normalized in ("false", "0", "no"):
        return False
    raise ValueError(f"{key} must be True or False, got: {raw}")


def parse_seed(config: dict[str, str]) -> int | None:
    """Parse the optional SEED key into an int, or None if absent.
    Args: config: The parsed config file key/value pairs.
    Returns: The seed as an int, or None if SEED was not provided.
    Raises: ValueError: If SEED is present but not a valid integer.
    """
    raw = config.get("SEED")
    if raw is None:
        return None
    try:
        return int(raw)
    except ValueError:
        raise ValueError(f"SEED must be an integer, got: {raw}")
