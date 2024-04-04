"""This script is kept for compatibility. Use evalplus.sanitize if possible."""

from evalplus.sanitize import main

if __name__ == "__main__":
    from fire import Fire

    Fire(main)
