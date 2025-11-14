# LRL - Little Runtime Language

A tiny interpreted language with variables, arithmetic, strings, lists, conditionals, loops, functions, and a few built-ins.

## Features
- Variables and arithmetic: `+ - * / ^`
- Strings with escapes `\n` and `\t`
- Lists: `[1, 2, 3]`
- Comparisons and logic: `== != < > <= >= and or not`
- Control flow: `if/elif/else ... end`, `for ... then ... end`, `while ... then ... end`
- Functions: `fun name(arg1, arg2) -> expr` or multi-line bodies ending with `end`
- Built-ins: `say(...)`, `get_int(prompt)`, `get_float(prompt)`, `get_string(prompt)`

## Quick start

Requirements: Python 3.9+

From the repo root:

```bash
# Option A: Run via module (recommended)
python3 -m lrl.cli path/to/file.lrl

# Option B: Call from Python
python3 - <<'PY'
from lrl.runner import run_text
code = 'say("Hello", "LRL!")'
val, err = run_text('<stdin>', code)
if err:
    print(err.as_string())
PY
```

## Language basics

```lrl
# variables
num1 = 1
num2 = 2
name = "John"

# printing
say("Hello World")
say(name)
say(num1 + num2)

# conditionals
if num1 is 1 then
  say("Hello", name)
else if num1 is 2 then
  say("Goodbye", name)
end

# loops
for i = 0 repeat 10 times then
  say(i)
end

# input
num = get_int("Enter number: ")
flt = get_float("Enter float: ")
word = get_string("Enter word: ")

# functions
fun greet(who)
  say("Hi", who)
end

greet(name)
```

Notes:
- Use `then` after `if`/`for`/`while` conditions.
- Use `end` to close compound statements.
- `is` is an equality alias.

### Interactive example

When running inside the Electron host, Laurel programs can pause for user input. For example:

```lrl
say("Interactive sum")
x = get_int("Enter first number: ")
y = get_int("Enter second number: ")
say("Total:", x + y)
```

Each `get_*` call asks the frontend for input, displays the prompt in a modal, and resumes execution once the user responds.

## Running the provided sample

A sample program is included at `sample.lrl`.

```bash
printf "1\n2.5\nhello\n" | python3 -m lrl.cli sample.lrl
```

Expected output (prompts may be adjacent due to piping):

```text
Hello World
John
3
Hello John
0
1
2
3
4
5
6
7
8
9
Enter number: Enter float: Enter word: This is a function
done
```

## Errors
On syntax or runtime errors, LRL shows a caret-highlighted snippet with file and line numbers.

## Project layout
- `lrl/lexer.py`: Turns source into tokens
- `lrl/parser.py`: Builds an AST
- `lrl/nodes.py`: AST node types
- `lrl/interpreter.py`: Walks the AST to execute
- `lrl/values.py`: Runtime values and built-ins
- `lrl/runtime.py`: Result tracking and symbol tables
- `lrl/errors.py`: Error types and formatting
- `lrl/cli.py`: Command-line interface
- `sample.lrl`: Example program

## Packaging (optional)
If you want an `lrl` command, create a virtualenv and install this package in editable mode, then run via `python -m lrl.cli` or add a console entry point.

```bash
python -m venv .venv
. .venv/bin/activate
pip install -e .
```
