#!/usr/bin/env python3
"""
carnada - Local-first CLI password generator and password checker.

Genera contraseñas seguras usando aleatoriedad criptográfica.
No guarda secretos, no cifra archivos y no envía datos a internet.
"""

from __future__ import annotations

import argparse
import json
import math
import secrets
import string
import sys
from dataclasses import dataclass
from getpass import getpass


APP_NAME = "carnada"
APP_VERSION = "1.0.0"

MIN_LENGTH = 8
DEFAULT_LENGTH = 18

UPPERCASE = string.ascii_uppercase
LOWERCASE = string.ascii_lowercase
NUMBERS = string.digits
SYMBOLS = "!@#$%^&*()-_=+[]{};:,.<>/?"

AMBIGUOUS_CHARS = set("O0I1lo")


@dataclass(frozen=True)
class Profile:
    name: str
    description: str
    length: int
    use_upper: bool
    use_lower: bool
    use_numbers: bool
    use_symbols: bool
    allow_ambiguous: bool = False


PROFILES: dict[str, Profile] = {
    "strong": Profile(
        name="strong",
        description="Uso general con letras, números y símbolos.",
        length=18,
        use_upper=True,
        use_lower=True,
        use_numbers=True,
        use_symbols=True,
    ),
    "legacy": Profile(
        name="legacy",
        description="Compatible con sistemas antiguos: letras y números.",
        length=16,
        use_upper=True,
        use_lower=True,
        use_numbers=True,
        use_symbols=False,
    ),
    "pin": Profile(
        name="pin",
        description="PIN numérico.",
        length=6,
        use_upper=False,
        use_lower=False,
        use_numbers=True,
        use_symbols=False,
        allow_ambiguous=True,
    ),
    "hex": Profile(
        name="hex",
        description="Token hexadecimal.",
        length=32,
        use_upper=False,
        use_lower=False,
        use_numbers=True,
        use_symbols=False,
        allow_ambiguous=True,
    ),
    "wifi": Profile(
        name="wifi",
        description="Contraseña larga y compatible para redes Wi-Fi.",
        length=24,
        use_upper=True,
        use_lower=True,
        use_numbers=True,
        use_symbols=False,
    ),
}


def remove_ambiguous(chars: str) -> str:
    """Elimina caracteres visualmente ambiguos."""
    return "".join(char for char in chars if char not in AMBIGUOUS_CHARS)


def get_charset_groups(
    use_upper: bool,
    use_lower: bool,
    use_numbers: bool,
    use_symbols: bool,
    allow_ambiguous: bool,
    profile_name: str | None = None,
) -> list[str]:
    """Construye los grupos de caracteres activos."""

    if profile_name == "hex":
        return ["0123456789abcdef"]

    groups: list[str] = []

    if use_upper:
        groups.append(UPPERCASE if allow_ambiguous else remove_ambiguous(UPPERCASE))

    if use_lower:
        groups.append(LOWERCASE if allow_ambiguous else remove_ambiguous(LOWERCASE))

    if use_numbers:
        groups.append(NUMBERS if allow_ambiguous else remove_ambiguous(NUMBERS))

    if use_symbols:
        groups.append(SYMBOLS)

    return [group for group in groups if group]


def calculate_entropy(length: int, charset_size: int) -> float:
    """Calcula entropía aproximada en bits."""
    if length <= 0 or charset_size <= 1:
        return 0.0

    return length * math.log2(charset_size)


def rate_entropy(entropy_bits: float) -> str:
    """Clasifica la fortaleza según entropía aproximada."""
    if entropy_bits < 40:
        return "weak"
    if entropy_bits < 70:
        return "moderate"
    if entropy_bits < 100:
        return "strong"

    return "very strong"


def generate_password(
    length: int,
    groups: list[str],
) -> str:
    """
    Genera una contraseña garantizando al menos un carácter
    de cada grupo activo.
    """
    if not groups:
        raise ValueError("Debe existir al menos un grupo de caracteres activo.")

    if length < MIN_LENGTH:
        length = MIN_LENGTH

    if length < len(groups):
        raise ValueError(
            f"La longitud mínima para los grupos seleccionados es {len(groups)}."
        )

    all_chars = "".join(groups)

    password_chars = [secrets.choice(group) for group in groups]

    remaining_length = length - len(password_chars)
    password_chars.extend(secrets.choice(all_chars) for _ in range(remaining_length))

    secrets.SystemRandom().shuffle(password_chars)

    return "".join(password_chars)


