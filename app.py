import os
import json
from glob import glob
import argparse

def not_dirs(files):
    return filter(lambda x: not os.path.isdir(x), files)

def not_markdown(files):
    return filter(lambda x: not x.lower().endswith('.md'), files)

def not_current(files):
    return filter(lambda x: x != __file__, files)

def not_hidden(files):
    return filter(lambda x: not any(part.startswith('.') for part in x.split(os.sep)), files)

def norm(files):
    return map(os.path.normpath, files)

def filter_files(files):
    files = norm(files)
    files = not_dirs(files)
    files = not_markdown(files)
    files = not_current(files)
    files = list(files)
    return files

def scan_files():
    cur_dir = os.path.dirname(__file__)
    files = glob(f'{cur_dir}/**', recursive=True)
    files = filter_files(files)
    return files

def main(output):
    files = scan_files()

    context = []
    for file_path in files:
        with open(file_path, 'r') as f:
            context.append({'Path': file_path.strip(), 'Content': f.read().strip()})

    with open(output, 'w') as f:
        json.dump(context, f, indent=3)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Collect scripts context.')
    parser.add_argument('output', type=str, help='Output context file path')
    args = parser.parse_args()
    main(args.output)
