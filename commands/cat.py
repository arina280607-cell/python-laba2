from pathlib import Path
from shutill import resolve_path

def cat_command(args: list, current_dir: Path) -> Path:
    if not args:
        print("cat: missing file")
        return False
    file_path = resolve_path(args[0], current_dir)

    if not(file_path.exists()):
        print("cat: {file_path}: No file in directory")
        return False
    if file_path.is_dir():
        print("cat: {file_path}: Is a directory")
        return False

    try:
        with file_path.open("r") as file:
            inform=file.read()
            print(inform)
            return True
            return inform
    except PermissionError:
        print("cat: {file_path}: permission error")
    except UnicodeDecodeError:
        print("cat: {file_path}: can't read file")
    except Exception as e:
        print("cat: {file_path}: {e}")


