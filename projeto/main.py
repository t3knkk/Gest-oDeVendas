from gui import LoginWindow
from database import DatabaseManager
from logger import setup_logger, log_error

def main():
    setup_logger()

    DB_CONFIG = {
        'host': 'localhost',
        'user': 'root',
        'password': '1724',
        'database': 'sales_system'
    }

    db_manager = None
    try:
        db_manager = DatabaseManager(**DB_CONFIG)
        if not db_manager.connect():
            print("Falha ao conectar ao banco de dados")
            return

        app = LoginWindow(db_manager)
        app.mainloop()

    except Exception as e:
        log_error(e)
        print(f"Erro! Verifique error.log para detalhes.")

    finally:
        if db_manager:
            db_manager.disconnect()

if __name__ == "__main__":

    main()
