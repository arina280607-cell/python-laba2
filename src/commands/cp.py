from pathlib import Path
import shutil


# копирование файлов и каталогов
def cp(shell, args: list[str]):
    if len(args) < 2:  # так как должно быть 2 аргумента: ТО, что копируем и КУЛА
        raise ValueError('Must provide at least 2 arguments')

    recursive = False
    sources = []

    for arg in args:
        if arg == '-r':
            recursive = True
        else:
            sources.append(arg)
    if len(sources)<2:
        raise ValueError('Must provide at least 1 source')
    destination = Path(sources.pop())
    sources = [Path(src) for src in sources]

    for source in sources:
        if not source.is_absolute():
            source_path = shell.current_dir / source
        else:
            source_path = source

        if not destination.is_absolute():
            dest_path = shell.current_dir / destination
        else:
            dest_path = destination

        if not source_path.exists():
            raise FileNotFoundError(f"Source {source_path} does not exist")

        try:
            if source_path.is_file():
                # Если destination - директория, копируем файл в нее
                if dest_path.exists() and dest_path.is_dir():
                    final_dest = dest_path / source_path.name
                else:
                    final_dest = dest_path
                shutil.copy2(source_path, final_dest)
                print(f'Copied file {source_path} to {final_dest}')
            elif source_path.is_dir():
                if recursive:
                    # Если destination существует и это директория, копируем внутрь
                    if dest_path.exists() and dest_path.is_dir():
                        final_dest = dest_path / source_path.name
                    else:
                        final_dest = dest_path
                    shutil.copytree(source_path, final_dest)
                    print(f'Copied directory {source_path} to {final_dest}')
                else:
                    raise ValueError('Use -r to copy directories')
        except Exception as e:
            raise RuntimeError(f"Error copying {source_path} to {dest_path}: {e}")

    return True
