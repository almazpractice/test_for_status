import logging

from collections import defaultdict
from typing import List

LOG_FORMAT = '"%(asctime)s - [%(levelname)s] - %(message)s"'
DT_FORMAT = "%d.%m.%Y %H:%M:%S"


class TreeStore:
    def __init__(self, items: List[dict]) -> None:
        self.items_list = items
        self.items = {item["id"]: item for item in items}
        self.items_by_parents = self.__group_by_parents(self.items_list)

    def __group_by_parents(self, items):
        parents_list = defaultdict(list)
        for item in items:
            parents_list[item["parent"]].append(item)
        return dict(parents_list)

    def getAll(self) -> list:
        return self.items.values()

    def getItem(self, item: int = None) -> dict:
        if item is None or item not in self.items.keys():
            return None
        return self.items[item]

    def getChildren(self, parent: int) -> list:
        if parent not in self.items_by_parents.keys():
            return []
        return self.items_by_parents[parent]

    def getAllParents(self, child: int) -> List[dict]:
        item = self.getItem(child)
        res = []
        while item["id"] > 1:
            res.append(self.getItem(item["parent"]))
            item = self.getItem(item["parent"])
        return res


def main():
    logging.basicConfig(
        datefmt=DT_FORMAT,
        format=LOG_FORMAT,
        level=logging.INFO,
    )
    items = [
        {"id": 1, "parent": "root"},
        {"id": 2, "parent": 1, "type": "test"},
        {"id": 3, "parent": 1, "type": "test"},
        {"id": 4, "parent": 2, "type": "test"},
        {"id": 5, "parent": 2, "type": "test"},
        {"id": 6, "parent": 2, "type": "test"},
        {"id": 7, "parent": 4, "type": None},
        {"id": 8, "parent": 4, "type": None},
    ]
    ts = TreeStore(items)

    try:
        logging.info("Запуск тестов")
        assert ts.getItem(7) == {"id": 7, "parent": 4, "type": None}

        assert ts.getChildren(4) == [
            {"id": 7, "parent": 4, "type": None},
            {"id": 8, "parent": 4, "type": None},
        ]

        assert ts.getChildren(5) == []

        assert ts.getAllParents(7) == [
            {"id": 4, "parent": 2, "type": "test"},
            {"id": 2, "parent": 1, "type": "test"},
            {"id": 1, "parent": "root"},
        ]
        logging.info("Тесты – ок")
    except Exception:
        logging.exception("Не все тесты проходят...", stack_info=False)


if __name__ == "__main__":
    main()
