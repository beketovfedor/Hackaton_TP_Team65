import json
from pathlib import Path
from unittest.mock import patch

import pytest

from src.classifier import MailClassifier
from src.file_manager import FileManager


@pytest.fixture
def sample_categories():
    return {
        "default_category": "other",
        "unreadable_category": "unreadable",
        "min_category_score": 1,
        "theme_weight": 2,
        "categories": {
            "spam": {
                "folder": "spam",
                "title": "Спам",
                "priority": 1,
                "keywords": ["купить", "скидка", "акция", "бесплатно"],
            },
            "critical": {
                "folder": "critical",
                "title": "Критические инциденты",
                "priority": 3,
                "keywords": ["сервер упал", "ошибка", "недоступен", "срочно"],
            },
            "support": {
                "folder": "support",
                "title": "Поддержка",
                "priority": 2,
                "keywords": ["помогите", "не работает", "проблема", "заявка"],
            },
            "other": {
                "folder": "other",
                "title": "Прочее",
                "priority": 0,
                "keywords": [],
            },
            "unreadable": {
                "folder": "unreadable",
                "title": "Нечитаемые",
                "priority": 0,
                "keywords": [],
            },
        },
    }


@pytest.fixture
def classifier_with_config(tmp_path, sample_categories):
    config_dir = tmp_path / "data" / "config"
    config_dir.mkdir(parents=True, exist_ok=True)
    config_file = config_dir / "categories.json"
    config_file.write_text(json.dumps(sample_categories, ensure_ascii=False), encoding="utf-8")

    with patch.object(MailClassifier, "__init__", lambda self: None):
        classifier = MailClassifier.__new__(MailClassifier)
        classifier.config_path = config_file
        classifier.config = sample_categories
        classifier.default_category = sample_categories["default_category"]
        classifier.unreadable_category = sample_categories["unreadable_category"]
        classifier.min_category_score = sample_categories["min_category_score"]
        classifier.theme_weight = sample_categories["theme_weight"]
        classifier.categories = sample_categories["categories"]

    return classifier


@pytest.fixture
def file_manager(tmp_path):
    manager = FileManager.__new__(FileManager)
    manager.processed_dir = tmp_path / "data" / "processed"
    manager.processed_dir.mkdir(parents=True, exist_ok=True)
    return manager
