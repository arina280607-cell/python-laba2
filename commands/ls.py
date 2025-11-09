from pathlib import Path
from shutill import resolve_path, format_file

#реализация команды ls - список файлов и каталогов
def ls_command(args: list, current_dir: Path) -> str:
    detailed = False
    target_dir = current_dir
    for arg in args:
        if arg == "-1" or arg == "-l":
            detailed = True
        else:
            target_dir = resolve_path(arg, current_dir)

    if not target_dir.exists():
        return f"The path '{target_dir}' does not exist"
    if target_dir.is_file():
        if detailed:
            return format_file(target_dir)
        else:
            return target_dir.name

    try:
        files = list(target_dir.iterdir())
        if not files:
            return f"The path '{target_dir}' is empty"

        files.sort()

        if detailed:
            result=[]
            for file in files:
                result.append(format_file(file))
            return result
        else:
            return [file.name for file in files]

    except PermissionError:
        return f"{target_dir} is not a directory"
    except FileNotFoundError:
        return f"{target_dir} does not exist"


