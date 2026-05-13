import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import email as email_lib
from unittest.mock import patch, MagicMock, mock_open
import json
import pytest
from core import imap_reader


MOCK_CONFIG = {
    'imap': {
        'host': 'imap.free.fr',
        'port': 993,
        'ssl': True,
        'user': 'test@free.fr',
        'password': 'testpassword'
    }
}


def _make_raw_headers(from_h, subject, date='Mon, 01 Jan 2024 10:00:00 +0000', list_unsub=''):
    headers = f"From: {from_h}\r\nSubject: {subject}\r\nDate: {date}\r\n"
    if list_unsub:
        headers += f"List-Unsubscribe: {list_unsub}\r\n"
    return headers.encode('utf-8')


@pytest.fixture
def mock_config(tmp_path):
    config_file = tmp_path / 'config.json'
    config_file.write_text(json.dumps(MOCK_CONFIG), encoding='utf-8')
    return str(config_file)


def test_load_config_missing(tmp_path):
    missing = str(tmp_path / 'nonexistent.json')
    with patch('core.imap_reader.os.path.exists', return_value=False):
        with pytest.raises(FileNotFoundError, match='Config manquante'):
            imap_reader._load_config()


def test_decode_header_value_ascii():
    result = imap_reader._decode_header_value('Hello World')
    assert result == 'Hello World'


def test_decode_header_value_none():
    result = imap_reader._decode_header_value(None)
    assert result == ''


def test_decode_header_value_encoded():
    encoded = '=?utf-8?b?SGVsbG8gV29ybGQ=?='
    result = imap_reader._decode_header_value(encoded)
    assert 'Hello World' in result


def test_list_emails_returns_list():
    mock_conn = MagicMock()
    mock_conn.search.return_value = ('OK', [b'1 2 3'])

    raw_headers = _make_raw_headers('sender@test.com', 'Test Email')
    fetch_response = [
        (b'1 (RFC822.SIZE 1024 BODY[HEADER.FIELDS (FROM SUBJECT DATE LIST-UNSUBSCRIBE)] {%d}' % len(raw_headers), raw_headers)
    ]
    mock_conn.fetch.return_value = ('OK', fetch_response)

    with patch('core.imap_reader._load_config', return_value=MOCK_CONFIG), \
         patch('core.imap_reader.connect', return_value=mock_conn):
        mock_conn.select.return_value = ('OK', [b'3'])
        emails = imap_reader.list_emails(limit=10)
    assert isinstance(emails, list)


def test_connect_uses_ssl():
    with patch('core.imap_reader._load_config', return_value=MOCK_CONFIG), \
         patch('imaplib.IMAP4_SSL') as mock_ssl:
        mock_ssl.return_value = MagicMock()
        mock_ssl.return_value.login.return_value = ('OK', [b'Logged in'])
        conn = imap_reader.connect()
        mock_ssl.assert_called_once_with('imap.free.fr', 993)


def test_connect_uses_plain_when_no_ssl():
    cfg = {**MOCK_CONFIG, 'imap': {**MOCK_CONFIG['imap'], 'ssl': False, 'port': 143}}
    with patch('core.imap_reader._load_config', return_value=cfg), \
         patch('imaplib.IMAP4') as mock_plain:
        mock_plain.return_value = MagicMock()
        mock_plain.return_value.login.return_value = ('OK', [b'Logged in'])
        conn = imap_reader.connect()
        mock_plain.assert_called_once_with('imap.free.fr', 143)


def test_get_email_body_plain():
    msg = email_lib.message.Message()
    msg.set_payload('Plain body content')
    msg.set_type('text/plain')
    msg.set_param('charset', 'utf-8')
    body = imap_reader.get_email_body(msg)
    assert 'Plain body content' in body


def test_get_email_body_html():
    msg = email_lib.message.Message()
    msg.set_payload('<html><body>HTML content</body></html>')
    msg.set_type('text/html')
    msg.set_param('charset', 'utf-8')
    body = imap_reader.get_email_body(msg)
    assert 'HTML content' in body


def test_fetch_email_full_returns_none_on_error():
    mock_conn = MagicMock()
    mock_conn.fetch.return_value = ('NO', [])
    with patch('core.imap_reader._load_config', return_value=MOCK_CONFIG), \
         patch('core.imap_reader.connect', return_value=mock_conn):
        mock_conn.select.return_value = ('OK', [b'0'])
        result = imap_reader.fetch_email_full('9999')
    assert result is None
