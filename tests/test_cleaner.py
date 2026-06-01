import pytest
import src.cleaner
from src.cleaner import clean_text, process_raw_email, translit_to_cyrillic, _extract_fields

@pytest.fixture(autouse=True)
def mock_cleaner_stopwords():
    old_rubbish = cleaner.rubbish
    cleaner.rubbish = {"и", "в", "на", "the", "a"}
    yield
    cleaner.rubbish = old_rubbish

class TestCleaner:

    def test_clean_text_lowercases(self):
        res = clean_text("HELLO WORLD", remove_stopwords=False)
        assert res == "hello world"

    def test_clean_text_removes_urls(self):
        out = clean_text("заходи на http://127.0.0.1:8000/api/v1/user/profile короче", remove_stopwords=False)
        assert "http" not in out
        assert "127.0.0.1" not in out

    def test_clean_text_removes_emails(self):
        res = clean_text("пиши мне на test_work_acc@my-company.com если что", remove_stopwords=False)
        assert "@" not in res

    def test_clean_text_empty_string(self):
        assert clean_text("") == ""

    def test_clean_text_none(self):
        assert clean_text(None) == ""

    def test_extract_fields_subject(self):
        raw_data = "Subject: Какая-то проблема\n\nНадо срочно пофиксить баг"
        fields = _extract_fields(raw_data)
        assert fields["subject"] == "Какая-то проблема"
        assert "пофиксить баг" in fields["body"]

    def test_extract_fields_russian_headers(self):
        raw_msg = "Тема: Срочно\nОт: boss@corp.ru\n\nТекст письма"
        res = _extract_fields(raw_msg)
        assert res["subject"] == "Срочно"
        assert res["from"] == "boss@corp.ru"

    def test_process_raw_email_returns_dict(self):
        raw = "Subject: Тестовый заголовок\n\nКакое-то тело письма"
        result = process_raw_email(raw, "some_test_file.txt")
        assert isinstance(result, dict)
        assert "mail_name" in result
        assert "mail_theme" in result
        assert "mail_txt" in result
        assert result["mail_name"] == "some_test_file.txt"

    def test_translit_to_cyrillic_basic(self):
        out = translit_to_cyrillic("privet drug")
        assert "привет" in out
