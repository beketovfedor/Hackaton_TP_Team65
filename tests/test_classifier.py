from src.analyzer.classifier import MailClassifier


def test_classify_unreadable(classifier_with_config):
    result = classifier_with_config.classify(None)
    assert result["category"] == "unreadable"
    assert result["category_score"] == 0


def test_classify_by_body_keyword(classifier_with_config):
    mail = {
        "mail_name": "mail_1.txt",
        "mail_theme": "",
        "mail_txt": "помогите пожалуйста не работает система",
    }
    result = classifier_with_config.classify(mail)
    assert result["category"] == "support"
    assert "помогите" in result["matched_keywords"]


def test_classify_by_theme_keyword_with_weight(classifier_with_config):
    mail = {
        "mail_name": "mail_2.txt",
        "mail_theme": "срочно ошибка",
        "mail_txt": "",
    }
    result = classifier_with_config.classify(mail)
    assert result["category"] == "critical"
    assert result["category_score"] == 4
    assert result["theme_matches_count"] == 2


def test_classify_other_if_no_keywords(classifier_with_config):
    mail = {
        "mail_name": "mail_3.txt",
        "mail_theme": "обычное письмо",
        "mail_txt": "информация без ключевых слов",
    }
    result = classifier_with_config.classify(mail)
    assert result["category"] == "other"
    assert result["category_score"] == 0


def test_priority_used_when_scores_are_equal(classifier_with_config):
    mail = {
        "mail_name": "mail_4.txt",
        "mail_theme": "",
        "mail_txt": "ошибка проблема",
    }
    result = classifier_with_config.classify(mail)
    assert result["category"] == "critical"
