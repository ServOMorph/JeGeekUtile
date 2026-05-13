from email.header import decode_header as _decode_header_raw
from email.utils import parsedate_to_datetime
from . import imap_reader
from . import scorer


def _decode(value):
    if value is None:
        return ''
    parts = _decode_header_raw(value)
    decoded = []
    for part, charset in parts:
        if isinstance(part, bytes):
            try:
                decoded.append(part.decode(charset or 'utf-8', errors='replace'))
            except (LookupError, UnicodeDecodeError):
                decoded.append(part.decode('latin-1', errors='replace'))
        else:
            decoded.append(part)
    return ' '.join(decoded)


def analyze_email(uid: str) -> dict:
    msg = imap_reader.fetch_email_full(uid)
    if msg is None:
        return {'error': f'Email {uid} introuvable'}

    headers = {
        'from': _decode(msg.get('From', '')),
        'reply_to': _decode(msg.get('Reply-To', '')),
        'subject': _decode(msg.get('Subject', '')),
        'date': msg.get('Date', ''),
        'list_unsubscribe': msg.get('List-Unsubscribe', ''),
        'message_id': msg.get('Message-ID', ''),
        'x_mailer': msg.get('X-Mailer', ''),
        'content_type': msg.get('Content-Type', ''),
    }

    body = imap_reader.get_email_body(msg)
    score_result = scorer.score_email(headers, body)

    criteria_detail = scorer.get_triggered_criteria(score_result['criteria'])

    return {
        'uid': uid,
        'headers': headers,
        'score': score_result['score'],
        'score_label': scorer.score_label(score_result['score']),
        'criteria': criteria_detail,
        'is_bulk': score_result['is_bulk'],
        'body_preview': body[:500] if body else '',
        'has_html': '<html' in body.lower() if body else False,
    }


def quick_score_from_headers(email_meta: dict) -> dict:
    headers = {
        'from': email_meta.get('from', ''),
        'reply_to': '',
        'list_unsubscribe': email_meta.get('list_unsubscribe', ''),
    }
    score_result = scorer.score_email(headers, '')
    return {
        'score': score_result['score'],
        'score_label': scorer.score_label(score_result['score'])
    }
