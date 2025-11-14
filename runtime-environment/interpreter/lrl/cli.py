import sys
from .runner import run_file


def main():
    if len(sys.argv) != 2:
        print('Usage: lrl <file.lrl>')
        sys.exit(1)
    file_path = sys.argv[1]
    if not file_path.endswith('.lrl'):
        print('Only .lrl files are allowed')
        sys.exit(1)
    value, error = run_file(file_path)
    if error:
        print(error.as_string())
        sys.exit(1)

if __name__ == '__main__':
    main()
