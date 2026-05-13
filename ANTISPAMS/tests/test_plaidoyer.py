import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import json
import pytest
from unittest.mock import patch
from core import plaidoyer


ANALYSIS_HIGH_RISK = {
    'uid': '42',
    'headers': {
        'from': 'spam@bulk.xyz',
        'subject': 'PROMO !!!',
        'date': 'Mon, 01 Jan 2024 10:00:00 +0000',
        'reply_to': 'bounce@other.com',
        'list_unsubscribe': '',
    },
    'score': 75,
    'score_label': 'danger',
    'criteria': [
        {'id': 'tracking_pixel', 'label': 'Pixel de tracking détecté', 'points': 20, 'description': 'Image 1x1', 'triggered': True},
        {'id': 'no_optout', 'label': 'Pas de lien désabonnement', 'points': 25, 'description': 'Absent', 'triggered': True},
        {'id': 'no_list_unsubscribe', 'label': 'Header absent', 'points': 15, 'description': 'Absent', 'triggered': True},
        {'id': 'tracking_links', 'label': 'Liens tracking', 'points': 20, 'description': 'Présents', 'triggered': False},
        {'id': 'sender_mismatch', 'label': 'Expéditeur suspect', 'points': 10, 'description': 'Mismatch', 'triggered': True},
        {'id': 'no_rgpd_mention', 'label': 'Pas RGPD', 'points': 10, 'description': 'Absent', 'triggered': False},
    ],
    'is_bulk': True,
}

ANALYSIS_CLEAN = {
    **ANALYSIS_HIGH_RISK,
    'uid': '1',
    'score': 0,
    'score_label': 'ok',
    'criteria': [
        {**c, 'triggered': False} for c in ANALYSIS_HIGH_RISK['criteria']
    ]
}


def test_generate_requires_validation():
    result = plaidoyer.generate(ANALYSIS_HIGH_RISK, validated=False)
    assert 'error' in result
    assert 'Validation' in result['error']


def test_generate_creates_files(tmp_path):
    with patch('core.plaidoyer.RAPPORTS_DIR', str(tmp_path)):
        result = plaidoyer.generate(ANALYSIS_HIGH_RISK, validated=True)
    assert result['success']
    assert os.path.exists(result['md_path'])
    assert os.path.exists(result['json_path'])


def test_generate_md_content(tmp_path):
    with patch('core.plaidoyer.RAPPORTS_DIR', str(tmp_path)):
        result = plaidoyer.generate(ANALYSIS_HIGH_RISK, validated=True)
    with open(result['md_path'], 'r', encoding='utf-8') as f:
        content = f.read()
    assert 'Plaidoyer RGPD' in content
    assert '75/100' in content
    assert 'HAUT RISQUE' in content
    assert 'spam@bulk.xyz' in content


def test_generate_json_content(tmp_path):
    with patch('core.plaidoyer.RAPPORTS_DIR', str(tmp_path)):
        result = plaidoyer.generate(ANALYSIS_HIGH_RISK, validated=True)
    with open(result['json_path'], 'r', encoding='utf-8') as f:
        data = json.load(f)
    assert data['analysis']['score'] == 75
    assert data['analysis']['risk_level'] == 'high'
    assert data['human_validated'] is True
    assert len(data['analysis']['violations']) == 4


def test_generate_clean_analysis(tmp_path):
    with patch('core.plaidoyer.RAPPORTS_DIR', str(tmp_path)):
        result = plaidoyer.generate(ANALYSIS_CLEAN, validated=True)
    assert result['triggered_count'] == 0


def test_list_rapports_empty(tmp_path):
    with patch('core.plaidoyer.RAPPORTS_DIR', str(tmp_path)):
        rapports = plaidoyer.list_rapports()
    assert rapports == []


def test_list_rapports_with_files(tmp_path):
    sample = {
        'generated_at': '2024-01-01T10:00:00',
        'analysis': {'score': 75, 'risk_level': 'high'},
        'email': {'from': 'test@test.com', 'subject': 'Test'}
    }
    with open(tmp_path / '20240101_test_42.json', 'w') as f:
        json.dump(sample, f)
    with patch('core.plaidoyer.RAPPORTS_DIR', str(tmp_path)):
        rapports = plaidoyer.list_rapports()
    assert len(rapports) == 1
    assert rapports[0]['score'] == 75


def test_get_rapport_returns_none_missing(tmp_path):
    with patch('core.plaidoyer.RAPPORTS_DIR', str(tmp_path)):
        result = plaidoyer.get_rapport('nonexistent.json')
    assert result is None


def test_get_rapport_returns_content(tmp_path):
    sample = {'test': 'data'}
    with open(tmp_path / 'test.json', 'w') as f:
        json.dump(sample, f)
    with patch('core.plaidoyer.RAPPORTS_DIR', str(tmp_path)):
        result = plaidoyer.get_rapport('test.json')
    assert result == {'test': 'data'}
