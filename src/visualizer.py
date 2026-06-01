import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import pandas as pd

plt.style.use('seaborn-v0_8')

class Visualizer:
    _root = None

    @staticmethod
    def _get_root():
        if Visualizer._root is None:
            Visualizer._root = tk.Tk()
            Visualizer._root.withdraw()
        return Visualizer._root

    @staticmethod
    def _plot_bar(data, title, xlabel, color):
        sorted_data = sorted(data.items(), key=lambda x: x[1], reverse=True)
        df = pd.DataFrame(sorted_data, columns=[xlabel, 'Count'])

        fig, ax = plt.subplots(figsize=(12, 5), facecolor='white')
        fig.patch.set_facecolor('white')

        # Строим столбцы с улучшенным видом
        bars = ax.bar(df[xlabel], df['Count'], color=color, edgecolor='black', linewidth=0.5, alpha=0.85)
        ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
        ax.set_xlabel(xlabel, fontsize=12, labelpad=10)
        ax.set_ylabel('Количество', fontsize=12, labelpad=10)
        ax.tick_params(axis='x', rotation=0, labelsize=10)
        ax.tick_params(axis='y', labelsize=10)
        ax.grid(axis='y', linestyle='--', alpha=0.7)

        # Добавляем значения над столбцами
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{int(height)}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 5),  # смещение вверх
                        textcoords="offset points",
                        ha='center', va='bottom',
                        fontsize=9, fontweight='bold')

        # Делаем рамку и фон аккуратными
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_linewidth(0.5)
        ax.spines['bottom'].set_linewidth(0.5)

        return fig

    @staticmethod
    def visualize_categories(pairs):
        if not pairs:
            print("Нет данных по категориям для визуализации.")
            return
        root = Visualizer._get_root()
        window = tk.Toplevel(root)
        window.title("Статистика по категориям")
        window.geometry("1200x550")
        fig = Visualizer._plot_bar(pairs, "Частота встречаемости категорий", "Категория", "#3498db")  # приятный синий
        canvas = FigureCanvasTkAgg(fig, master=window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    @staticmethod
    def visualize_keywords(pairs):
        if not pairs:
            print("Нет данных по ключевым словам для визуализации.")
            return
        root = Visualizer._get_root()
        window = tk.Toplevel(root)
        window.title("Статистика по ключевым словам")
        window.geometry("850x550")
        fig = Visualizer._plot_bar(pairs, "Частота встречаемости ключевых слов", "Ключевое слово", "#e67e22")  # тёплый оранжевый
        canvas = FigureCanvasTkAgg(fig, master=window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        window.mainloop()

    @staticmethod
    def start():
        if Visualizer._root:
            Visualizer._root.mainloop()