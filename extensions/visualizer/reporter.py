from graphs import *


class Reporter:
    category_counter = {} #пары: категория -> количество
    keywords_counter = {} #пары: ключевое слово -> количество
    total_amount_of_letters = 0

    @staticmethod
    def add_category(category: str) -> None:
        if category in Reporter.category_counter:
            Reporter.category_counter[category] += 1
        else:
            Reporter.category_counter[category] = 1
        Reporter.total_amount_of_letters+=1

    @staticmethod
    def add_keywords(word_list: list) -> None:
        word_list = set(word_list)
        for word in word_list:
            if word in Reporter.keywords_counter:
                Reporter.keywords_counter[word] += 1
            else:
                Reporter.keywords_counter[word] = 1

    @staticmethod
    def create_report(filename: str = "report.txt") -> None:
        # Сортировка категорий и слов сначала по значению (убывание), затем по ключу (возрастание)
        sorted_categories = sorted(
            Reporter.category_counter.items(),
            key=lambda item: (-item[1], item[0])
        )

        sorted_keywords = sorted(
            Reporter.keywords_counter.items(),
            key=lambda item: (-item[1], item[0])
        )

        with open(filename, 'w', encoding='utf-8') as f:
            f.write("ОТЧЁТ О КЛАССИФИКАЦИИ ПИСЕМ\n")
            f.write(f"Всего обработано файлов: {Reporter.total_amount_of_letters}\n")
            f.write("--- Распределение по категориям ---\n")
            if not sorted_categories:
                f.write("No categories recorded.\n")
            else:
                for category, count in sorted_categories:
                    percent = (count / Reporter.total_amount_of_letters) * 100
                    f.write(f"{category}: {count} писем ({percent:5.1f}%)\n")
            f.write("\n--- Число уникальных писем с ключевыми словами ---\n")
            if not sorted_keywords:
                f.write("No keywords recorded.\n")
            else:
                k = 0
                for keyword, count in sorted_keywords:
                    k+=1
                    percent = (count / Reporter.total_amount_of_letters) * 100
                    f.write(f"{keyword}: {count} писем ({percent:5.1f}%)\n")
                    if k == 20:
                        break

if __name__ == "__main__":
    # Добавляем тестовые данные для категорий
    Reporter.add_category("news")
    Reporter.add_category("sports")
    Reporter.add_category("news")
    Reporter.add_category("technology")
    Reporter.add_category("science")
    Reporter.add_category("sports")
    Reporter.add_category("sports")
    Reporter.add_category("news")

    # Добавляем тестовые данные для ключевых слов
    Reporter.add_keywords(["python", "code", "python", "data", "AI", "machine learning"])
    Reporter.add_keywords(["code", "python", "deep learning", "AI", "data"])
    Reporter.add_keywords(["java", "python", "code", "code"])

    # Создаём текстовый отчёт (опционально, для демонстрации)
    Reporter.create_report("test_report.txt")
    print("Текстовый отчёт сохранён в test_report.txt")

    # Визуализируем категории (откроется отдельное окно)
    Visualizer.visualize_categories(Reporter.category_counter)

    # После закрытия окна категорий откроется окно ключевых слов
    Visualizer.visualize_keywords(Reporter.keywords_counter)