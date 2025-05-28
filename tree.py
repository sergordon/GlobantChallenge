import os
import sys

def generate_tree(root_dir, prefix="", level=0, max_depth=2):
    if level > max_depth:
        return
    try:
        contents = sorted(os.listdir(root_dir))
    except PermissionError:
        return

    pointers = ['├── '] * (len(contents) - 1) + ['└── ']
    for pointer, name in zip(pointers, contents):
        path = os.path.join(root_dir, name)
        print(prefix + pointer + name)
        if os.path.isdir(path):
            extension = '│   ' if pointer == '├── ' else '    '
            generate_tree(path, prefix + extension, level + 1, max_depth)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python tree.py <path> [max_depth]")
        sys.exit(1)

    root = sys.argv[1]
    max_depth = int(sys.argv[2]) if len(sys.argv) > 2 else 2

    print(os.path.basename(os.path.abspath(root)) + "/")
    generate_tree(root, level=0, max_depth=max_depth)
