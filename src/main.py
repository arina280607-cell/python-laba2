import os
from pathlib import Path
from src.commands.ls import ls
from src.commands.cd import cd
from src.commands.cat import cat
from src.commands.cp import cp
from src.commands.mv import mv
from src.commands.rm import rm
from src.minishell import Minishell
#настраиваем нашу оболлчку, функция регестрирует все наши созданные команды
def setup_shell():
    print("Setting up shell")
    shell = Minishell()
    all_commands = {
        'ls': ls, #просмотр файлов и папок
        'cd': cd, #смена директроии
        'cat': cat, #просмотр содержимого файла
        'cp': cp, #копированине файла
        'rm': rm, #удаление файлов
        'mv': mv, #перемещение файлов
    }
    print('Available commands:')
    for command_name, command_function in all_commands.items():
        shell.baza_komand(command_name, command_function)
        print(f"{command_name}")
    print('Minishell is ready to work')
    return shell

def main():
    try:
        shell = setup_shell()
        shell.start()
    except KeyboardInterrupt:
        print("Shutting down")
    except Exception as error:
        print(error)
if __name__ == '__main__':
    main()
