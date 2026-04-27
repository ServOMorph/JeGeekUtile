import subprocess
import sys
import os
import threading
import webbrowser
import time

base_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, base_dir)

from config import PORT

v3_dir = os.path.join(base_dir, "v3")
sys.path.insert(0, v3_dir)

def ouvrir_navigateur():
    time.sleep(2)
    webbrowser.open(f"http://localhost:{PORT}")

print(f"🚀 Lancement JeGeekUtile V3 sur http://localhost:{PORT}")
print(f"📂 Répertoire : {v3_dir}")
print(f"💾 Base de données : {os.path.join(v3_dir, 'instance', 'jegeekutile.db')}")
print(f"⏹️  Arrêter : CTRL+C\n")

threading.Thread(target=ouvrir_navigateur, daemon=True).start()

env = os.environ.copy()
env['PORT'] = str(PORT)
subprocess.run([sys.executable, "app.py"], cwd=v3_dir, env=env)
