from dataclasses import dataclass
from abc import ABC, abstractmethod

# Собственное исключение (Пункт 7 презентации)
class RestorationError(Exception):
    """Базовое исключение для мастерской реставрации."""
    pass

class InvalidValueError(RestorationError):
    """Вызывается при некорректных или отрицательных числовых данных."""
    pass


# Полиморфный интерфейс (Пункт 3 презентации)
class Describable(ABC):
    @abstractmethod
    def get_info(self) -> str:
        pass


@dataclass
class Master(Describable):
    name: str
    specialization: str

    def get_info(self) -> str:
        return f"Мастер: {self.name} (Специализация: {self.specialization})"


@dataclass
class RestoredItem(Describable):
    item_name: str          # Например: "Дубовый комод"
    category: str           # Например: "Корпусная мебель"
    _restored_count: int = 0  # Сколько отреставрировано
    _cost_per_item: float = 0.0

    @property
    def restored_count(self) -> int:
        return self._restored_count

    @restored_count.setter
    def restored_count(self, value: int):
        if value < 0:
            raise InvalidValueError("Количество отреставрированных предметов не может быть отрицательным.")
        self._restored_count = value

    @property
    def cost_per_item(self) -> float:
        return self._cost_per_item

    @cost_per_item.setter
    def cost_per_item(self, value: float):
        if value < 0:
            raise InvalidValueError("Стоимость услуги не может быть отрицательной.")
        self._cost_per_item = value

    def get_info(self) -> str:
        total = self._restored_count * self._cost_per_item
        return f"Мебель: {self.item_name} [{self.category}] | Отреставрировано: {self._restored_count} шт. | Сумма: {total} руб."