import logging
from storage import RestorationWorkshopManager
from ui import ConsoleUI

def configure_logging():
    logging.basicConfig(
        filename='app.log',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

if __name__ == '__main__':
    configure_logging()
    manager = RestorationWorkshopManager()
    ui = ConsoleUI(manager)
    ui.run()