import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import random
from threading import Thread
from queue import Queue
from multiprocessing import Process


class Gift:  # класс, считывающий информацию из файла
    def __init__(self, name_file):
        self.name_file = name_file

    def read_file(self):
        with open(self.name_file) as file:
            line = file.readline()
            gifts = line.split()
            return gifts  # возвращает список


class B:
    def __init__(self, gift):
        self.gift = gift

    @staticmethod
    def box(gift):
        i = random.randint(1, 2)
        str_i = str(i)
        new_str = 'Box:' + str_i + ' - ' + gift
        return new_str


class A:  # это процесс с очередью
    def __init__(self, gifts):
        self.gifts = gifts

    def queue(self, q):
        for i in self.gifts:
            q.put(i)
        q.put(None)
        q.put(None)

    @staticmethod
    def present(q, box):  # делаю статическими, чтобы использовать этот метод в другом методе
        while True:
            item = q.get()
            if item is None:
                break
            print(box, item, end='\n')


class C:
    def __init__(self, gifts):
        self._block = threading.RLock()
        self.gifts = gifts

    def present(self):
        self._block.acquire()
        box = []

        for i in self.gifts:
            self.gifts.remove(i)
            if len(box) < 3:
                box.append(i)
            else:
                break
        print('Box:' + str(random.randint(1, 4)), box)
        self._block.release()


def main_one():
    t0 = time.time()
    with ThreadPoolExecutor(max_workers=2) as pool:
        results = [pool.submit(B.box, i) for i in Gift('t.txt').read_file()]
        for future in as_completed(results):
            print(future.result())
    print(time.time() - t0)
    print()


def main_two():
    t0 = time.time()
    my_gifts = Gift('t.txt').read_file()  # создаем экземпляр класса, который считывает информацию из файла

    q = Queue(6)
    box1 = Thread(target=A.present, args=(q, 'Box: 1 -'))  # использую статический метод в target
    box2 = Thread(target=A.present, args=(q, 'Box: 2 -'))

    box1.start()
    box2.start()

    A(my_gifts).queue(q)

    box1.join()
    box2.join()

    print(time.time() - t0)
    print()


def main_thee():
    t0 = time.time()
    my_gifts = Gift('t.txt').read_file()  # создаем экземпляр класса, который считывает информацию из файла

    process_C = C(my_gifts)

    box1 = Thread(target=process_C.present)  # использую статический метод в target
    box2 = Thread(target=process_C.present)

    box1.start()
    box1.join()
    box2.start()
    box2.join()
    print(time.time() - t0)


def main():
    p_one = Process(target=main_one)
    p_two = Process(target=main_two())
    p_three = Process(target=main_thee())

    p_one.start()
    p_two.start()
    p_three.start()

    p_one.join()
    p_two.join()
    p_three.join()


if __name__ == '__main__':
    main()





