#!/usr/bin/env python3
"""Split a migration file into numbered statements. Synthetic fixture script."""
import sys


def split(text):
    out = []
    for chunk in text.split(";"):
        chunk = chunk.strip()
        if chunk:
            out.append(chunk)
    return out


def main():
    text = sys.stdin.read()
    for i, stmt in enumerate(split(text), 1):
        print(f"[{i}] {stmt}")


if __name__ == "__main__":
    main()
