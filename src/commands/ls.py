from pathlib import Path
import stat
from datetime import datetime


# реализация команды ls - список файлов и каталогов
def ls(shell, args):
    options = [arg for arg in args if arg.startswith('-')]  # список аргументов
    paths = [arg for arg in args if not arg.startswith('-')]  # пути к файлам, папкам
    if paths:  # проверяем есть ли пути
        target_path = Path(args[0])
        if not target_path.is_absolute():
            target_path = shell.current_dir / target_path  # преобр относительный в абсолютный
    else:
        target_path = shell.current_dir  # если путей нет, используем текущ директорию
    if not target_path.exists():
        raise FileNotFoundError(f'{target_path} does not exist')
    if not target_path.is_dir():
        raise NotADirectoryError(f'{target_path} is not a directory')

    detailed = "-l" in options

    try:
        items = list(target_path.iterdir())  # возвращает все элементы директории
    except PermissionError:  # если нет доступа к чтению
        raise PermissionError(f'There is no access to the catalog: {target_path}')

    items.sort(key=lambda i: (i.is_file(), i.name.lower()))

    if detailed:
        print(f'Content of {target_path}:')
        print('-'*50)
        for item in items:
            try:
                stat_info = item.stat()
                mode = stat_info.st_mode
                permission = 'd' if item.is_dir() else '-'
                permission += 'r' if mode & stat.S_IREAD else '-'
                permission += 'w' if mode & stat.S_IWRITE else '-'
                permission += 'x' if mode & stat.S_IEXEC else '-'

                size = stat_info.st_size
                mtime = datetime.fromtimestamp(stat_info.st_mtime)
                mtime_str = mtime.strftime('%Y-%m-%d %H:%M:%S')

                print(f"{permission} {size:8d} {mtime_str} {item.name}")
            except PermissionError:
                print(f'There is no access to the catalog: {item.name}')
    else:
        for item in items:
            print(item.name)

    return True
