import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from unittest.mock import patch, MagicMock
import email as email_lib
from core import analyzer


def _make_msg(from_h='sender@test.com', subject='Test', body_html='', body_text='', reply_to='', list_unsub=''):
    msg = email_lib.message.Message()
    msg['From'] = from_h
    msg['Subject'] = subject
    msg['Date'] = 'Mon, 01 Jan 2024 10:00:00 +0000'
    if reply_to:
        msg['Reply-To'] = reply_to
    if list_unsub:
        msg['List-Unsubscribe'] = list_unsub
    if body_html:
        msg.set_payload(body_html)
        msg.set_type('text/html')
        msg.set_param('charset', 'utf-8')
    else:
        msg.set_payload(body_text)
        msg.set_type('text/plain')
        msg.set_param('charset', 'utf-8')
    return msg


def test_analyze_email_structure():
    spam_body = '<img width="1" height="1" src="track.gif"> Newsletter sans désabonnement'
    mock_msg = _make_msg(
        from_h='promo@spam.xyz',
        subject='Promo !!!',
        body_html=spam_body,
        reply_to='bounce@other.com'
    )
    with patch('core.analyzer.imap_reader.fetch_email_full', return_value=mock_msg), \
         patch('core.analyzer.imap_reader.get_email_body', return_value=spam_body):
        result = analyzer.analyze_email('42')
    assert result['uid'] == '42'
    assert 'score' in result
    assert 'criteria' in result
    assert 'headers' in result
    assert isinstance(result['criteria'], list)
    assert len(result['criteria']) == 6


def test_analyze_email_not_found():
    with patch('core.analyzer.imap_reader.fetch_email_full', return_value=None):
        result = analyzer.analyze_email('99999')
    assert 'error' in result


def test_analyze_email_high_score():
    spam_body = (
        '<img width="1" height="1" src="https://mailtrack.io/trace/pixel.gif">'
        'Chers abonnés, offre exceptionnelle !'
        '<a href="https://click.mailchimp.com/track?utm_source=email">voir</a>'
    )
    mock_msg = _make_msg(
        from_h='spam@bulk.com',
        subject='Newsletter',
        body_html=spam_body,
        reply_to='bounce@other-domain.com'
    )
    with patch('core.analyzer.imap_reader.fetch_email_full', return_value=mock_msg), \
         patch('core.analyzer.imap_reader.get_email_body', return_value=spam_body):
        result = analyzer.analyze_email('1')
    assert result['score'] >= 60
    assert result['score_label'] == 'danger'


def test_analyze_email_low_score():
    clean_body = 'Bonjour, merci. Cliquez ici pour vous désabonner. RGPD - protection des données.'
    mock_msg = _make_msg(
        from_h='contact@association.org',
        subject='Info',
        body_text=clean_body,
        list_unsub='<mailto:unsub@association.org>'
    )
    with patch('core.analyzer.imap_reader.fetch_email_full', return_value=mock_msg), \
         patch('core.analyzer.imap_reader.get_email_body', return_value=clean_body):
        result = analyzer.analyze_email('2')
    assert result['score'] < 30
    assert result['score_label'] == 'ok'


def test_quick_score_from_headers_no_list_unsub():
    meta = {'from': 'promo@spam.com', 'reply_to': '', 'list_unsubscribe': ''}
    result = analyzer.quick_score_from_headers(meta)
    assert 'score' in result
    assert 'score_label' in result
    assert result['score'] >= 15


def test_quick_score_from_headers_with_list_unsub():
    meta = {'from': 'info@legit.org', 'reply_to': '', 'list_unsubscribe': '<mailto:unsub@legit.org>'}
    result = analyzer.quick_score_from_headers(meta)
    assert result['score'] == 25
