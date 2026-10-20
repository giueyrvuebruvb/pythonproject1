from models import RestoredItem, InvalidValueError
from storage import RestorationWorkshopManager
import logging


class ConsoleUI:
    def __init__(self, manager: RestorationWorkshopManager):
        self.manager = manager

    def run(self):
        while True:
            print("\n=== УЧЁТ РЕСТАВРАЦИИ МЕБЕЛИ ===")
            print("1. Посмотреть все записи (через генератор)")
            print("2. Добавить или изменить данные по реставрации")
            print("3. Найти мебель по названию (Свой поиск O(N))")
            print("4. Отсортировать по количеству отреставрированного (Своя сортировка O(N^2))")
            print("5. Импортировать из CSV и выгрузить итоговый отчёт в JSON")
            print("6. Выход")

            choice = input("Выберите пункт меню: ").strip()

            if choice == '1':
                print("\n--- Отчёт по отреставрированной мебели ---")
                for info in self.manager.lazy_load_report():
                    print(info)
            elif choice == '2':
                self._handle_add_or_update()
            elif choice == '3':
                self._handle_search()
            elif choice == '4':
                self._handle_sort()
            elif choice == '5':
                self._handle_files()
            elif choice == '6':
                print("Выход из программы. До свидания!")
                break
            else:
                print("Неверный выбор. Введите число от 1 до 6.")

    def _handle_add_or_update(self):
        try:
            name = input("Введите название мебели (например, Стул венский): ").strip()
            if not name:
                raise ValueError("Название не может быть пустым.")
            category = input("Введите категорию (например, Стулья): ").strip()
            count = int(input("Сколько единиц отреставрировано?: "))
            cost = float(input("Стоимость реставрации 1 ед. (руб.): "))

            # Проверка, есть ли уже такой объект в памяти (в словаре)
            if name in self.manager.item_index_map:
                existing = self.manager.item_index_map[name]
                existing.restored_count += count
                existing.cost_per_item = cost
                print(f"Запись '{name}' обновлена! Новое общее количество: {existing.restored_count}")
            else:
                item = RestoredItem(name, category, _restored_count=count, _cost_per_item=cost)
                self.manager.add_item(item)
                print("Новая запись успешно добавлена!")
        except (ValueError, InvalidValueError) as e:
            print(f"Ошибка ввода данных: {e}")
            logging.warning(f"Ошибка при добавлении/обновлении записи: {e}")

    def _handle_search(self):
        kw = input("Введите ключевое слово для поиска: ")
        results = self.manager.search_by_name(kw)
        if not results:
            print("Ничего не найдено.")
        else:
            print("\n--- Результаты поиска ---")
            for r in results:
                print(r.get_info())

    def _handle_sort(self):
        asc_input = input("Сортировать по возрастанию количества? (y/n): ").lower()
        ascending = True if asc_input == 'y' else False
        sorted_items = self.manager.sort_items_by_count(ascending)
        print("\n--- Отсортированный список ---")
        for i in sorted_items:
            print(i.get_info())

    def _handle_files(self):
        try:
            self.manager.import_from_csv('data.csv')
            self.manager.export_to_json('report.json')
            print("Импорт из data.csv и сохранение итогов в report.json прошли успешно!")
        except Exception as e:
            print(f"Ошибка при работе с файлами: {e}")