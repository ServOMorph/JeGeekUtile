#!/usr/bin/env python3
import json
import os
from datetime import datetime
from pathlib import Path
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

BASE_DIR = Path(__file__).parent
DONNEES_DIR = BASE_DIR / 'donnees'
IAS_FILE = DONNEES_DIR / 'ias.json'
CLICS_FILE = DONNEES_DIR / 'clics.json'

DONNEES_DIR.mkdir(exist_ok=True)

def load_json(filepath, default):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return default

def save_json(filepath, data):
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

@app.route('/')
def index():
    return send_from_directory(BASE_DIR, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory(BASE_DIR, path)

@app.route('/donnees/<path:path>')
def serve_donnees(path):
    return send_from_directory(DONNEES_DIR, path)

@app.route('/api/ia', methods=['GET', 'POST'])
def gestion_ias():
    if request.method == 'GET':
        data = load_json(IAS_FILE, {'ias': []})
        return jsonify(data)

    elif request.method == 'POST':
        data = load_json(IAS_FILE, {'ias': []})

        ia_data = request.json
        ia_id = ia_data['nom'].lower().replace(' ', '_')

        if any(ia['id'] == ia_id for ia in data['ias']):
            return jsonify({'error': 'IA déjà existante'}), 400

        nouvelle_ia = {
            'id': ia_id,
            'nom': ia_data['nom'],
            'type': ia_data['type']
        }

        data['ias'].append(nouvelle_ia)
        save_json(IAS_FILE, data)

        return jsonify({'success': True, 'ia': nouvelle_ia}), 201

@app.route('/api/ia/<ia_id>', methods=['DELETE'])
def supprimer_ia(ia_id):
    data_ias = load_json(IAS_FILE, {'ias': []})
    data_ias['ias'] = [ia for ia in data_ias['ias'] if ia['id'] != ia_id]
    save_json(IAS_FILE, data_ias)

    data_clics = load_json(CLICS_FILE, {'clics': []})
    data_clics['clics'] = [c for c in data_clics['clics'] if c['ia_id'] != ia_id]
    save_json(CLICS_FILE, data_clics)

    return jsonify({'success': True})

@app.route('/api/clic', methods=['POST'])
def enregistrer_clic():
    data = load_json(CLICS_FILE, {'clics': []})

    clic_data = request.json
    ia_id = clic_data['ia_id']

    ias = load_json(IAS_FILE, {'ias': []})
    ia = next((i for i in ias['ias'] if i['id'] == ia_id), None)

    if not ia:
        return jsonify({'error': 'IA non trouvée'}), 404

    nouveau_clic = {
        'ia_id': ia_id,
        'timestamp': datetime.now().isoformat(),
        'type': ia['type']
    }

    data['clics'].append(nouveau_clic)
    save_json(CLICS_FILE, data)

    return jsonify({'success': True, 'clic': nouveau_clic}), 201

@app.route('/api/stats')
def statistiques():
    ias = load_json(IAS_FILE, {'ias': []})
    clics = load_json(CLICS_FILE, {'clics': []})

    total_clics = len(clics['clics'])
    clics_locaux = sum(1 for c in clics['clics'] if c['type'] == 'local')
    clics_cloud = total_clics - clics_locaux

    ratio_local = round((clics_locaux / total_clics * 100), 1) if total_clics > 0 else 0

    stats_par_ia = {}
    for ia in ias['ias']:
        ia_clics = [c for c in clics['clics'] if c['ia_id'] == ia['id']]
        stats_par_ia[ia['id']] = {
            'nom': ia['nom'],
            'type': ia['type'],
            'clics': len(ia_clics),
            'pct': round((len(ia_clics) / total_clics * 100), 1) if total_clics > 0 else 0
        }

    return jsonify({
        'total_clics': total_clics,
        'clics_locaux': clics_locaux,
        'clics_cloud': clics_cloud,
        'ratio_local': ratio_local,
        'objectif_atteint': ratio_local >= 70,
        'par_ia': stats_par_ia
    })

if __name__ == '__main__':
    if not IAS_FILE.exists():
        save_json(IAS_FILE, {'ias': []})
    if not CLICS_FILE.exists():
        save_json(CLICS_FILE, {'clics': []})

    print("\n" + "="*60)
    print("Tracker Usage IA - Serveur démarré")
    print("="*60)
    print("URL: http://localhost:5000")
    print("="*60 + "\n")

    app.run(host='0.0.0.0', port=5000, debug=True)
