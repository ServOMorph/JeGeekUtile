from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from auto_ia.core.actions import execute_action, action_queue, action_worker
from auto_ia.core.zones import zone_manager
from auto_ia.core.tutorial import tutorial_manager
from auto_ia.core.init_tutorial import load_default_tutorial

app = Flask(__name__)
CORS(app)

SAFE_MODE = os.getenv('AUTO_IA_SAFE_MODE', 'true').lower() == 'true'

@app.route('/action', methods=['POST'])
def handle_action():
    action = request.json
    result = execute_action(action)
    return jsonify(result)

@app.route('/status', methods=['GET'])
def get_status():
    return jsonify({"status": "idle", "message": "Serveur actif"})

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "ok", "service": "auto_ia"})

@app.route('/queue/actions', methods=['POST'])
def add_to_queue():
    data = request.json
    action_type = data.get('type')
    params = data.get('params', {})
    source = data.get('source', 'unknown')
    priority = data.get('priority', 0)
    label = data.get('label')

    if not action_type:
        return jsonify({"status": "error", "message": "Type manquant"}), 400

    action_id = action_queue.add_action(action_type, params, source, priority, label)
    return jsonify({"status": "ok", "action_id": action_id})

@app.route('/queue/actions', methods=['GET'])
def list_queue():
    status_filter = request.args.get('status')
    actions = action_queue.list_actions(status_filter)
    return jsonify({"status": "ok", "items": actions})

@app.route('/queue/control', methods=['POST'])
def control_worker():
    data = request.json
    command = data.get('command')

    if command == 'start':
        action_worker.start()
    elif command == 'stop':
        action_worker.stop()
    elif command == 'pause':
        action_worker.pause()
    elif command == 'resume':
        action_worker.resume()
    else:
        return jsonify({"status": "error", "message": "Commande inconnue"}), 400

    return jsonify({"status": "ok", "worker_status": action_worker.get_status()})

@app.route('/queue/status', methods=['GET'])
def get_worker_status():
    return jsonify({
        "status": "ok",
        "worker_status": action_worker.get_status(),
        "queue_count": len(action_queue.list_actions())
    })

@app.route('/config/status', methods=['GET'])
def get_config_status():
    return jsonify({
        "status": "ok",
        "safe_mode": SAFE_MODE,
        "min_delay_seconds": action_worker.min_delay_seconds,
        "max_actions_per_minute": action_worker.max_actions_per_minute
    })

@app.route('/zones', methods=['POST'])
def create_or_update_zone():
    data = request.json
    name = data.get('name')
    x = data.get('x')
    y = data.get('y')
    width = data.get('width')
    height = data.get('height')

    if not name or x is None or y is None:
        return jsonify({"status": "error", "message": "name, x, y requis"}), 400

    zone = zone_manager.set_zone(name, x, y, width, height)
    return jsonify({"status": "ok", "zone": zone.to_dict()})

@app.route('/zones', methods=['GET'])
def list_zones():
    zones = zone_manager.list_zones()
    return jsonify({"status": "ok", "zones": zones})

@app.route('/zones/<name>', methods=['DELETE'])
def delete_zone(name):
    deleted = zone_manager.delete_zone(name)
    if deleted:
        return jsonify({"status": "ok", "message": f"Zone {name} supprimée"})
    return jsonify({"status": "error", "message": "Zone non trouvée"}), 404

@app.route('/tutorial/start', methods=['POST'])
def start_tutorial():
    success = tutorial_manager.start_tutorial()
    if success:
        return jsonify({"status": "ok", "message": "Tutoriel démarré"})
    return jsonify({"status": "error", "message": "Aucun tutoriel chargé"}), 404

@app.route('/tutorial/stop', methods=['POST'])
def stop_tutorial():
    success = tutorial_manager.stop_tutorial()
    if success:
        return jsonify({"status": "ok", "message": "Tutoriel arrêté"})
    return jsonify({"status": "error", "message": "Aucun tutoriel actif"}), 404

@app.route('/tutorial/status', methods=['GET'])
def get_tutorial_status():
    return jsonify(tutorial_manager.get_status())

def run_server(host='127.0.0.1', port=8000):
    load_default_tutorial()
    app.run(host=host, port=port, debug=True, use_reloader=True)
