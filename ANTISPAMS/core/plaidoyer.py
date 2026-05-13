import json
import os
import re
from datetime import datetime


RAPPORTS_DIR = os.path.join(os.path.dirname(__file__), '..', 'donnees', 'rapports')


def _safe_filename(uid: str) -> str:
    uid_clean = re.sub(r'[^\w-]', '_', uid)
    date_str = datetime.now().strftime('%Y%m%d_%H%M%S')
    return f"{date_str}_{uid_clean}"


def generate(analysis: dict, validated: bool = False) -> dict:
    if not validated:
        return {'error': 'Validation humaine requise avant génération du plaidoyer'}

    uid = analysis.get('uid', 'unknown')
    score = analysis.get('score', 0)
    headers = analysis.get('headers', {})
    criteria = analysis.get('criteria', [])
    triggered = [c for c in criteria if c.get('triggered')]

    now = datetime.now()
    filename_base = _safe_filename(uid)

    recommendations = _build_recommendations(triggered)
    md_content = _build_markdown(uid, score, headers, triggered, recommendations, now)
    json_content = _build_json(uid, score, headers, triggered, recommendations, now)

    os.makedirs(RAPPORTS_DIR, exist_ok=True)

    md_path = os.path.join(RAPPORTS_DIR, f"{filename_base}.md")
    json_path = os.path.join(RAPPORTS_DIR, f"{filename_base}.json")

    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(md_content)

    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(json_content, f, ensure_ascii=False, indent=2)

    return {
        'success': True,
        'md_path': md_path,
        'json_path': json_path,
        'filename': filename_base,
        'triggered_count': len(triggered),
        'score': score
    }


def _build_recommendations(triggered: list) -> list:
    recs = []
    ids = {c['id'] for c in triggered}

    if 'tracking_pixel' in ids:
        recs.append("Signaler l'usage de pixels de tracking invisibles (violation art. 5 RGPD - transparence)")
    if 'no_optout' in ids:
        recs.append("Exiger l'ajout d'un lien de désabonnement fonctionnel (obligation légale - art. 21 RGPD)")
    if 'no_list_unsubscribe' in ids:
        recs.append("Réclamer l'implémentation du header List-Unsubscribe (RFC 2369 / bonne pratique email)")
    if 'tracking_links' in ids:
        recs.append("Demander suppression des liens de tracking comportemental (art. 22 RGPD)")
    if 'sender_mismatch' in ids:
        recs.append("Signaler la divergence From/Reply-To comme pratique trompeuse (art. 7 RGPD - loyauté)")
    if 'no_rgpd_mention' in ids:
        recs.append("Exiger l'ajout de mentions légales RGPD obligatoires (art. 13-14 RGPD)")

    if not recs:
        recs.append("Aucune violation majeure détectée — conserver ce modèle comme référence conforme")

    return recs


def _build_markdown(uid, score, headers, triggered, recommendations, now):
    date_str = now.strftime('%d/%m/%Y %H:%M')
    lines = [
        f"# Plaidoyer RGPD — Email UID {uid}",
        f"",
        f"**Date de génération** : {date_str}",
        f"**Score de risque** : {score}/100",
        f"**Statut** : {'🔴 HAUT RISQUE' if score >= 60 else '🟡 RISQUE MODÉRÉ' if score >= 30 else '🟢 CONFORME'}",
        f"",
        f"---",
        f"",
        f"## Métadonnées de l'email",
        f"",
        f"| Champ | Valeur |",
        f"|-------|--------|",
        f"| Expéditeur | `{headers.get('from', 'N/A')}` |",
        f"| Sujet | `{headers.get('subject', 'N/A')}` |",
        f"| Date | `{headers.get('date', 'N/A')}` |",
        f"| Reply-To | `{headers.get('reply_to', '(absent)')}` |",
        f"| List-Unsubscribe | `{headers.get('list_unsubscribe', '(absent)')}` |",
        f"",
        f"---",
        f"",
        f"## Violations RGPD détectées ({len(triggered)} critère(s))",
        f"",
    ]

    if triggered:
        for c in triggered:
            lines.append(f"### {c['label']} (+{c['points']} pts)")
            lines.append(f"")
            lines.append(f"{c['description']}")
            lines.append(f"")
    else:
        lines.append("Aucune violation détectée.")
        lines.append("")

    lines += [
        f"---",
        f"",
        f"## Recommandations",
        f"",
    ]
    for rec in recommendations:
        lines.append(f"- {rec}")

    lines += [
        f"",
        f"---",
        f"",
        f"## Validation humaine",
        f"",
        f"- [ ] Contenu vérifié manuellement",
        f"- [ ] Données personnelles anonymisées si nécessaire",
        f"- [ ] Export autorisé par le responsable du traitement",
        f"",
        f"---",
        f"",
        f"*Généré par AntiSpams v1.0 — @Je Geek Utile*",
    ]

    return '\n'.join(lines)


def _build_json(uid, score, headers, triggered, recommendations, now):
    return {
        'generated_at': now.isoformat(),
        'version': '1.0',
        'email': {
            'uid': uid,
            'from': headers.get('from', ''),
            'subject': headers.get('subject', ''),
            'date': headers.get('date', ''),
            'reply_to': headers.get('reply_to', ''),
            'list_unsubscribe': headers.get('list_unsubscribe', ''),
        },
        'analysis': {
            'score': score,
            'risk_level': 'high' if score >= 60 else 'medium' if score >= 30 else 'low',
            'violations': [
                {
                    'id': c['id'],
                    'label': c['label'],
                    'points': c['points'],
                    'description': c['description']
                }
                for c in triggered
            ],
        },
        'recommendations': recommendations,
        'human_validated': True,
        'tool': 'AntiSpams v1.0 — JeGeekUtile'
    }


def list_rapports() -> list:
    os.makedirs(RAPPORTS_DIR, exist_ok=True)
    rapports = []
    for fname in sorted(os.listdir(RAPPORTS_DIR), reverse=True):
        if fname.endswith('.json'):
            fpath = os.path.join(RAPPORTS_DIR, fname)
            try:
                with open(fpath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                rapports.append({
                    'filename': fname,
                    'generated_at': data.get('generated_at', ''),
                    'score': data.get('analysis', {}).get('score', 0),
                    'risk_level': data.get('analysis', {}).get('risk_level', ''),
                    'from': data.get('email', {}).get('from', ''),
                    'subject': data.get('email', {}).get('subject', ''),
                })
            except (json.JSONDecodeError, KeyError):
                continue
    return rapports


def get_rapport(filename: str) -> dict | None:
    fpath = os.path.join(RAPPORTS_DIR, filename)
    if not os.path.exists(fpath):
        return None
    with open(fpath, 'r', encoding='utf-8') as f:
        return json.load(f)
