import re


CRITERIA = [
    {
        'id': 'tracking_pixel',
        'label': 'Pixel de tracking détecté',
        'points': 20,
        'description': 'Image 1x1 ou URL de tracking dans le HTML'
    },
    {
        'id': 'no_optout',
        'label': 'Pas de lien de désabonnement',
        'points': 25,
        'description': 'Absence de lien unsubscribe / désabonnement dans le contenu'
    },
    {
        'id': 'no_list_unsubscribe',
        'label': 'Header List-Unsubscribe absent',
        'points': 15,
        'description': 'Le header RFC 2369 List-Unsubscribe est manquant'
    },
    {
        'id': 'tracking_links',
        'label': 'Liens de tracking détectés',
        'points': 20,
        'description': 'URLs contenant des domaines ou paramètres de tracking connus'
    },
    {
        'id': 'sender_mismatch',
        'label': 'Expéditeur suspect (From/Reply-To divergent)',
        'points': 10,
        'description': 'Le domaine From et Reply-To ne correspondent pas'
    },
    {
        'id': 'no_rgpd_mention',
        'label': 'Aucune mention RGPD / données personnelles',
        'points': 10,
        'description': 'Absence de mention légale RGPD/GDPR dans un email en masse'
    },
]

TRACKING_PIXEL_RE = re.compile(
    r'<img[^>]+(?:width=["\']?1["\']?[^>]*height=["\']?1["\']?|height=["\']?1["\']?[^>]*width=["\']?1["\']?)[^>]*>',
    re.IGNORECASE
)

TRACKING_PIXEL_SRC_RE = re.compile(
    r'<img[^>]+src=["\'][^"\']*(?:pixel|track|beacon|open|click|stat)[^"\']*["\']',
    re.IGNORECASE
)

OPTOUT_RE = re.compile(
    r'(?:unsubscribe|désabonn|desabonn|opt[-\s]?out|se désinscrire|se desinscrire|retirer|supprimer.*liste)',
    re.IGNORECASE
)

TRACKING_LINK_DOMAINS_RE = re.compile(
    r'https?://[^"\'>\s]*(?:mailtrack|click\.|track\.|pixel\.|beacon\.|trk\.|bnc\.|etracker|sendgrid|mailchimp|klaviyo|hubspot|exacttarget|salesforce\.com/track|mandrillapp)',
    re.IGNORECASE
)

TRACKING_PARAMS_RE = re.compile(
    r'https?://[^"\'>\s]*[?&](?:utm_|mc_eid|fbclid|gclid|mkt_tok)[^"\'>\s]*',
    re.IGNORECASE
)

RGPD_RE = re.compile(
    r'(?:RGPD|GDPR|données personnelles|données à caractère personnel|protection des données|politique de confidentialité|privacy policy)',
    re.IGNORECASE
)

BULK_INDICATORS_RE = re.compile(
    r'(?:newsletter|bulletin|mailing|destinataires|abonnés|liste|diffusion)',
    re.IGNORECASE
)


def score_email(headers: dict, body: str) -> dict:
    results = {}
    total = 0

    has_pixel = bool(TRACKING_PIXEL_RE.search(body)) or bool(TRACKING_PIXEL_SRC_RE.search(body))
    results['tracking_pixel'] = has_pixel
    if has_pixel:
        total += 20

    has_optout = bool(OPTOUT_RE.search(body))
    results['no_optout'] = not has_optout
    if not has_optout:
        total += 25

    list_unsub = headers.get('list_unsubscribe', '').strip()
    results['no_list_unsubscribe'] = not bool(list_unsub)
    if not list_unsub:
        total += 15

    has_tracking_links = bool(TRACKING_LINK_DOMAINS_RE.search(body)) or bool(TRACKING_PARAMS_RE.search(body))
    results['tracking_links'] = has_tracking_links
    if has_tracking_links:
        total += 20

    from_addr = headers.get('from', '')
    reply_to = headers.get('reply_to', '')
    mismatch = _sender_mismatch(from_addr, reply_to)
    results['sender_mismatch'] = mismatch
    if mismatch:
        total += 10

    is_bulk = bool(BULK_INDICATORS_RE.search(body))
    has_rgpd = bool(RGPD_RE.search(body))
    no_rgpd = is_bulk and not has_rgpd
    results['no_rgpd_mention'] = no_rgpd
    if no_rgpd:
        total += 10

    return {
        'score': min(total, 100),
        'criteria': results,
        'is_bulk': is_bulk
    }


def _extract_domain(addr: str) -> str:
    match = re.search(r'@([\w.-]+)', addr)
    return match.group(1).lower() if match else ''


def _sender_mismatch(from_addr: str, reply_to: str) -> bool:
    if not reply_to:
        return False
    from_domain = _extract_domain(from_addr)
    reply_domain = _extract_domain(reply_to)
    if not from_domain or not reply_domain:
        return False
    return from_domain != reply_domain


def score_label(score: int) -> str:
    if score >= 60:
        return 'danger'
    if score >= 30:
        return 'warning'
    return 'ok'


def get_triggered_criteria(criteria_results: dict) -> list:
    triggered = []
    for c in CRITERIA:
        if criteria_results.get(c['id']):
            triggered.append({
                'id': c['id'],
                'label': c['label'],
                'points': c['points'],
                'description': c['description'],
                'triggered': True
            })
        else:
            triggered.append({
                'id': c['id'],
                'label': c['label'],
                'points': c['points'],
                'description': c['description'],
                'triggered': False
            })
    return triggered
