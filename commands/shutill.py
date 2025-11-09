from pathlib import Path
import os
import shutil
from datetime import datetime
import sys


# преобразует относительные пути в абсолютные
def resolve_path(path_str: str, current_directory: Path) -> Path:
    if not path_str:
        return current_directory
    path = Path(path_str)

    if not path.is_absolute():
        path = current_directory / path

    try:
        return path.resolve()
    except OSError:
        return path


# форматирование информации о файле для вывода
def format_file(file_path: Path) -> str:
    file_name = file_path.name
    try:
        stat = file_path.stat()
        size = stat.st_size
        mtime = stat.st_mtime

        mtime_str = datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M:%S')
        file_type = 'd' if file_path.is_dir() else 'f'

        if os.access(file_path, os.W_OK):
            permission = "rw-"  # это значит файл доступен для засписи
        else:
            permission = "r--"  # это значит файл доступен только для чтения
        if file_path.is_dir():
            size_str = "DIR"
        else:
            size_str = f"{size:8d}"
        return f'{file_name} {file_type} {size} {mtime_str} {permission}'
    except FileNotFoundError:
        return f'not found {file_path}'
    except PermissionError:
        return f'permission error {file_path}'
    except OSError:
        return f'access error {file_path}'


def is_protected(path: Path) -> bool:
    try:
        absolute_path = path.resolve()
        protected_roots = [
            Path("C:\\"), Path("D:\\"), Path("E:\\"), Path("F:\\"),
            Path.home().root,
            Path.cwd().root
        ]

        protected_paths = [
            Path('C:\\Windows'),
            Path('C:\\Program Files'),
            Path('C:\\Program Files (x86)'),
            Path('C:\\System32'),
            Path.home() / 'AppData',
        ]

        if absolute_path in protected_roots:
            return True
        for protected in protected_paths:
            try:
                if protected.exists() and absolute_path.is_relative_to(protected):
                    return True
            except OSError:
                continue
        return False

    except OSError:
        return True
def safe_copy(src: Path, dest: Path) -> bool:
    try:
        if not src.exists():
            return False
        if is_protected(src) or is_protected(dest):
            return False
        shutil.move(str(src), str(dest))
        return True
    except OSError:
        return False
def safe_remove(src: Path) -> bool:
    try:
        if not src.exists():
            return False
        if is_protected(src):
            return False
        if src.is_file():
            path.unlink(missing_ok=True)
        elif src.is_dir():
            shutil.rmtree(str(src))
        return True
    except OSError:
        return False
def get_disk(path: Path) -> dict:
    try:
        usage = shutil.disk_usage(path)
        return {
            'total': usage.total,
            'used': usage.used,
            'free': usage.free,
            'total_gb': usage.total//1024**3,
            'free_gb': usage.free//1024**3,
            'used_gb': usage.used//1024**3 ,
        }
    except OSError:
        return {}

