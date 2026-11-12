import sys

sys.dont_write_bytecode = True
from gate import task_cli


if __name__ == "__main__":
    raise SystemExit(task_cli("input"))
