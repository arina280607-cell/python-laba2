from pathlib import Path
from shutill import resolve_path
import os

#команда cd - смена директории
def cd_command(args: list, current_dir: Path) -> Path:
    if not args:
        home_dir = Path.home()
        os.chdir(home_dir)
        return home_dir
    target = args[0]

    if target == "~":
        home_dir = Path.home()
        os.chdir(home_dir)
        return home_dir
    elif target == "..":
        new_dir = current_dir.parent
        os.chdir(new_dir)
        return new_dir
    else:
        target_path = resolve_path(target, current_dir)
        if target_path.is_dir() and target_path.exists():
            os.chdir(target_path)
            return target_path
        else:
            print(f"cd: {target}: Not a directory")
            return None

