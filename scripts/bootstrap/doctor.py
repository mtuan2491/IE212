"""Report the tools available to this workspace without installing anything."""
import shutil
import subprocess
import sys


def main():
    print(sys.version.split()[0])
    for command in ("git", "java", "mvn", "hdfs", "spark-submit"):
        path = shutil.which(command)
        print(f"{command}: {path or 'not found'}")
    if sys.version_info < (3, 11) or not shutil.which("git"):
        return 2
    subprocess.run(["git", "--version"], check=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
