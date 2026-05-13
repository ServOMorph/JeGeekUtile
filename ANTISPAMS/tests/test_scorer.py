import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from core.scorer import score_email, score_label, get_triggered_criteria, _extract_domain, _sender_mismatch


HEADERS_CLEAN = {'from': 'Legit Shop <legit@example.com>', 'reply_to': '', 'list_unsubscribe': '<mailto:unsub@example.com>'}
HEADERS_SPAM = {'from': 'PROMO <promo@marketing.xyz>', 'reply_to': 'bounce@other-domain.com', 'list_unsubscribe': ''}

BODY_CLEAN = "Bonjour, cliquez ici pour vous désabonner. Conformément au RGPD."
BODY_SPAM = '<img width="1" height="1" src="https://track.example.com/pixel.gif"> Offre exceptionnelle!'
BODY_TRACKING_LINK = 'Voir notre offre : https://click.mailchimp.com/track?utm_source=email&id=123'
BODY_BULK_NO_RGPD = "Chers abonnés, notre newsletter mensuelle est disponible."


def test_score_clean_email():
    result = score_email(HEADERS_CLEAN, BODY_CLEAN)
    assert result['score'] < 30
    assert not result['criteria']['no_optout']
    assert not result['criteria']['no_list_unsubscribe']


def test_score_pixel_detected():
    result = score_email(HEADERS_SPAM, BODY_SPAM)
    assert result['criteria']['tracking_pixel']


def test_score_no_optout():
    result = score_email(HEADERS_SPAM, BODY_SPAM)
    assert result['criteria']['no_optout']


def test_score_no_list_unsubscribe():
    result = score_email(HEADERS_SPAM, BODY_SPAM)
    assert result['criteria']['no_list_unsubscribe']


def test_score_tracking_links():
    result = score_email(HEADERS_SPAM, BODY_TRACKING_LINK)
    assert result['criteria']['tracking_links']


def test_score_sender_mismatch():
    result = score_email(HEADERS_SPAM, '')
    assert result['criteria']['sender_mismatch']


def test_score_no_rgpd_bulk():
    result = score_email(HEADERS_SPAM, BODY_BULK_NO_RGPD)
    assert result['criteria']['no_rgpd_mention']
    assert result['is_bulk']


def test_score_max_100():
    result = score_email(HEADERS_SPAM, BODY_SPAM + BODY_TRACKING_LINK + BODY_BULK_NO_RGPD)
    assert result['score'] <= 100


def test_score_label_danger():
    assert score_label(75) == 'danger'
    assert score_label(60) == 'danger'


def test_score_label_warning():
    assert score_label(59) == 'warning'
    assert score_label(30) == 'warning'


def test_score_label_ok():
    assert score_label(29) == 'ok'
    assert score_label(0) == 'ok'


def test_extract_domain():
    assert _extract_domain('user@example.com') == 'example.com'
    assert _extract_domain('User Name <user@sub.domain.org>') == 'sub.domain.org'
    assert _extract_domain('no-email') == ''


def test_sender_mismatch_same_domain():
    assert not _sender_mismatch('promo@example.com', 'bounce@example.com')


def test_sender_mismatch_different_domain():
    assert _sender_mismatch('promo@legit.com', 'bounce@other.com')


def test_sender_mismatch_no_reply_to():
    assert not _sender_mismatch('promo@legit.com', '')


def test_get_triggered_criteria_returns_all():
    criteria_results = {
        'tracking_pixel': True, 'no_optout': False, 'no_list_unsubscribe': True,
        'tracking_links': False, 'sender_mismatch': False, 'no_rgpd_mention': False
    }
    result = get_triggered_criteria(criteria_results)
    assert len(result) == 6
    triggered = [c for c in result if c['triggered']]
    assert len(triggered) == 2


def test_score_list_unsubscribe_present():
    headers = {**HEADERS_SPAM, 'list_unsubscribe': '<mailto:unsub@example.com>'}
    result = score_email(headers, '')
    assert not result['criteria']['no_list_unsubscribe']
