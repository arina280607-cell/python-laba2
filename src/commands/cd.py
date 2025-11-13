from pathlib import Path
import os

#команда cd - смена директории
def cd(shell, args: list[str]) -> bool:
    if not args:
        home_dir = Path.home()
    else:
        target = args[0]

        if target == "~":
            new_path = Path.home()
        elif target == "..":
            new_path = shell.current_dir.parent
        else:
            new_path = Path(target)
            if not new_path.is_absolute():
                new_path = shell.current_dir/new_path
    if not new_path.exists():
        raise FileNotFoundError(f"Directory {new_path} does not exist")
    if not new_path.is_dir():
        raise NotADirectoryError(f"{new_path} not a directory")
    os.chdir(new_path)
    shell.current_dir = Path.cwd()

    print(f"Current working directory: {shell.current_dir}")
    return True