def analyze_password(password: str) -> dict[str, object]:
    """Evalúa una contraseña localmente."""
    length = len(password)

    has_upper = any(char.isupper() for char in password)
    has_lower = any(char.islower() for char in password)
    has_number = any(char.isdigit() for char in password)
    has_symbol = any(char in SYMBOLS for char in password)
    has_ambiguous = any(char in AMBIGUOUS_CHARS for char in password)

    charset_size = 0

    if has_upper:
        charset_size += len(UPPERCASE)
    if has_lower:
        charset_size += len(LOWERCASE)
    if has_number:
        charset_size += len(NUMBERS)
    if has_symbol:
        charset_size += len(SYMBOLS)

    entropy = calculate_entropy(length, charset_size)

    return {
        "length": length,
        "uppercase": has_upper,
        "lowercase": has_lower,
        "numbers": has_number,
        "symbols": has_symbol,
        "ambiguous_chars": has_ambiguous,
        "entropy_bits": round(entropy, 2),
        "rating": rate_entropy(entropy),
    }


def format_bool(value: bool) -> str:
    return "yes" if value else "no"


def print_generation_result(
    password: str,
    profile: str,
    charset_size: int,
    entropy_bits: float,
    quiet: bool,
    as_json: bool,
) -> None:
    """Imprime el resultado de generación."""

    if quiet:
        print(password)
        return

    payload = {
        "password": password,
        "profile": profile,
        "length": len(password),
        "charset_size": charset_size,
        "entropy_bits": round(entropy_bits, 2),
        "rating": rate_entropy(entropy_bits),
    }

    if as_json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return

    print(f"{APP_NAME.upper()} — Secure Password Generator")
    print("-" * 42)
    print(f"Password : {password}")
    print(f"Profile  : {profile}")
    print(f"Length   : {len(password)}")
    print(f"Charset  : {charset_size} characters")
    print(f"Entropy  : ~{round(entropy_bits, 2)} bits")
    print(f"Rating   : {rate_entropy(entropy_bits)}")


def print_check_result(result: dict[str, object], as_json: bool) -> None:
    """Imprime el resultado del análisis de contraseña."""

    if as_json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return

    print(f"{APP_NAME.upper()} — Password Check")
    print("-" * 42)
    print(f"Length          : {result['length']}")
    print(f"Uppercase       : {format_bool(bool(result['uppercase']))}")
    print(f"Lowercase       : {format_bool(bool(result['lowercase']))}")
    print(f"Numbers         : {format_bool(bool(result['numbers']))}")
    print(f"Symbols         : {format_bool(bool(result['symbols']))}")
    print(f"Ambiguous chars : {format_bool(bool(result['ambiguous_chars']))}")
    print(f"Entropy         : ~{result['entropy_bits']} bits")
    print(f"Rating          : {result['rating']}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog=APP_NAME,
        description="Local-first CLI password generator and password checker.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  python carnada.py\n"
            "  python carnada.py -l 24\n"
            "  python carnada.py --profile legacy\n"
            "  python carnada.py --count 5\n"
            "  python carnada.py --quiet\n"
            "  python carnada.py --json\n"
            "  python carnada.py check\n"
            "  python carnada.py check \"Password123!\"\n"
        ),
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"{APP_NAME} {APP_VERSION}",
    )

    subparsers = parser.add_subparsers(dest="command")

    generate_parser = subparsers.add_parser(
        "generate",
        help="Generate secure passwords.",
    )

    add_generate_arguments(generate_parser)

    check_parser = subparsers.add_parser(
        "check",
        help="Check password strength locally.",
    )

    check_parser.add_argument(
        "password",
        nargs="?",
        help="Password to check. If omitted, it will be requested securely.",
    )

    check_parser.add_argument(
        "--json",
        action="store_true",
        help="Print output as JSON.",
    )

    add_generate_arguments(parser)

    return parser


