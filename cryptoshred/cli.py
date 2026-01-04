import sys
import argparse
import textwrap
from pathlib import Path

from cryptoshred.files.shredder import shred_file
from cryptoshred.files.verify import verify_file


lethe_epilog = textwrap.dedent("""\
    ---------------------------------------------------------------------------
    "Lethe guarantees future inaccessibility, not retroactive erasure of history."

    Technical Specifications:
      - Algorithm:   AES-GCM (Authenticated Encryption)
      - Paradigm:    Cryptographic Erasure (Crypto-shredding)
      - Strategy:    Irreversible key destruction via memory purging

    Security Advisory:
      Lethe operates on the principle of mathematical finality. By destroying
      the unique encryption key, the target data is rendered computationally
      infeasible to recover, bypassing the limitations of SSD wear-leveling
      and Copy-on-Write (CoW) filesystems.

    Warning:
      Key destruction is instantaneous and irreversible. Ensure all required
      backups are secured before execution. Lethe cannot protect against
      plaintext remnants existing in RAM or swap space prior to execution.
    ---------------------------------------------------------------------------
    For full threat model details, visit: https://github.com/saadiee/lethe
""")


def main():
    parser = argparse.ArgumentParser(
        prog="lethe",
        description="Lethe: Cryptographic erasure via irreversible key destruction.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=lethe_epilog,
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    shred_parser = subparsers.add_parser("shred", help="Encrypt a file and permanently destroy access to the plaintext",)
    shred_parser.add_argument("path", help="Path to the file to shred")

    verify_parser = subparsers.add_parser("verify",help="Verify structural validity of a .lethe encrypted file",)
    verify_parser.add_argument("path", help="Path to the .lethe file to verify")

    args = parser.parse_args()

    try:
        if args.command == "shred":
            encrypted_path = shred_file(Path(args.path))
            print(f"Encrypted file written to: {encrypted_path}")
            sys.exit(0)

        elif args.command == "verify":
            verify_file(Path(args.path))
            print("OK")
            sys.exit(0)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
