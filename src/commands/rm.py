from pathlib import Path
import shutil
# команда rm- удаление файлов и директорий
def rm(shell, args):
    if not args:
        raise RuntimeError('No arguments provided')
    recursive = False
    targets = []

    for arg in args:
        if arg == '-r':
            recursive = True
        else:
            targets.append(Path(arg))
    if not targets:
        raise RuntimeError('No targets provided')

    for target in targets:
        if not target.is_absolute():
            target_path = shell.current_dir / target
        else:
            target_path = target

        if not target_path.exists():
            raise FileNotFoundError(f'Target file {target_path} does not exist')
        if target_path.is_dir():
            if not recursive:
                raise RuntimeError('please, use -r to remove')

            response = input(f'Remove {target_path}? [Y/N] ')
            if response.lower() == 'n':
                print('ok! file remines')

            try:
                shutil.rmtree(target_path)
                print(f'Successfully removed {target_path}')
            except Exception as e:
                raise RuntimeError(f'Error removing {target_path}: {e}')
        else:
            try:
                target_path.unlink()
                print(f'Successfully removed {target_path}')
            except Exception as e:
                raise RuntimeError(f'Error removing {target_path}: {e}')
    return True
