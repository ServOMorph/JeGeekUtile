import re


EMAIL_RE = re.compile(r'[\w.+-]+@[\w.-]+\.[a-zA-Z]{2,}')
NAME_IN_FROM_RE = re.compile(r'^([^<]+)<')
PHONE_RE = re.compile(r'(?:\+\d{1,3}[\s.-]?)?\(?\d{2,4}\)?[\s.-]?\d{2,4}[\s.-]?\d{2,4}[\s.-]?\d{0,4}')


def anonymize_email_address(addr: str) -> str:
    match = EMAIL_RE.search(addr)
    if not match:
        return '***@***.***'
    email = match.group(0)
    local, domain = email.split('@', 1)
    anon_local = local[0] + '***' if len(local) > 1 else '***'
    domain_parts = domain.split('.')
    anon_domain = domain_parts[0][0] + '***.' + domain_parts[-1] if domain_parts else '***'
    return f"{anon_local}@{anon_domain}"


def anonymize_from(from_header: str) -> str:
    name_match = NAME_IN_FROM_RE.match(from_header.strip())
    if name_match:
        name = name_match.group(1).strip()
        anon_name = name[0] + '***' if len(name) > 1 else '***'
        email_match = EMAIL_RE.search(from_header)
        if email_match:
            anon_email = anonymize_email_address(from_header)
            return f"{anon_name} <{anon_email}>"
    return anonymize_email_address(from_header)


def anonymize_body(body: str) -> str:
    body = EMAIL_RE.sub(lambda m: anonymize_email_address(m.group(0)), body)
    body = PHONE_RE.sub('[TÉLÉPHONE ANONYMISÉ]', body)
    return body


def anonymize_analysis(analysis: dict) -> dict:
    import copy
    anon = copy.deepcopy(analysis)

    headers = anon.get('headers', {})
    if headers.get('from'):
        headers['from'] = anonymize_from(headers['from'])
    if headers.get('reply_to'):
        headers['reply_to'] = anonymize_email_address(headers['reply_to'])
    if headers.get('message_id'):
        headers['message_id'] = '[ANONYMISÉ]'

    if anon.get('body_preview'):
        anon['body_preview'] = anonymize_body(anon['body_preview'])

    anon['anonymized'] = True
    return anon
