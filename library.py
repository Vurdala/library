import json


class Book:
    """Класс, описывающий книгу и действия с ней."""

    def __init__(self, title="Нет", author="Нет", year="Нет", filename="books.json"):
        """Инациализация Book."""
        self.filename = filename
        self.load()
        self.id = len(self.books["books"]) + 1
        self.title = title
        self.author = author
        self.year = year
        self.status = "В наличии"

    def load(self):
        """Выгрузка файла с книгами."""
        try:
            with open(self.filename, encoding="utf-8") as f:
                self.books = json.load(f)
        except FileNotFoundError:
            self.books = {"books": []}

    def save(self):
        """Сохранение файла с книгами."""
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(self.books, f, ensure_ascii=False, indent=4)

    def add_book(self):
        """Добавляет книгу."""
        data = {
            "id": str(self.id),
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "status": self.status,
        }
        self.books["books"].append(data)
        self.save()
        print("Книга успешно добавлена")

    # При удалении книги, id книг смещаются,
    # что бы корректно работало автоматическое присваивание id

    def change_id(self):
        for i in range(len(self.books["books"])):
            self.books["books"][i]["id"] = str(i + 1)
            self.save()

    def delete_book(self, book_id):
        """Удаляает книгу."""
        quantity = len(self.books["books"])
        for i in self.books["books"]:
            if i["id"] == book_id:
                self.books["books"].remove(i)
                self.save()
        quantity_after = len(self.books["books"])
        if quantity != quantity_after:
            self.change_id()
        else:
            print("Такого id нет в библиотеке")

    def all_books(self):
        """Показывает все книги."""
        for i in self.books['books']:
            print(i)

    def change_status(self, book_id, new_status):
        """Меняет статус книги."""
        for i in self.books["books"]:
            if i["id"] == book_id:
                ind = self.books["books"].index(i)
                self.books["books"][ind]["status"] = new_status
                self.save()
        print("Статус книги успешно изменен")

    def search_book(self, book_info):
        """Ищет книгу по информации."""
        for i in self.books["books"]:
            if book_info in i.values():
                return i
        


book_for_command = Book()


def main():
    """Функция для взаимодействия пользователя с библиотекой."""
    while True:
        print(
            "Введите номер команды: \n",
            "1 - Добавить книгу \n",
            "2 - Удалить книгу \n",
            "3 - Поиск книги \n",
            "4 - Отоброзить все книги \n",
            "5 - Изменить статус книги \n",
            "6 - Для выхода из программы ",
        )
        try:
            command = int(input())
        except ValueError:
            raise ValueError('Введите номер команды')
        if command == 1:
            title = input("Введите название книги: ")
            author = input("Введите ФИО автора: ")
            year = input("Введите год, когда была написана книга: ")
            book = Book(title, author, year)
            book.add_book()
        elif command == 2:
            book_for_command = Book()
            book_id = str(input("Введите id книги: "))
            book_for_command.delete_book(book_id)
        elif command == 3:
            book_for_command = Book()
            book_info = str(input("Введите название, автора или год: "))
            book = book_for_command.search_book(book_info)
            if book is None:
                print('Ничего не найдено')
            else:
                print(book)
        elif command == 4:
            book_for_command = Book()
            book_for_command.all_books()
        elif command == 5:
            book_for_command = Book()
            book_id = str(input("Введите id книги: "))
            status = str(input("Введите новый статус(в наличии или выдана): ")).lower()
            book_for_command.change_status(book_id, status)
        elif command == 6:
            return False


if __name__ == "__main__":
    try:
        main()
    except Exception as err:
        print(f'Возникла ошибка: {err}')
