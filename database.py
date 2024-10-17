import sqlite3
import pathlib
from typing import List, Dict
from datetime import date

DATABASE = pathlib.Path(__file__).parent / 'database.sqlite'

class DatabaseAPI:
    def __init__(self):
        self.create_db()
        self.connection = sqlite3.connect(DATABASE)
        self.connection.row_factory = sqlite3.Row
        self.connection.execute('PRAGMA foreign_keys = ON')

    def create_db(self):
        query = """
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            quantidade INTEGER NOT NULL,
            preco REAL NOT NULL,
            validade DATE NOT NULL
        )
        """
        try:
            with sqlite3.connect(DATABASE) as connection:
                cursor = connection.cursor()
                cursor.executescript(query)
                connection.commit()
                print("Banco de dados criado com sucesso")
        except sqlite3.Error as e:
            print(f"Erro ao criar o banco de dados: {e}")

    def close_connection(self):
        self.connection.close()

    def get_produtos(self,) -> List[Dict]:
        cursor = self.connection.cursor()
        result = cursor.execute('SELECT * FROM produtos').fetchall()
        self.close_connection()
        return [dict(row) for row in result]
    
    def create_produto(self, nome: str, quantidade: int, preco: float, validade: date) -> int:
        cursor = self.connection.cursor()
        try:
            cursor.execute('INSERT INTO produtos (nome, quantidade, preco, validade) VALUES (?, ?, ?, ?)', (nome, quantidade, preco, validade))
        except sqlite3.Error as e:
            self.close_connection()
            return {e}
        self.connection.commit()
        self.close_connection()
        return cursor.lastrowid
    
    def delete_produto(self, id: int) -> bool:
        cursor = self.connection.cursor()
        try:
            cursor.execute('DELETE FROM produtos WHERE id = ?', (id,))
            self.connection.commit()
        except sqlite3.Error as e:
            self.close_connection()
            return {e}
        self.close_connection()
        return True
    
