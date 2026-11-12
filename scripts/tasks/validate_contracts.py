from gate import InvalidContract, load_registry


if __name__ == "__main__":
    try:
        tasks = load_registry()
    except InvalidContract as exc:
        print(f"FAIL: {exc}")
        raise SystemExit(1)
    print(f"PASS: {len(tasks)} contracts and dependency graph")
