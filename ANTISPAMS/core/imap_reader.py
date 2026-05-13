import imaplib
import email
import json
import os
from email.header import decode_header
from email.utils import parsedate_to_datetime


def _load_config():
    config_path = os.path.join(os.path.dirname(__file__), '..', 'donnees', 'config.json')
    config_path = os.path.abspath(config_path)
    if not os.path.exists(config_path):
        raise FileNotFoundError(
            f"Config manquante: {config_path}\n"
            "Copiez donnees/config.example.json vers donnees/config.json et remplissez vos identifiants."
        )
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def _decode_header_value(value):
    if value is None:
        return ''
    parts = decode_header(value)
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


def connect():
    cfg = _load_config()
    imap_cfg = cfg.get('imap', {})
    host = imap_cfg.get('host', 'imap.free.fr')
    port = imap_cfg.get('port', 993)
    ssl = imap_cfg.get('ssl', True)
    user = imap_cfg.get('user', '')
    password = imap_cfg.get('password', '')

    if ssl:
        conn = imaplib.IMAP4_SSL(host, port)
    else:
        conn = imaplib.IMAP4(host, port)

    conn.login(user, password)
    return conn


def list_emails(limit=50):
    conn = connect()
    try:
        conn.select('INBOX', readonly=True)
        status, data = conn.search(None, 'ALL')
        if status != 'OK':
            return []

        uids = data[0].split()
        uids = uids[-limit:]
        uids.reverse()

        emails = []
        for uid in uids:
            status, msg_data = conn.fetch(uid, '(RFC822.SIZE BODY.PEEK[HEADER.FIELDS (FROM SUBJECT DATE LIST-UNSUBSCRIBE)])')
            if status != 'OK':
                continue

            raw_headers = msg_data[0][1]
            msg = email.message_from_bytes(raw_headers)

            emails.append({
                'uid': uid.decode(),
                'from': _decode_header_value(msg.get('From', '')),
                'subject': _decode_header_value(msg.get('Subject', '(sans objet)')),
                'date': msg.get('Date', ''),
                'list_unsubscribe': msg.get('List-Unsubscribe', ''),
                'size': int(msg_data[0][0].split()[2]) if len(msg_data[0]) > 1 else 0
            })
        return emails
    finally:
        conn.logout()


def fetch_email_full(uid):
    conn = connect()
    try:
        conn.select('INBOX', readonly=True)
        status, msg_data = conn.fetch(uid.encode(), '(RFC822)')
        if status != 'OK' or not msg_data or not msg_data[0]:
            return None
        raw = msg_data[0][1]
        msg = email.message_from_bytes(raw)
        return msg
    finally:
        conn.logout()


def get_email_body(msg):
    body_html = ''
    body_text = ''
    if msg.is_multipart():
        for part in msg.walk():
            ct = part.get_content_type()
            disp = str(part.get('Content-Disposition', ''))
            if 'attachment' in disp:
                continue
            if ct == 'text/html':
                charset = part.get_content_charset() or 'utf-8'
                body_html = part.get_payload(decode=True).decode(charset, errors='replace')
            elif ct == 'text/plain' and not body_text:
                charset = part.get_content_charset() or 'utf-8'
                body_text = part.get_payload(decode=True).decode(charset, errors='replace')
    else:
        ct = msg.get_content_type()
        charset = msg.get_content_charset() or 'utf-8'
        payload = msg.get_payload(decode=True)
        if payload:
            decoded = payload.decode(charset, errors='replace')
            if ct == 'text/html':
                body_html = decoded
            else:
                body_text = decoded

    return body_html or body_text
