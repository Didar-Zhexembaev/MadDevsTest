from collections import defaultdict
from typing import Any
from bs4 import Tag
import threading
import htmlentities


class ThreadSafeCounter:
    def __init__(self, element: Tag, child_nodes_count: int):
        self.counter = defaultdict(int)
        self.lock = threading.Lock()
        self.element = element
        self.child_nodes_count = child_nodes_count

    def increment(self, value: int = 1) -> int:
        with self.lock:
            self.child_nodes_count += 1
            return self.child_nodes_count

    def decrement(self, value: int = 1) -> int:
        with self.lock:
            self.child_nodes_count -= 1
            return self.child_nodes_count

    def get_value(self) -> int:
        with self.lock:
            return self.child_nodes_count

    def get_name(self) -> str:
        with self.lock:
            return self.element.name

    def get_attrs(self) -> dict[str, str | Any]:
        with self.lock:
            return self.element.attrs

    def get_after_tag_content(self) -> str:
        with self.lock:
            content_buffer = []
            for content in self.element.next_siblings:
                if isinstance(content, Tag) and not str(content).isspace():
                    break
                else:
                    content_buffer.append(htmlentities.encode(content))
            return "".join(content_buffer)

    def __str__(self) -> str:
        return str(self.counter.items())
