from pathlib import Path
import shutil
from shutill import resolve_path, safe_copy, is_protected

def cp_command(sourse, destinations, recursive=False):
    try:
        current_dir = Path.cwd()
        source_path = resolve_path(sourse, current_dir)
        dest_path = resolve_path(destinations, current_dir)
        if not is_protected(source_path):
            return f"The path '{source_path}' is protected"
        if is_protected(dest_path) or is_protected(source_path):
            return f"The path '{dest_path}' is protected"
        if dest_path.exists() and dest_path.is_dir():
            dest_path = dest_path / source_path.name
        if source_path.is_file():
            if safe_copy(source_path, dest_path):
                return f"The file '{source_path}' is copied"
            else:
                return f"The file '{source_path}' is not copied"
        elif source_path.is_dir():
            if recursive:
                shutil.copytree(source_path, dest_path)
                return f"The dir '{source_path}' is copied"
            else:
                return f"The dir '{source_path}' is not copied"
        else:
            return f"Unknown object type"
    except Exception as e:
        return str(e)
    except PermissionError:
        return f"Permission error"
    except shutil.SameFileError:
        return f"Same file error"






