import argparse
import string
from itertools import zip_longest


def generate_running_key(primer, length, verbose=False):
    if isinstance(primer, str):
        if not primer.isdigit():
            raise ValueError("Primer must contain only digits.")
        primer = [int(d) for d in primer]

    if length <= len(primer):
        raise ValueError("Length must be greater than the primer.")

    if verbose:
        print("\n[Running Key Generation]")
        print(f"Primer: {''.join(map(str, primer))}")

    while len(primer) < length:
        a, b = primer[-2], primer[-1]
        result = (a + b) % 10
        if verbose:
            print(f"({a} + {b}) % 10 = {result} → {''.join(map(str, primer))}{result}")
        primer.append(result)

    return primer


def generate_mixed_alphabet(keyword, verbose=False):
    keyword = ''.join(dict.fromkeys(keyword.upper()))
    remaining = ''.join(sorted(set(string.ascii_uppercase) - set(keyword)))
    combined = keyword + remaining

    num_cols = len(keyword)
    rows = [combined[i:i+num_cols] for i in range(0, len(combined), num_cols)]

    column_order = sorted(range(num_cols), key=lambda i: keyword[i])
    mixed = ''.join(
        row[i] for i in column_order for row in rows if i < len(row)
    )

    if verbose:
        print("\n[Mixed Alphabet Generation]")
        print(f"Keyword (unique): {keyword}")
        print(f"Remaining letters: {remaining}")
        print("\nTransposition Grid:")
        for row in rows:
            print(' '.join(row))
        print("\nColumn Order:", [keyword[i] for i in column_order])
        print(f"\nMixed Alphabet: {mixed}")

    return mixed


def build_index_map(mixed_alphabet):
    return {char: i for i, char in enumerate(mixed_alphabet)}


def encrypt(plaintext, mixed_alphabet, running_key, verbose=False):
    index_map = build_index_map(mixed_alphabet)
    result = []

    if verbose:
        print("\n[Encryption Steps]")

    for i, (ch, rk) in enumerate(zip(plaintext.upper(), running_key), 1):
        if ch in index_map:
            idx = (index_map[ch] + rk) % 26
            new_ch = mixed_alphabet[idx]
            result.append(new_ch)
            if verbose:
                print(f"{i:>2}: {ch} (index {index_map[ch]}) + {rk} → {idx} → {new_ch}")
        else:
            result.append(ch)
            if verbose:
                print(f"{i:>2}: {ch} (non-alpha) → {ch}")
    return ''.join(result)


def decrypt(ciphertext, mixed_alphabet, running_key, verbose=False):
    index_map = build_index_map(mixed_alphabet)
    alphabet = string.ascii_uppercase
    result = []

    if verbose:
        print("\n[Decryption Steps]")

    for i, (ch, rk) in enumerate(zip(ciphertext.upper(), running_key), 1):
        if ch in index_map:
            idx = (index_map[ch] - rk) % 26
            new_ch = alphabet[idx]
            result.append(new_ch)
            if verbose:
                print(f"{i:>2}: {ch} (index {index_map[ch]}) - {rk} → {idx} → {new_ch}")
        else:
            result.append(ch)
            if verbose:
                print(f"{i:>2}: {ch} (non-alpha) → {ch}")
    return ''.join(result)


def prompt_input(prompt_text, validate_fn, error_msg):
    while True:
        value = input(prompt_text).strip()
        if validate_fn(value):
            return value
        print(f"Invalid input: {error_msg}")


def main():
    parser = argparse.ArgumentParser(description="Delta_JRM's GROMARK Cipher Tool")
    parser.add_argument("-m", "--mode", choices=['encrypt', 'decrypt'], help="Mode: encrypt or decrypt")
    parser.add_argument("-p", "--primer", help="Primer digits (e.g. 12345)")
    parser.add_argument("-k", "--keyword", help="Keyword for generating mixed alphabet (e.g. KEYWORD)")
    parser.add_argument("-t", "--text", help="Plaintext or ciphertext to process")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")

    args = parser.parse_args()

    mode = args.mode or prompt_input("Encrypt or Decrypt? [encrypt/decrypt]: ",
                                     lambda x: x.lower() in ('encrypt', 'decrypt'),
                                     "Must be 'encrypt' or 'decrypt'").lower()

    primer = args.primer or prompt_input("Enter primer digits (e.g. 12345): ",
                                         lambda x: x.isdigit(),
                                         "Primer must contain only digits.")

    keyword = args.keyword or prompt_input("Enter keyword (e.g. KEYWORD): ",
                                           lambda x: x.isalpha(),
                                           "Keyword must be alphabetic.")

    text = args.text or input("Enter the text to process: ").strip().upper()

    if args.verbose:
        verbose = True
    else:
        verbose_input = prompt_input("Enable verbose output? [y/n]: ",
                                     lambda x: x.lower() in ('y', 'n'),
                                     "Please enter 'y' or 'n'.")
        verbose = verbose_input.lower() == 'y'

    mixed_alphabet = generate_mixed_alphabet(keyword, verbose=verbose)
    running_key = generate_running_key(primer, len(text), verbose=verbose)

    if mode == 'encrypt':
        result = encrypt(text, mixed_alphabet, running_key, verbose=verbose)
    else:
        result = decrypt(text, mixed_alphabet, running_key, verbose=verbose)

    print("\n[Final Results]")
    print(f"Mixed Alphabet: {mixed_alphabet}")
    print(f"Running Key   : {''.join(map(str, running_key))}")
    print(f"Input Text    : {text}")
    print(f"Output Text   : {result}")


if __name__ == "__main__":
    main()
