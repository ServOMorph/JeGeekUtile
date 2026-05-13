import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from core import anonymizer


def test_anonymize_email_address_basic():
    result = anonymizer.anonymize_email_address('john.doe@example.com')
    assert '@' in result
    assert 'john.doe' not in result
    assert 'example.com' not in result


def test_anonymize_email_address_no_email():
    result = anonymizer.anonymize_email_address('no-email-here')
    assert result == '***@***.***'


def test_anonymize_from_with_name():
    result = anonymizer.anonymize_from('Jean Dupont <jean@example.com>')
    assert 'Jean Dupont' not in result
    assert 'jean@example.com' not in result
    assert '@' in result


def test_anonymize_from_email_only():
    result = anonymizer.anonymize_from('jean@example.com')
    assert 'jean' not in result or result.startswith('j***')


def test_anonymize_body_removes_emails():
    body = 'Bonjour user@example.com, votre commande est prête.'
    result = anonymizer.anonymize_body(body)
    assert 'user@example.com' not in result
    assert 'Bonjour' in result


def test_anonymize_body_removes_phones():
    body = 'Appelez-nous au 01 23 45 67 89 pour plus d\'info.'
    result = anonymizer.anonymize_body(body)
    assert '[TÉLÉPHONE ANONYMISÉ]' in result


def test_anonymize_body_no_false_positive():
    body = 'Version 3.0 disponible. Prix : 12.50€'
    result = anonymizer.anonymize_body(body)
    assert 'Version 3.0' in result


def test_anonymize_analysis_sets_flag():
    analysis = {
        'uid': '42',
        'headers': {'from': 'user@example.com', 'reply_to': 'other@example.com', 'message_id': '<abc@mail.com>'},
        'score': 50,
        'body_preview': 'Contact: admin@test.com'
    }
    result = anonymizer.anonymize_analysis(analysis)
    assert result['anonymized'] is True
    assert 'user@example.com' not in result['headers']['from']
    assert result['headers']['message_id'] == '[ANONYMISÉ]'


def test_anonymize_analysis_preserves_score():
    analysis = {
        'uid': '1',
        'headers': {'from': 'a@b.com', 'reply_to': '', 'message_id': ''},
        'score': 75,
        'body_preview': ''
    }
    result = anonymizer.anonymize_analysis(analysis)
    assert result['score'] == 75


def test_anonymize_analysis_does_not_mutate_original():
    analysis = {
        'uid': '1',
        'headers': {'from': 'user@example.com', 'reply_to': '', 'message_id': '<x>'},
        'score': 30,
        'body_preview': 'test@email.com'
    }
    original_from = analysis['headers']['from']
    anonymizer.anonymize_analysis(analysis)
    assert analysis['headers']['from'] == original_from
