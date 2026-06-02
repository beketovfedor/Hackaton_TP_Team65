import traceback

from extensions.visualizer.main_interface.tk_viewer import MailViewer


def main():
    print("visualize.py запущен")

    try:
        viewer = MailViewer()
        print("Окно создано")
        viewer.run()
        print("mainloop завершён")

    except Exception:
        print("Ошибка при запуске визуализатора:")
        traceback.print_exc()


if __name__ == "__main__":
    main()