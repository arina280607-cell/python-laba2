from pathlib import Path
import shutil


# копирование файлов и каталогов
def cp(shell, args: list[str]):
    if len(args) < 2:  # так как должно быть 2 аргумента: ТО, что копируем и КУЛА
        raise ValueError('Must provide at least 2 arguments')

    recursive = '-r' in args
    sources = [arg for arg in args if arg != 'r']

    destinations = Path(sources.pop())
    sources = [Path(src) for src in sources]

    if not sources:
        raise ValueError('The source is not specified')

    for source in sources:
        if not source.is_absolute():
            source = shell.current_dir / source
        if not source.exists():
            raise FileNotFoundError("Source does not exist")
        if not destinations.is_absolute():
            dest_path = shell.current_dir / destinations
        else:
            dest_path = destinations

        try:
            if source.is_file():
                shutil.copy(source, dest_path)
                print(f'Copied file {source} to {dest_path}')
            elif source.is_dir():
                if recursive:
                    shutil.copy_tree(source, dest_path)
                    print(f'Copied dir {source} to {dest_path}')
                else:
                    raise ValueError('please, use -r')

        except Exception as e:
            raise RuntimeError(e)

    return True
