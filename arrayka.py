class AssociativeArray:
    def __init__(self, size=10):
        self.size = size
        self.table = [[] for _ in range(size)]

    def _hash(self, key):
        """Хэш-функция, возвращает индекс для ключа"""
        return hash(key) % self.size

    def insert(self, key, value):
        """Добавление элемента (метод цепочек) (при наличии ключа значение обновляется)"""
        index = self._hash(key)
        for i, (k, v) in enumerate(self.table[index]):
            if k == key:
                self.table[index][i] = (key, value)
                return
        self.table[index].append((key, value))

    def delete(self, key):
        """Удаление элемента по ключу"""
        index = self._hash(key)
        for i, (k, v) in enumerate(self.table[index]):
            if k == key:
                del self.table[index][i]
                return

    def search(self, key):
        """Поиск элемента по ключу"""
        index = self._hash(key)
        for k, v in self.table[index]:
            if k == key:
                return v
        return None


"""Данных операций достаточно, поскольку они обеспечивают все
    необходимые возможности для работы с ассоциативным массивом
    и все остальные операции можно выразить через данные базовые"""

if __name__ == '__main__':
    # Пример использования
    array = AssociativeArray()

    # Добавление элементов
    array.insert(1, 1)
    array.insert(2, 3)
    print("Associative array:", array.table)

    # Проверка разрешения коллизий
    array.insert(11, 11)
    print("Array after collision:", array.table)

    # Удаление элемента
    array.delete(1)
    print("Array after delete:", array.table)

    # Поиск значения по ключу
    print("Searched value:", array.search(2))