def add_generate_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--profile",
        choices=sorted(PROFILES.keys()),
        default="strong",
        help="Password generation profile. Default: strong.",
    )

    parser.add_argument(
        "--length",
        "-l",
        type=int,
        default=None,
        help="Password length. Overrides profile default.",
    )

    parser.add_argument(
        "--count",
        "-c",
        type=int,
        default=1,
        help="Number of passwords to generate. Default: 1.",
    )

    parser.add_argument(
        "--no-upper",
        action="store_true",
        help="Exclude uppercase letters.",
    )

    parser.add_argument(
        "--no-lower",
        action="store_true",
        help="Exclude lowercase letters.",
    )

    parser.add_argument(
        "--no-numbers",
        action="store_true",
        help="Exclude numbers.",
    )

    parser.add_argument(
        "--no-symbols",
        action="store_true",
        help="Exclude symbols.",
    )

    parser.add_argument(
        "--allow-ambiguous",
        action="store_true",
        help="Allow ambiguous characters such as O, 0, I, 1, l and o.",
    )

    parser.add_argument(
        "--quiet",
        "-q",
        action="store_true",
        help="Print only the generated password.",
    )

    parser.add_argument(
        "--json",
        action="store_true",
        help="Print output as JSON.",
    )


def run_generate(args: argparse.Namespace) -> int:
    profile = PROFILES[args.profile]

    length = args.length if args.length is not None else profile.length

    use_upper = profile.use_upper and not args.no_upper
    use_lower = profile.use_lower and not args.no_lower
    use_numbers = profile.use_numbers and not args.no_numbers
    use_symbols = profile.use_symbols and not args.no_symbols

    allow_ambiguous = args.allow_ambiguous or profile.allow_ambiguous

    if args.count < 1:
        print("Error: --count must be greater than 0.", file=sys.stderr)
        return 1

    if length < MIN_LENGTH and args.profile != "pin":
        print(
            f"Warning: minimum recommended length is {MIN_LENGTH}. "
            f"Using {MIN_LENGTH}.",
            file=sys.stderr,
        )
        length = MIN_LENGTH

    groups = get_charset_groups(
        use_upper=use_upper,
        use_lower=use_lower,
        use_numbers=use_numbers,
        use_symbols=use_symbols,
        allow_ambiguous=allow_ambiguous,
        profile_name=args.profile,
    )

    if not groups:
        print("Error: at least one character group must be enabled.", file=sys.stderr)
        return 1

    charset_size = len(set("".join(groups)))
    entropy_bits = calculate_entropy(length, charset_size)

    passwords = [generate_password(length, groups) for _ in range(args.count)]

    if args.json:
        payload = {
            "profile": args.profile,
            "count": args.count,
            "length": length,
            "charset_size": charset_size,
            "entropy_bits": round(entropy_bits, 2),
            "rating": rate_entropy(entropy_bits),
            "passwords": passwords,
        }
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return 0

    if args.quiet:
        for password in passwords:
            print(password)
        return 0

    if args.count == 1:
        print_generation_result(
            password=passwords[0],
            profile=args.profile,
            charset_size=charset_size,
            entropy_bits=entropy_bits,
            quiet=False,
            as_json=False,
        )
        return 0

    print(f"{APP_NAME.upper()} — Secure Password Generator")
    print("-" * 42)
    print(f"Profile  : {args.profile}")
    print(f"Count    : {args.count}")
    print(f"Length   : {length}")
    print(f"Entropy  : ~{round(entropy_bits, 2)} bits each")
    print(f"Rating   : {rate_entropy(entropy_bits)}")
    print("-" * 42)

    for index, password in enumerate(passwords, start=1):
        print(f"{index:02d}. {password}")

    return 0


def run_check(args: argparse.Namespace) -> int:
    password = args.password

    if password is None:
        password = getpass("Password to check: ")

    if not password:
        print("Error: password cannot be empty.", file=sys.stderr)
        return 1

    result = analyze_password(password)
    print_check_result(result, as_json=args.json)

    return 0


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "check":
        return run_check(args)

    return run_generate(args)


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        print("\nInterrupted by user.", file=sys.stderr)
        raise SystemExit(130)