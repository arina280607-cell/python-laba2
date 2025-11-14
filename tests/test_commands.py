import os
import tempfile
import shutil
from pathlib import Path
import sys
from unittest.mock import patch

sys.path.append(str(Path(__file__).parent.parent / 'src'))#путь к исходному коду

from src.commands.ls import ls
from src.commands.cd import cd
from src.commands.cat import cat
from src.commands.cp import cp
from src.commands.mv import mv
from src.commands.rm import rm
from src.minishell import Minishell


class TestMinishellFixed:
    def setup_method(self):
        #cоздаем временную директорию для тестов
        self.test_dir = tempfile.mkdtemp() #создание временной папки
        self.original_dir = os.getcwd() #сохр текущую директорию
        os.chdir(self.test_dir) #передод во временную папку

        #cоздаем тестовые файлы и папки
        self.test_file1 = Path("test1.txt")
        self.test_file2 = Path("test2.txt")
        self.test_dir1 = Path("test_dir")
        #создаем файлики с каким-то содержимым
        with open(self.test_file1, 'w') as f:
            f.write("Hello, World!")

        with open(self.test_file2, 'w') as f:
            f.write("Test content")

        self.test_dir1.mkdir()#тестовая директория

        #cоздаем shell для тестов
        self.shell = Minishell()
        self.shell.current_dir = Path(self.test_dir)

    def teardown_method(self):
        #очищаем после тестов
        os.chdir(self.original_dir)#возврат в исх директорию
        try:
            shutil.rmtree(self.test_dir)#удаляем временную папку
        except PermissionError:
            pass
    #тест команды ls
    def test_ls_basic(self):
        result = ls(self.shell, [])
        assert result == True
    def test_ls_detailed(self):
        result = ls(self.shell, ['-l'])
        assert result == True
    def test_ls_specific_path(self):
        result = ls(self.shell, ['.'])
        assert result == True

    #тест команды cd
    def test_cd_basic(self):
        original_dir = self.shell.current_dir
        result = cd(self.shell, ['test_dir'])#переход в папку
        assert result == True
        assert self.shell.current_dir != original_dir#проверяем сменилась ли наша директория
    def test_cd_home(self): #~
        result = cd(self.shell, ['~'])
        assert result == True
    def test_cd_parent(self): #..
        original_dir = self.shell.current_dir
        result = cd(self.shell, ['..'])
        assert result == True
        assert self.shell.current_dir == original_dir.parent #проверка что перешли на уровень выше

    #тест команды cat
    def test_cat_basic(self):
        result = cat(self.shell, ['test1.txt'])
        assert result == True
    def test_cat_nonexistent(self):
        try:
            cat(self.shell, ['nonexistent.txt'])
            assert False, "Should have raised an error"
        except ValueError as e:
            assert "File not found" in str(e)

    #тест команды cp
    def test_cp_file(self):
        result = cp(self.shell, ['test1.txt', 'test1_copy.txt'])
        assert result == True
        assert Path('test1_copy.txt').exists()
    def test_cp_directory(self):
        test_file = self.test_dir1 / "inner.txt"#создаеи файл в тестовой директории
        with open(test_file, 'w') as f:
            f.write("Inner file")
        result = cp(self.shell, ['-r', 'test_dir', 'test_dir_copy'])
        assert result == True
        assert Path('test_dir_copy').exists()
        assert (Path('test_dir_copy') / "inner.txt").exists()

    #тест команды mv
    def test_mv_file(self):
        result = mv(self.shell, ['test1.txt', 'test1_moved.txt'])
        assert result == True
        assert not Path('test1.txt').exists()
        assert Path('test1_moved.txt').exists()
    def test_mv_to_directory(self):
        result = mv(self.shell, ['test1.txt', 'test_dir'])
        assert result == True
        assert not Path('test1.txt').exists()
        assert (self.test_dir1 / 'test1.txt').exists()

    def test_rm_file(self):
        result = rm(self.shell, ['test1.txt'])
        assert result == True
        assert not Path('test1.txt').exists()

    @patch('builtins.input', return_value='y')  # Мокаем input чтобы автоматически отвечать 'y'
    def test_rm_directory(self, mock_input):
        # cоздаем файл в тестовой директории
        test_file = self.test_dir1 / "inner.txt"
        with open(test_file, 'w') as f:
            f.write("Inner file")

        result = rm(self.shell, ['-r', 'test_dir'])
        assert result == True
        assert not Path('test_dir').exists()


def run_simple_tests():
    test_class = TestMinishellFixed()

    # запускаем только простые тесты сначала
    simple_tests = [
        'test_ls_basic',
        'test_ls_specific_path',
        'test_cat_basic',
        'test_cat_nonexistent',
        'test_cp_file',
        'test_mv_file',
        'test_mv_to_directory',
        'test_rm_file'
    ]

    passed = 0
    failed = 0

    for method_name in simple_tests:
        try:
            test_class.setup_method()
            method = getattr(test_class, method_name)
            method()
            print(f" {method_name} - PASSED")
            passed += 1
        except Exception as e:
            print(f" {method_name} - FAILED: {e}")
            failed += 1
        finally:
            test_class.teardown_method()

    print("=" * 50)
    print(f"РЕЗУЛЬТАТ: {passed} passed, {failed} failed")
    print("=" * 50)


if __name__ == "__main__":
    run_simple_tests()