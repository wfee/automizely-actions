import re
import argparse
import os
import json

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--pattern",  help='Regex pattern')
    parser.add_argument("-s", "--text", help='String need to be matched')
    parser.add_argument("-f", "--from_branch", help='From branch')
    parser.add_argument("-t", "--to_branch", help='To branch')
    parser.add_argument("-r", "--rules", help='Rules which branch to branch need to check')
    args = parser.parse_args()

    rules = json.loads(args.rules)

    for rule in rules:
        patternFrom = re.compile(rule["from"])
        patternTo = re.compile(rule["to"])
        if patternFrom.match(args.from_branch) and patternTo.match(args.to_branch):
            pattern = re.compile(args.pattern)
            if pattern.match(args.text):
                print("Passed")
                os._exit(0)
            else:
                print("Filed")
                os._exit(1)

    print("Skipped Check")
    os._exit(0)

