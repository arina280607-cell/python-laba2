
from pathlib import Path
from logger import logg, log_command

class Minishell:
    def __init__(self):
        self.commands= {} #словарь для команд(название и что выполняет)
        self.plugins = {} #словарь для плагинов
        self.current_dir=Path.cwd() #текцщая директория
        self.logger = logg() #логгер для записи действий
    def baza_komand(self, name:str, function):
        self.commands[name] = function #функция добавления команд
    def baza_plugins(self, name:str, plugins):
        self.plugins[name] = plugins

    def preobr(self, user_input:str):
        return user_input.strip().split() #разделяет команду на части для обработки
    def show_promt(self):
        current_path = str(self.current_dir).replace("\\", "/")#так как \n, например, питон воспримет как начало новой строки
        return f"{current_path}: "

    def proverka_vipoln(self, command_name:str, arguments):
        if command_name in self.commands:
            command_function = self.commands[command_name]
        elif command_name in self.plugins:
            command_function = self.plugins[command_name]
        else:
            print(f"unknown command:{command_name}")
            log_command(self.logger, f'{command_name} {' '.join(arguments)}', success=False, error_message=f"unknown command:{command_name}")
            return False
        try:
            result = command_function(self, arguments)
            log_command(self.logger, f"{command_name}{' '.join(arguments)}", success=True)
            return result
        except Exception as e:
            print(f"error: {e}")
            log_command(self.logger, f"{command_name}{' '.join(arguments)}", success=False, error_message=str(e))
            return False
    def start(self):
        print("Hello! To exit, enter 'exit'")
        print("Enter the command:")
        while True:
            try:
                user_input = input(self.show_promt())
                if not user_input.strip():
                    continue
                if user_input.lower() == "exit":
                    print("Goodbye!")
                    break
                parts = self.preobr(user_input)
                command_name = parts[0].lower()
                arguments = parts[1:]
                self.proverka_vipoln(command_name, arguments)
            except KeyboardInterrupt:
                print("Goodbye!")
                break
            except Exception as e:
                print(f"Error: {e}")
