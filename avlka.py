class AVLNode:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None
        self.height = 1


class AVLTree:
    def __init__(self):
        self.root = None

    @staticmethod
    def _height(node):
        """Возвращает высоту дерева"""
        if node is None:
            return 0

        return node.height

    def _correct_height(self, node):
        """Изменение высоты узла"""
        node.height = max(self._height(node.right), self._height(node.right)) + 1

    def _diff_height(self, node):
        """Поиск разности высот поддеревьев"""
        if node is None:
            return 0

        return self._height(node.right) - self._height(node.left)

    def _rotate_left(self, node):
        """Малый левый поворот"""
        new_node = node.right
        node.right = new_node.left
        new_node.left = node

        self._correct_height(node)
        self._correct_height(new_node)

        return new_node

    def _rotate_right(self, node):
        """Малый правый поворот"""
        new_node = node.left
        node.left = new_node.right
        new_node.right = node

        self._correct_height(node)
        self._correct_height(new_node)

        return new_node

    def _balance(self, node):
        """Операция балансировки дерева"""
        if node is None:
            return None

        self._correct_height(node)
        diff = self._diff_height(node)
        diff_left = self._diff_height(node.left)
        diff_right = self._diff_height(node.right)

        if diff == -2:
            if diff_left > 0:
                node.left = self._rotate_left(node.left)
            return self._rotate_right(node)
        elif diff == 2:
            if diff_right < 0:
                node.right = self._rotate_right(node.right)
            return self._rotate_left(node)

        return node

    def insert(self, key, value):
        """Вставка узла (без дубликатов)"""
        self.root = self._insert(self.root, key, value)

    def _insert(self, node, key, value):
        if node is None:
            return AVLNode(key, value)

        if key < node.key:
            node.left = self._insert(node.left, key, value)
        if key > node.key:
            node.right = self._insert(node.right, key, value)

        node = self._balance(node)
        return node

    def search(self, key):
        """Поиск значения по ключу (выбрасывает ошибку при отсутствии элемента)"""
        node = self._search(self.root, key)
        if node is None:
            raise KeyError(f"Key '{key}' not found")
        return node.value

    def _search(self, node, key):
        if node is None or node.key == key:
            return node

        if key < node.key:
            return self._search(node.left, key)
        return self._search(node.right, key)

    def _delete_min(self, node):
        """Удаление узла с минимальным ключом"""
        if node is None:
            return None

        if node.left is None:
            return node.right

        node.left = self._delete_min(node.left)
        return self._balance(node)

    @staticmethod
    def _search_min(node):
        """Поиск узла с минимальным ключом"""
        while node.left is not None:
            node = node.left

        return node

    def delete(self, key):
        """Удаление узла по ключу (выбрасывает ошибку при отсутствии элемента)"""
        self.root = self._delete(self.root, key)

    def _delete(self, node, key):
        if node is None:
            raise KeyError(f"Key '{key}' not found")

        if key < node.key:
            node.left = self._delete(node.left, key)
        elif key > node.key:
            node.right = self._delete(node.right, key)
        else:
            if node.right is None:
                return node.left
            else:
                min_node = self._search_min(node.right)
                min_node.right = self._delete_min(node.right)
                min_node.left = node.left
                return self._balance(min_node)

        return self._balance(node)

    def update(self, key, value):
        """Обновление значения по ключу (выбрасывает ошибку при отсутствии элемента)"""
        self._update(self.root, key, value)

    def _update(self, node, key, value):
        node = self._search(node, key)
        if node:
            node.value = value
        else:
            raise KeyError(f"Key '{key}' not found")

    def merge(self, other_tree):
        """Слияние двух деревьев (без дубликатов)"""
        return self._merge(self, other_tree)

    def _merge(self, first_node, second_node):
        first_nodes = [x for x in first_node.in_order()]
        second_nodes = [x for x in second_node.in_order()]

        nodes = self.merge_nodes(first_nodes, second_nodes)

        new_tree = AVLTree()
        new_tree.build_tree(nodes)

        return new_tree

    @staticmethod
    def merge_nodes(first_nodes, second_nodes):
        """Объединение двух массивов узлов деревьев"""
        result = []
        f = s = 0

        while f < len(first_nodes) and s < len(second_nodes):
            if first_nodes[f].key < second_nodes[s].key:
                result.append(first_nodes[f])
                f += 1
            elif first_nodes[f].key > second_nodes[s].key:
                result.append(second_nodes[s])
                s += 1
            else:
                # Если ключи совпадают - добавляем узел из 2-го дерева
                result.append(second_nodes[s])
                f += 1
                s += 1
        result.extend(first_nodes[f:])
        result.extend(second_nodes[s:])

        return result

    def split(self, key):
        """Разделение АВЛ-дерева на два дерева по ключу (первое содержит элементы < ключа)"""
        first_nodes = []
        second_nodes = []
        for item in self.in_order():
            if item.key < key:
                first_nodes.append(item)
            else:
                second_nodes.append(item)

        first_tree = AVLTree()
        second_tree = AVLTree()
        first_tree.build_tree(first_nodes)
        second_tree.build_tree(second_nodes)

        return first_tree, second_tree

    def build_tree(self, sorted_list):
        """Построение АВЛ-дерева из отсортированного списка"""
        self.root = self._build_tree(sorted_list, 0, len(sorted_list) - 1)

    def _build_tree(self, sorted_list, start, end):
        if start > end:
            return None

        mid = (start + end) // 2
        node = AVLNode(sorted_list[mid].key, sorted_list[mid].value)
        node.left = self._build_tree(sorted_list, start, mid - 1)
        node.right = self._build_tree(sorted_list, mid + 1, end)

        self._correct_height(node)
        return self._balance(node)

    def count(self):
        """Подсчет количества узлов в дереве"""
        return self._count(self.root)

    def _count(self, node):
        if node is None:
            return 0

        return 1 + self._count(node.left) + self._count(node.right)

    def in_order(self):
        """Проход по дереву в порядке возрастания ключей"""
        return self._in_order(self.root)

    def _in_order(self, node, lst=None):
        if node is None:
            return

        if lst is None:
            lst = []

        self._in_order(node.left, lst)
        lst += [node]
        self._in_order(node.right, lst)

        return lst

    def print_tree(self):
        """Визуализация АВЛ-дерева"""
        self._print_tree(self.root)
        print()

    def _print_tree(self, root, level=0):
        if root is not None:
            self._print_tree(root.right, level + 1)
            print(' ' * 4 * level + '-> ' + '(' + str(root.key) + ') ' + str(root.value))
            self._print_tree(root.left, level + 1)


if __name__ == '__main__':
    # Пример использования
    tree = AVLTree()
    tree.insert(1, 1)
    tree.insert(5, 5)
    tree.insert(3, 3)

    # Визуализация дерева
    print("Tree:")
    tree.print_tree()

    # Поиск значения по ключу
    info = tree.search(3)
    print("Searched value:", info, "\n")

    # Обновление значения по ключу
    tree.update(1, 100)
    print("Updated tree:")
    tree.print_tree()

    # Удаление узла по ключу
    tree.delete(3)
    print("Tree after removal:")
    tree.print_tree()

    tree1 = AVLTree()
    tree1.insert(10, 10)
    tree1.insert(3, 3)
    tree1.insert(4, 4)
    print("Tree1:")
    tree1.print_tree()

    # Слияние деревьев
    tree_merged = tree.merge(tree1)
    print("Merged tree (tree + tree1):")
    tree_merged.print_tree()

    # Разделение дерева по ключу
    first, second = tree_merged.split(4)
    print("First tree:")
    first.print_tree()
    print("Second tree:")
    second.print_tree()

    # Количество элементов в дереве
    print("Second tree size:", second.count())
