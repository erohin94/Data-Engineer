# Домашнее задание по созданию базы данных и манипуляциям с таблицами:

<img width="1169" height="444" alt="image" src="https://github.com/user-attachments/assets/5a5c1a7a-72ee-40c1-96d7-ccc1aa1833f6" />

**Создайте базу данных примерно с 4-мя сущностями. Предметную область можете выбрать по своему усмотрению. 
Например, это может быть управление проектами с сущностями: Projects, Employees, Tasks, Assignments**

```
-- Таблица Authors
CREATE TABLE Authors (
    author_id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    birth_year INT CHECK (birth_year > 0) --CHECK — это ограничение целостности (constraint), можно вставить только значения больше нуля;
										  --CHECK говорит базе данных:
										  --«При вставке или изменении строки убедись, что условие выполняется. Если не выполняется — отклони операцию с ошибкой».
);

-- Таблица Books
CREATE TABLE Books (
    book_id INT PRIMARY KEY,
    title VARCHAR(150) NOT NULL,
    published_year INT,
    author_id INT NOT NULL,
    CONSTRAINT fk_books_authors FOREIGN KEY (author_id) REFERENCES Authors(author_id)
    --CONSTRAINT fk_books_authors - имя ограничения.
    --FOREIGN KEY (author_id) - объявляет, что столбец author_id в таблице Books является внешним ключом.
    --REFERENCES Authors(author_id) - указывает, что внешний ключ в Books.author_id ссылается на Authors.author_id.
);

-- Таблица Readers
CREATE TABLE Readers (
    reader_id INT PRIMARY KEY,
    full_name VARCHAR(150) NOT NULL,
    birth_year INT
);

-- Таблица Borrowings
CREATE TABLE Borrowings (
    borrowing_id INT PRIMARY KEY,
    reader_id INT NOT NULL,
    book_id INT NOT NULL,
    borrow_date DATE NOT NULL,
    return_date DATE,
    CONSTRAINT fk_borrowings_readers FOREIGN KEY (reader_id) REFERENCES Readers(reader_id),
    CONSTRAINT fk_borrowings_books FOREIGN KEY (book_id) REFERENCES Books(book_id)
);
```

**Создайте концептуальную схему по этим сущностям с указанием связей**

Что это значит простыми словами:

Ты выделяешь сущности (например, Авторы, Книги, Читатели, Выдачи).

Для каждой сущности указываешь основные атрибуты (ID, имя, дата и т.д.).

Показываешь связи между сущностями (один ко многим, многие ко многим и т.п.).

На этом уровне не обязательно указывать типы данных (INT, VARCHAR и т.п.) — это будет уже в логической схеме.

------------------------------------------------------------------------------

Пример концептуальной схемы для «Библиотеки»

*Сущности:*

Author (Автор): AuthorID, Name, BirthYear

Book (Книга): BookID, Title, PublishedYear

Reader (Читатель): ReaderID, FullName, BirthYear

Borrowing (Выдача): BorrowingID, BorrowDate, ReturnDate

*Связи:*

Автор ↔ Книга: 1 ко многим (один автор пишет много книг).

Читатель ↔ Выдача: 1 ко многим (один читатель может брать много книг).

Книга ↔ Выдача: 1 ко многим (одну книгу можно выдавать много раз, но каждый раз — в новой записи).

```
Визуально (как ER-диаграмма):
Author (1) ───< (N) Book
Reader (1) ───< (N) Borrowing >─── (1) Book
```

*Концептуальная схема* — это картинка/схема (или текстовое описание), где видны сущности и связи между ними.

*Логическая схема* — это уже описание таблиц с ключами, типами данных и ограничениями.

*Физическая модель* — это SQL-скрипты для создания таблиц.

**Сделайте описание каждой таблицы с типами данных и ограничениями, названиями столбцов. 
В каждой таблице должен быть первичный ключ, внешний ключ только в связанных таблицах, ограничения целостности по усмотрению.**

Таблицы с описанием

*Таблица Authors*

```
author_id INT PRIMARY KEY

name VARCHAR(100) NOT NULL

birth_year INT CHECK (birth_year > 0)
```

*Таблица Books*

```
book_id INT PRIMARY KEY

title VARCHAR(150) NOT NULL

published_year INT

author_id INT NOT NULL
→ FOREIGN KEY (author_id) REFERENCES Authors(author_id)
```

*Таблица Readers*

```
reader_id INT PRIMARY KEY

full_name VARCHAR(150) NOT NULL

birth_year INT
```

*Таблица Borrowings*

```
borrowing_id INT PRIMARY KEY

reader_id INT NOT NULL
→ FOREIGN KEY (reader_id) REFERENCES Readers(reader_id)

book_id INT NOT NULL
→ FOREIGN KEY (book_id) REFERENCES Books(book_id)

borrow_date DATE NOT NULL

return_date DATE NULL
```

**Создайте логическую модель. Очень важно разобраться и правильно отобразить ссылочную целостность между взаимосвязанными таблицами.**

Все ключи определены.

Связи 1:N реализованы через внешние ключи.

Ограничения: NOT NULL, CHECK, PRIMARY KEY, FOREIGN KEY.

**Вставьте по несколько строк в каждую таблицу. Учтите, что сначала необходимо вставлять строки в родительскую таблицу, в которой первичный ключ ссылается на внешний ключ дочерней.**

```
-- Родительские таблицы
INSERT INTO Authors VALUES (1, 'Leo Tolstoy', 1828);
INSERT INTO Authors VALUES (2, 'Fyodor Dostoevsky', 1821);

INSERT INTO Books VALUES (1, 'War and Peace', 1869, 1);
INSERT INTO Books VALUES (2, 'Anna Karenina', 1877, 1);
INSERT INTO Books VALUES (3, 'Crime and Punishment', 1866, 2);

INSERT INTO Readers VALUES (1, 'Ivan Petrov', 1990);
INSERT INTO Readers VALUES (2, 'Anna Ivanova', 1985);

-- Дочерняя таблица
INSERT INTO Borrowings VALUES (1, 1, 1, '2025-08-01', '2025-08-15');
INSERT INTO Borrowings VALUES (2, 2, 2, '2025-08-05', NULL);
```




