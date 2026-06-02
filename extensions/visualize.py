import sys
import traceback
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from extensions.visualizer.main_interface.tk_viewer import MailViewer


def main():
    print("visualize.py запущен")
    try:
        viewer = MailViewer()
        print("Окно создано")
        viewer.run()
    except Exception:
        print("Ошибка при запуске визуализатора:")
        traceback.print_exc()


if __name__ == "__main__":
    main()
