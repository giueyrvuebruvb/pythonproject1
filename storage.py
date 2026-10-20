import csv
import json
import logging
from typing import List, Generator
from models import RestoredItem, InvalidValueError

logger = logging.getLogger(__name__)


class RestorationWorkshopManager:
    def __init__(self):
        self.items: List[RestoredItem] = []  # list для порядка (Пункт 4)
        self.categories = set()  # set для уникальных категорий (Пункт 4)
        self.item_index_map = {}  # dict для быстрого индексирования (Пункт 4)

    def add_item(self, item: RestoredItem):
        self.items.append(item)
        self.categories.add(item.category)
        self.item_index_map[item.item_name] = item
        logger.info(f"Добавлена запись: {item.item_name} ({item.restored_count} шт.)")

    # СОБСТВЕННЫЙ ПОИСК (Пункт 4)
    def search_by_name(self, keyword: str) -> List[RestoredItem]:
        """
        Линейный поиск по названию мебели.
        Сложность: O(N), где N — количество записей.
        """
        if not keyword.strip():
            return []
        found = []
        for item in self.items:
            if keyword.lower() in item.item_name.lower():
                found.append(item)
        return found

    # СОБСТВЕННАЯ СОРТИРОВКА (Пункт 4)
    def sort_items_by_count(self, ascending: bool = True) -> List[RestoredItem]:
        """
        Сортировка пузырьком (Bubble Sort) по количеству отреставрированных единиц.
        Сложность: O(N^2). Написана вручную без встроенных sort().
        """
        n = len(self.items)
        arr = list(self.items)
        for i in range(n):
            for j in range(0, n - i - 1):
                cond = (arr[j].restored_count > arr[j + 1].restored_count) if ascending else (
                            arr[j].restored_count < arr[j + 1].restored_count)
                if cond:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
        return arr

    # ГЕНЕРАТОР для ленивой обработки (Пункт 6)
    def lazy_load_report(self) -> Generator[str, None, None]:
        """Потоковая выдача информации без загрузки всего файла в память разом."""
        for item in self.items:
            yield item.get_info()

    # Импорт из CSV (Пункт 6)
    def import_from_csv(self, filepath: str):
        try:
            with open(filepath, mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    item = RestoredItem(
                        item_name=row['item_name'],
                        category=row['category'],
                        _restored_count=int(row['restored_count']),
                        _cost_per_item=float(row['cost_per_item'])
                    )
                    self.add_item(item)
            logger.info(f"Успешный импорт CSV из {filepath}")
        except Exception as e:
            logger.error(f"Ошибка импорта CSV: {e}")
            raise

    # Экспорт в JSON (Пункт 6)
    def export_to_json(self, filepath: str):
        data = [{
            "item_name": i.item_name,
            "category": i.category,
            "restored_count": i.restored_count,
            "cost_per_item": i.cost_per_item,
            "total_sum": i.restored_count * i.cost_per_item
        } for i in self.items]

        with open(filepath, mode='w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        logger.info(f"Экспорт в JSON выполнен: {filepath}")