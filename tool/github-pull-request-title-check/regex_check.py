import re
import argparse
import os

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--pattern",  help='Regex pattern')
    parser.add_argument("-s", "--text", help='String need to be matched')
    args = parser.parse_args()
    pattern = re.compile(args.pattern)
    if pattern.match(args.text):
        os._exit(0)
    else:
        os._exit(1)
