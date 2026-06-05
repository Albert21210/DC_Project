"""Подключение к SQLite и управление схемой БД."""
import sqlite3


def get_connection(db_path: str = "shop.db") -> sqlite3.Connection:
    conn = sqlite3.connect(db_path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

_DDL = """
CREATE TABLE IF NOT EXISTS Categories (
    CategoryID   INTEGER PRIMARY KEY,
    CategoryName TEXT NOT NULL,
    Description  TEXT
);
CREATE TABLE IF NOT EXISTS Suppliers (
    SupplierID   INTEGER PRIMARY KEY,
    SupplierName TEXT NOT NULL,
    ContactPhone TEXT,
    Email        TEXT
);
CREATE TABLE IF NOT EXISTS Products (
    ProductID      INTEGER PRIMARY KEY,
    ProductName    TEXT    NOT NULL,
    CategoryID     INTEGER,
    SupplierID     INTEGER,
    Price          REAL    NOT NULL,
    StockQuantity  INTEGER NOT NULL DEFAULT 0,
    WarrantyMonths INTEGER DEFAULT 12,
    FOREIGN KEY (CategoryID) REFERENCES Categories(CategoryID),
    FOREIGN KEY (SupplierID) REFERENCES Suppliers(SupplierID)
);
CREATE TABLE IF NOT EXISTS Employees (
    EmployeeID INTEGER PRIMARY KEY,
    LastName   TEXT NOT NULL,
    FirstName  TEXT NOT NULL,
    Position   TEXT,
    HireDate   TEXT
);
CREATE TABLE IF NOT EXISTS Customers (
    CustomerID INTEGER PRIMARY KEY,
    LastName   TEXT NOT NULL,
    FirstName  TEXT NOT NULL,
    Phone      TEXT,
    Email      TEXT
);
CREATE TABLE IF NOT EXISTS Orders (
    OrderID     INTEGER PRIMARY KEY,
    CustomerID  INTEGER,
    EmployeeID  INTEGER,
    OrderDate   TEXT NOT NULL,
    OrderStatus TEXT DEFAULT 'Оформлен',
    FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID),
    FOREIGN KEY (EmployeeID) REFERENCES Employees(EmployeeID) ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS Order_Details (
    OrderDetailID INTEGER PRIMARY KEY,
    OrderID       INTEGER,
    ProductID     INTEGER,
    Quantity      INTEGER NOT NULL CHECK (Quantity > 0),
    UnitPrice     REAL    NOT NULL,
    FOREIGN KEY (OrderID)   REFERENCES Orders(OrderID)   ON DELETE CASCADE,
    FOREIGN KEY (ProductID) REFERENCES Products(ProductID)
);
CREATE TRIGGER IF NOT EXISTS tg_restore_stock
AFTER DELETE ON Order_Details
BEGIN
    UPDATE Products SET StockQuantity = StockQuantity + OLD.Quantity
    WHERE ProductID = OLD.ProductID;
END;
"""


def init_schema(conn: sqlite3.Connection) -> None:
    """Создаёт таблицы и триггер (идемпотентно)."""
    conn.executescript(_DDL)
    conn.commit()


_SEED_CATEGORIES = [
    (1, "Процессоры",         "Центральные процессоры"),
    (2, "Видеокарты",         "Графические ускорители"),
    (3, "Оперативная память", "Модули ОЗУ DDR4/DDR5"),
    (4, "Накопители",         "SSD и HDD диски"),
]
_SEED_SUPPLIERS = [
    (1, "ООО Дистрибьюция-ИТ", "+74951112233", "sales@it-dist.ru"),
    (2, "АО Компьютер-Опт",    "+78123334455", "opt@compopt.ru"),
]
_SEED_PRODUCTS = [
    (1, "Intel Core i5-13400F OEM",      1, 1, 18500.0, 15, 12),
    (2, "AMD Ryzen 7 7800X3D Box",       1, 2, 42000.0,  4, 36),
    (3, "NVIDIA RTX 4070 Super 12GB",    2, 1, 75000.0,  3, 24),
    (4, "Kingston FURY Beast DDR5 32GB", 3, 2, 13000.0, 25, 60),
    (5, "Samsung 990 PRO SSD 1TB",       4, 1, 12500.0, 20, 60),
]
_SEED_EMPLOYEES = [
    (1, "Иванов",  "Алексей", "Старший менеджер",     "2024-01-15"),
    (2, "Петрова", "Мария",   "Кассир",               "2025-03-10"),
    (3, "Сидоров", "Дмитрий", "Специалист по сборке", "2024-08-01"),
]
_SEED_CUSTOMERS = [
    (1, "Кузнецов",  "Сергей", "+79001112233", "serg@mail.ru"),
    (2, "Смирнов",   "Андрей", "+79112223344", "andrey@ya.ru"),
    (3, "Васильева", "Елена",  "+79223334455", "elena@gmail.com"),
]
_SEED_ORDERS = [
    (101, 1, 1, "2026-05-10", "Выдан"),
    (102, 2, 1, "2026-05-14", "Оформлен"),
    (103, 3, 2, "2026-05-15", "Оплачен"),
]
_SEED_DETAILS = [
    (1, 101, 1, 1, 18500.0), (2, 101, 4, 2, 13000.0),
    (3, 102, 3, 1, 75000.0), (4, 103, 2, 1, 42000.0),
    (5, 103, 5, 1, 12500.0), (6, 102, 1, 2, 18500.0),
    (7, 101, 5, 1, 12500.0), (8, 103, 4, 1, 13000.0),
]


def seed_demo_data(conn: sqlite3.Connection) -> None:
    """Заполняет БД демо-данными, если она пустая (идемпотентно)."""
    if conn.execute("SELECT COUNT(*) FROM Categories").fetchone()[0]:
        return
    cur = conn.cursor()
    cur.executemany("INSERT INTO Categories VALUES(?,?,?)",       _SEED_CATEGORIES)
    cur.executemany("INSERT INTO Suppliers VALUES(?,?,?,?)",       _SEED_SUPPLIERS)
    cur.executemany("INSERT INTO Products VALUES(?,?,?,?,?,?,?)",  _SEED_PRODUCTS)
    cur.executemany("INSERT INTO Employees VALUES(?,?,?,?,?)",     _SEED_EMPLOYEES)
    cur.executemany("INSERT INTO Customers VALUES(?,?,?,?,?)",     _SEED_CUSTOMERS)
    cur.executemany("INSERT INTO Orders VALUES(?,?,?,?,?)",        _SEED_ORDERS)
    cur.executemany("INSERT INTO Order_Details VALUES(?,?,?,?,?)", _SEED_DETAILS)
    conn.commit()