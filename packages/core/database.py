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