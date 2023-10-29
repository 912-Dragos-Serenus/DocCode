from llist import sllist

from .element import SuperHashMapElement


class SuperHashMap:
    current_value = 0

    def __init__(self, size=20):
        self._size = size
        self._data = [sllist() for _ in range(self._size)]

    def _hashed(self, value: any) -> int:
        return hash(value) % self._size

    def put(self, key: any, value: any) -> None:
        if self.has(key):
            self.get(key).value = value
        else:
            self._data[self._hashed(key)].append(SuperHashMapElement(key, value))

    def has(self, key: any) -> bool:
        for element in self._data[self._hashed(key)]:
            if element.key == key:
                return True
        return False

    def get(self, key: any) -> SuperHashMapElement | None:
        for element in self._data[self._hashed(key)]:
            if element.key == key:
                return element
        return None
