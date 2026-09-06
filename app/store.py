from dataclasses import dataclass, asdict
from itertools import count


MAX_NAME_LENGTH = 100


class InvalidItemName(ValueError):
    pass


class ItemNotFound(LookupError):
    def __init__(self, item_id: int) -> None:
        super().__init__(f"item {item_id} not found")
        self.item_id = item_id


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
        try:
            return self._items[item_id]
        except KeyError:
            raise ItemNotFound(item_id) from None

    def add(self, name: str) -> Item:
        cleaned = _clean_name(name)
        item = Item(id=next(self._ids), name=cleaned)
        self._items[item.id] = item
        return item

    def mark_done(self, item_id: int) -> Item:
        item = self.get(item_id)
        item.done = True
        return item

    def remove(self, item_id: int) -> None:
        self.get(item_id)
        del self._items[item_id]


def _clean_name(name: object) -> str:
    if not isinstance(name, str) or not name.strip():
        raise InvalidItemName("name is required and must be a non-empty string")
    cleaned = name.strip()
    if len(cleaned) > MAX_NAME_LENGTH:
        raise InvalidItemName(f"name must be at most {MAX_NAME_LENGTH} characters")
    return cleaned
