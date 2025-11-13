from pathlib import Path
import shutil
#команда mv перемещение или переименовывание файлов и каталогов
def mv(shell, args):
    if len(args) < 2:
        raise ValueError('Must provide at least two arguments')
    source = Path(args[0])
    destination = Path(args[1])
    if not source.is_absolute():
        source = shell.current_dir / source
    if not destination.is_absolute():
        destination = shell.current_dir / destination
    else:
        dest_path = destination

    if not source.exists():
        raise FileNotFoundError('Source does not exist')
    if dest_path.exists() and dest_path.is_dir():
        final_dest = dest_path / source.name
    else:
        final_dest = dest_path

    try:
        shutil.move(str(source), str(final_dest))
        print(f'moving {source} to {final_dest}')
    except Exception as e:
        raise RuntimeError(f'Error moving {source} to {final_dest}: {e}')
    return True


