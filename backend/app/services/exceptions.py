from uuid import UUID

from app.domain.exceptions import OperationalException


class ExceptionQueue:
    def __init__(self) -> None:
        self._items: dict[UUID, OperationalException] = {}

    def add(self, item: OperationalException) -> OperationalException:
        self._items[item.exception_id] = item
        return item

    def list_open(self) -> list[OperationalException]:
        return [item for item in self._items.values() if item.status != "RESOLVED"]
