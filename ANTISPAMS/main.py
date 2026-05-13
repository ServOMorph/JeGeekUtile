import json
import os
import sys

from flask import Flask, jsonify, send_from_directory, request, abort

sys.path.insert(0, os.path.dirname(__file__))

from core import imap_reader, analyzer, plaidoyer, anonymizer, scorer

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RAPPORTS_DIR = os.path.join(BASE_DIR, 'donnees', 'rapports')

app = Flask(__name__, static_folder=BASE_DIR, static_url_path='')


def _load_config():
    config_path = os.path.join(BASE_DIR, 'donnees', 'config.json')
    if not os.path.exists(config_path):
        return None
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)


@app.route('/')
def index():
    return send_from_directory(BASE_DIR, 'index.html')


@app.route('/api/health')
def health():
    cfg = _load_config()
    if cfg is None:
        return jsonify({
            'status': 'error',
            'message': 'Config manquante. Copiez donnees/config.example.json vers donnees/config.json'
        }), 503

    imap_cfg = cfg.get('imap', {})
    return jsonify({
        'status': 'ok',
        'imap_host': imap_cfg.get('host', ''),
        'imap_port': imap_cfg.get('port', 993),
        'imap_ssl': imap_cfg.get('ssl', True),
        'imap_user': imap_cfg.get('user', ''),
        'config_present': True
    })


@app.route('/api/emails')
def api_emails():
    limit = request.args.get('limit', 50, type=int)
    try:
        emails = imap_reader.list_emails(limit=limit)
        enriched = []
        for e in emails:
            quick = analyzer.quick_score_from_headers(e)
            e['score'] = quick['score']
            e['score_label'] = quick['score_label']
            enriched.append(e)
        return jsonify({'emails': enriched, 'total': len(enriched)})
    except FileNotFoundError as ex:
        return jsonify({'error': str(ex)}), 503
    except Exception as ex:
        return jsonify({'error': f'Erreur IMAP: {str(ex)}'}), 500


@app.route('/api/email/<uid>')
def api_email_detail(uid):
    try:
        result = analyzer.analyze_email(uid)
        if 'error' in result:
            return jsonify(result), 404
        return jsonify(result)
    except FileNotFoundError as ex:
        return jsonify({'error': str(ex)}), 503
    except Exception as ex:
        return jsonify({'error': f'Erreur analyse: {str(ex)}'}), 500


@app.route('/api/rapport/<uid>', methods=['POST'])
def api_generate_rapport(uid):
    body = request.get_json(silent=True) or {}
    validated = body.get('validated', False)

    if not validated:
        return jsonify({'error': 'Validation humaine requise (validated: true)'}), 400

    try:
        analysis = analyzer.analyze_email(uid)
        if 'error' in analysis:
            return jsonify(analysis), 404

        result = plaidoyer.generate(analysis, validated=True)
        return jsonify(result)
    except FileNotFoundError as ex:
        return jsonify({'error': str(ex)}), 503
    except Exception as ex:
        return jsonify({'error': f'Erreur génération: {str(ex)}'}), 500


@app.route('/api/anonymize/<uid>')
def api_anonymize(uid):
    try:
        analysis = analyzer.analyze_email(uid)
        if 'error' in analysis:
            return jsonify(analysis), 404
        anon = anonymizer.anonymize_analysis(analysis)
        return jsonify(anon)
    except FileNotFoundError as ex:
        return jsonify({'error': str(ex)}), 503
    except Exception as ex:
        return jsonify({'error': f'Erreur anonymisation: {str(ex)}'}), 500


@app.route('/api/rapports')
def api_list_rapports():
    rapports = plaidoyer.list_rapports()
    return jsonify({'rapports': rapports, 'total': len(rapports)})


@app.route('/api/rapports/<filename>')
def api_get_rapport(filename):
    if '..' in filename or '/' in filename or '\\' in filename:
        abort(400)
    data = plaidoyer.get_rapport(filename)
    if data is None:
        return jsonify({'error': 'Rapport introuvable'}), 404
    return jsonify(data)


@app.route('/api/rapports/<filename>/md')
def api_get_rapport_md(filename):
    if '..' in filename or '/' in filename or '\\' in filename:
        abort(400)
    md_name = filename.replace('.json', '.md')
    md_path = os.path.join(RAPPORTS_DIR, md_name)
    if not os.path.exists(md_path):
        return jsonify({'error': 'Rapport Markdown introuvable'}), 404
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()
    return app.response_class(content, mimetype='text/plain; charset=utf-8')


if __name__ == '__main__':
    cfg = _load_config()
    port = 8020
    if cfg:
        port = cfg.get('server', {}).get('port', 8020)
    print(f"AntiSpams démarré sur http://localhost:{port}")
    print(f"Config: {'OK' if cfg else 'MANQUANTE — copier config.example.json vers config.json'}")
    app.run(host='0.0.0.0', port=port, debug=False)
