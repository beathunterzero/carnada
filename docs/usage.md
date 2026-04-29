# CARNADA Usage Guide

`carnada` is a local-first command-line tool for generating secure passwords and checking existing passwords from the terminal.

This guide explains the main usage modes, available profiles, command options, and practical examples.

---

# Requirements

`carnada` requires:

```text
Python 3.10 or higher
```

No external dependencies are required.

The tool uses only the Python standard library.

---

# Running the Tool

From the project directory, run:

```bash
python3 carnada.py
```

On Windows PowerShell:

```powershell
python carnada.py
```

On Linux, WSL, or macOS, you can optionally make the script executable:

```bash
chmod +x carnada.py
./carnada.py
```

---

# Basic Password Generation

Generate one secure password using the default profile:

```bash
python3 carnada.py
```

Example output:

```text
CARNADA — Secure Password Generator
------------------------------------------
Password : V7#kQm92@tLx8pRz
Profile  : strong
Length   : 18
Charset  : 82 characters
Entropy  : ~114.44 bits
Rating   : very strong
```

By default, `carnada` uses the `strong` profile.

---

# Custom Password Length

Use `-l` or `--length` to define a custom length.

```bash
python3 carnada.py -l 24
```

Equivalent command:

```bash
python3 carnada.py --length 24
```

Example output:

```text
CARNADA — Secure Password Generator
------------------------------------------
Password : N9#rVx28@LmQ7sKpT4zW!a
Profile  : strong
Length   : 24
Charset  : 82 characters
Entropy  : ~152.59 bits
Rating   : very strong
```

---

# Generation Profiles

Profiles provide predefined settings for different usage scenarios.

Use a profile with:

```bash
python3 carnada.py --profile <profile_name>
```

Available profiles:

```text
strong
legacy
pin
hex
wifi
```

---

## strong

Default profile for general use.

Uses:

```text
uppercase letters
lowercase letters
numbers
symbols
```

Example:

```bash
python3 carnada.py --profile strong
```

---

## legacy

Compatible profile for restrictive or older systems.

Uses:

```text
uppercase letters
lowercase letters
numbers
```

Does not use symbols.

Example:

```bash
python3 carnada.py --profile legacy
```

This profile is useful when a system rejects special characters or has older password policy restrictions.

---

## pin

Numeric profile.

Uses:

```text
numbers only
```

Example:

```bash
python3 carnada.py --profile pin
```

You can also define a custom PIN length:

```bash
python3 carnada.py --profile pin -l 8
```

---

## hex

Hexadecimal token profile.

Uses:

```text
0123456789abcdef
```

Example:

```bash
python3 carnada.py --profile hex
```

This profile is useful for labs, technical testing, or workflows that require hexadecimal values.

---

## wifi

Long and compatible Wi-Fi password profile.

Uses:

```text
uppercase letters
lowercase letters
numbers
```

Example:

```bash
python3 carnada.py --profile wifi
```

This profile avoids complex symbols to make manual typing easier on phones, routers, smart TVs, consoles, and IoT devices.

---

# Generate Multiple Passwords

Use `-c` or `--count` to generate more than one password.

```bash
python3 carnada.py --count 5
```

Equivalent command:

```bash
python3 carnada.py -c 5
```

Example output:

```text
CARNADA — Secure Password Generator
------------------------------------------
Profile  : strong
Count    : 5
Length   : 18
Entropy  : ~114.44 bits each
Rating   : very strong
------------------------------------------
1. V7#kQm92@tLx8pRz
2. B4!sKp81@TxQ9mVw
3. M8#qLn73@RvX2pZa
4. K5@wTr49#LpQ8nXs
5. Z9!vMc61@HsT3qRb
```

This is useful when you need several temporary credentials or want to choose from multiple generated options.

---

# Quiet Mode

Quiet mode prints only the generated password.

Use:

```bash
python3 carnada.py --quiet
```

Equivalent command:

```bash
python3 carnada.py -q
```

Example output:

```text
V7#kQm92@tLx8pRz
```

Quiet mode is useful for shell scripting.

Example:

```bash
PASSWORD=$(python3 carnada.py --quiet)
```

Use this carefully. Passwords stored in shell variables may still be exposed through logs, debugging output, or later commands.

---

# JSON Output

Use `--json` to print structured output.

```bash
python3 carnada.py --json
```

Example output:

```json
{
  "profile": "strong",
  "count": 1,
  "length": 18,
  "charset_size": 82,
  "entropy_bits": 114.44,
  "rating": "very strong",
  "passwords": [
    "V7#kQm92@tLx8pRz"
  ]
}
```

JSON output is useful for automation or integration with other tools.

Avoid redirecting real passwords into files unless you understand the risk.

Example to avoid with sensitive credentials:

