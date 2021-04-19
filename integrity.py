import hashlib
import os
import argparse
import re


def get_file_dict(input_file, directory):
    """ Возвращает словарь вида {'filename': 'полное имя файла с путем',
                                 'method': '[sha256, sha1, md5]',
                                 'hash': 'строка хэш-суммы'}"""
    lines = []
    try:
        f = open(input_file)
        for line in f:
            if line[-1] == "\n":
                line = line[0:len(line) - 1]
            lines.append(line)
        f.close()
    except FileNotFoundError:
        print('отсутсвует файл задания')
        exit(-1)
    result = []
    for i, line in enumerate(lines):
        parts = re.split(r'( SHA256 | SHA1 | MD5 )', line)
        if len(parts) != 3:
            print(f'Неправильный формат файла задания в строке {i}: {line}')
            exit(-1)
        result.append({'filename': os.path.join(os.path.abspath(directory), parts[0]),
                       'method': parts[1].lstrip().rstrip().lower(),
                       'hash': parts[2]})
    return result


def main():
    p = argparse.ArgumentParser(usage=f'Использование: python integrity.py "имя файла с заданием" '
                                      f'"каталог, где лежат файлы"')
    p.add_argument('input_file', type=str, metavar='имя файла с заданием')
    p.add_argument('directory', type=str, metavar='каталог, где лежат файлы')
    args = p.parse_args()

    input_file = args.input_file
    directory = args.directory

    file_dict = get_file_dict(input_file, directory)

    for file_el in file_dict:
        try:
            file_for_check = open(file_el['filename'], 'rb')
        except FileNotFoundError:
            print(f"Файл НЕ НАЙДЕН  <- {file_el['filename']}")
            continue
        if os.path.getsize(file_el['filename']) > 100000000:
            print(f"Файл ОЧ БОЛЬШОЙ <- {file_el['filename']}")
            continue
        data = file_for_check.read()
        file_for_check.close()
        my_hash = hashlib.new(file_el['method'])
        my_hash.update(data)
        if my_hash.hexdigest() == file_el['hash']:
            print(f"Файл OK         <- {file_el['filename']}")
        else:
            print(f"Файл НЕ ОК      <- {file_el['filename']}")


if __name__ == "__main__":
    main()
