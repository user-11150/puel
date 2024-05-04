# coding: utf-8

# UTest 是一个测试工具
import os
import multiprocessing

def uel_test(filename) -> None:
    print(filename)
    os.system(f"python -B -m main {filename}")

def find_uels(directory):
    result = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            abspath = os.path.join(root, file)
            if abspath.endswith(".uel"):
                result.append(abspath)
    return result


def main():
    with multiprocessing.Pool() as pool:
        pool.map(uel_test, find_uels("__test__"))

if __name__ == "__main__":
    main()