```bash
python3 carnada.py --json > password.json
```

This creates a plaintext file containing the generated password.

---

# Character Group Options

`carnada` allows disabling specific character groups.

Available options:

```text
--no-upper
--no-lower
--no-numbers
--no-symbols
```

Examples:

Generate a password without symbols:

```bash
python3 carnada.py --no-symbols
```

Generate a password with only lowercase letters and numbers:

```bash
python3 carnada.py --no-upper --no-symbols
```

Generate a password without numbers:

```bash
python3 carnada.py --no-numbers
```

At least one character group must remain enabled.

---

# Ambiguous Characters

By default, `carnada` avoids visually ambiguous characters.

Examples:

```text
O
0
I
1
l
o
```

This makes generated passwords easier to read and type manually.

To allow ambiguous characters, use:

```bash
python3 carnada.py --allow-ambiguous
```

This may slightly increase the available character set.

---

# Password Check Mode

`carnada` can check an existing password locally.

Use:

```bash
python3 carnada.py check
```

The tool will ask for the password using hidden input.

Example:

```text
Password to check:
```

This is the recommended method because the password is not passed directly through the shell command.

Example output:

```text
CARNADA — Password Check
------------------------------------------
Length          : 12
Uppercase       : yes
Lowercase       : yes
Numbers         : yes
Symbols         : yes
Ambiguous chars : yes
Entropy         : ~78.66 bits
Rating          : strong
```

---

# Checking a Password from the Command Line

You can also provide the password directly as an argument:

```bash
python3 carnada.py check "Password123!"
```

This is less recommended for real sensitive passwords because it may be stored in shell history or visible through process inspection.

Use this form mainly for testing, examples, or non-sensitive values.

---

# JSON Output in Check Mode

Use `--json` with `check` mode:

```bash
python3 carnada.py check --json
```

Example output:

```json
{
  "length": 12,
  "uppercase": true,
  "lowercase": true,
  "numbers": true,
  "symbols": true,
  "ambiguous_chars": true,
  "entropy_bits": 78.66,
  "rating": "strong"
}
```

You can also check a provided value:

```bash
python3 carnada.py check "Password123!" --json
```

---

# Help Menu

To display the main help menu:

```bash
python3 carnada.py --help
```

To display help for generate mode:

```bash
python3 carnada.py generate --help
```

To display help for check mode:

```bash
python3 carnada.py check --help
```

---

# Version

To display the tool version:

```bash
python3 carnada.py --version
```

Example output:

```text
carnada 1.0.0
```

---

# Common Usage Patterns

Generate a strong password:

```bash
python3 carnada.py
```

Generate a longer password:

```bash
python3 carnada.py -l 32
```

Generate a password for a restrictive system:

```bash
python3 carnada.py --profile legacy
```

Generate a Wi-Fi-friendly password:

```bash
python3 carnada.py --profile wifi
```

Generate a numeric PIN:

```bash
python3 carnada.py --profile pin -l 6
```

Generate a hexadecimal token:

```bash
python3 carnada.py --profile hex
```

Generate multiple candidates:

```bash
python3 carnada.py --count 10
```

Use output in a shell variable:

```bash
PASSWORD=$(python3 carnada.py --quiet)
```

Check a password safely using hidden input:

```bash
python3 carnada.py check
```

---

# Recommended Practices

Use the default `strong` profile for general passwords.

Use `legacy` only when a system rejects symbols.

Use `wifi` when the password must be typed manually on multiple devices.

Use `check` mode without passing real sensitive passwords directly as command-line arguments.

Use `--quiet` carefully in scripts.

Avoid redirecting generated passwords into plaintext files.

Store long-term credentials in a dedicated password manager.

---

# Exit Behavior

`carnada` runs, prints the requested output, and exits.

It does not keep a background process running.

It does not store generated passwords.

It does not create logs.

It does not require internet access.

---

# Troubleshooting

## Python command not found

Try:

```bash
python carnada.py
```

or:

```bash
python3 carnada.py
```

depending on your operating system and Python installation.

---

## Permission denied when running `./carnada.py`

Give the script execution permissions:

```bash
chmod +x carnada.py
```

Then run:

```bash
./carnada.py
```

---

## Invalid profile

Use one of the available profiles:

```text
strong
legacy
pin
hex
wifi
```

Example:

```bash
python3 carnada.py --profile strong
```

---

## No character groups enabled

This can happen if all character groups are disabled:

```bash
python3 carnada.py --no-upper --no-lower --no-numbers --no-symbols
```

At least one character group must remain enabled.

---

# Summary

`carnada` provides a simple local workflow:

```text
generate passwords;
check passwords;
estimate entropy;
print clean terminal output;
avoid storing secrets.
```

It is designed to be small, practical, and safe for local terminal use.