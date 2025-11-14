#!/usr/bin/env python3
import sys
from lrl.runner import run_text
from lrl.values import Number  # import Number to check null

CODE_END_MARKER = "__LAUREL_END_OF_CODE__"


def read_code_from_stdin():
    lines = []
    for line in sys.stdin:
        if line.rstrip("\n") == CODE_END_MARKER:
            break
        lines.append(line)
    return "".join(lines)


def main():
    # Read code sent via stdin until marker
    code = read_code_from_stdin()

    if not code.strip():
        print("No code provided.")
        return

    # Run Laurel code
    result, error = run_text("<stdin>", code)

    if error:
        # Send the error back through stderr
        print(error.as_string(), file=sys.stderr, flush=True)
    elif result is not None and str(result) != "0":  # ignore Number.null
        print(str(result), flush=True)


if __name__ == "__main__":
    main()
