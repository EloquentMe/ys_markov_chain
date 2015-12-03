import sys
from generator import collect, generate


def main():
    filename = 'db.json'
    collect(sys.stdin, filename)
    generate(sys.stdout, filename)

if __name__ == '__main__':
    main()
