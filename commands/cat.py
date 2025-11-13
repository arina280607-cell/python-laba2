from pathlib import Path
#выводим водержимое файла в консоль
def cat(shell, args:list[str]) -> bool:
    if not args:
        raise ValueError('File not specified')

    file_path = Path(args[0])
    if not file_path.is_absolute():
        file_path=shell.current_dir/file_path

    if not file_path.exists():
        raise ValueError('File not found')
    if file_path.is_dir():
        raise IsADirectoryError("It is not a file, a directory")

    try:
        with open(file_path, 'r') as file:
            content = file.read()
            print(content)
    except UnicodeDecodeError:
        print(f'The file {file_path} is not a text file')

    return True


