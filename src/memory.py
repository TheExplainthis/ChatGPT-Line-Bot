from collections import defaultdict


class MemoryInterface:
    def append(self, user_id: str, text: str) -> None:
        pass

    def get(self, user_id: str) -> str:
        return ""

    def remove(self, user_id: str) -> None:
        pass


class Memory(MemoryInterface):
    def __init__(self):
        self.storage = defaultdict(list)

    def append(self, user_id: str, text: str) -> None:
        self.storage[user_id].append(text)

    def get(self, user_id: str) -> str:
        HISTORY_MESSAGE_COUNT = 3
        return '\n\n'.join(self.storage.get(user_id, [])[-HISTORY_MESSAGE_COUNT:])

    def remove(self, user_id: str) -> None:
        self.storage[user_id] = []
