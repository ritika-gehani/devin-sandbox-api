from dataclasses import dataclass, asdict
from itertools import count


@dataclass
class Item:
    id: int
    name: str
    done: bool = False

    def to_dict(self) -> dict:
        return asdict(self)


class ItemStore:
    def __init__(self) -> None:
        self._items: dict[int, Item] = {}
        self._ids = count(1)

    def list(self) -> list[Item]:
        return list(self._items.values())

    def get(self, item_id: int) -> Item:
        return self._items[item_id]

    def add(self, name: str) -> Item:
        item = Item(id=next(self._ids), name=name)
        self._items[item.id] = item
        return item

    def mark_done(self, item_id: int) -> Item:
        item = self.get(item_id)
        item.done = True
        return item
