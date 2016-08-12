#! usr/bin/env python3
import argparse
import os.path
import compiler

def main():
    parser = argparse.ArgumentParser(description="Compiles a forth program into a .sb2")
    parser.add_argument("source", help="The forth source file")
    parser.add_argument("-o", "--output", help="Destination of the output.")
    args = parser.parse_args()
    source = args.source
    out = args.output or os.path.splitext(source)[0] + ".sb2"
    with open(source) as fin:
        compiler.compile_code(fin.read(), out)

if __name__ == '__main__':
    main()
