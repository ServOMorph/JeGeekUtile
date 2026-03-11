import subprocess
import sys
import os
import threading
import webbrowser
import time
sys.path.insert(0, os.path.dirname(__file__))
from config import PORT_SITE

site_dir = os.path.join(os.path.dirname(__file__), "site internet")

def ouvrir_navigateur():
    time.sleep(1.5)
    webbrowser.open(f"http://localhost:{PORT_SITE}")

threading.Thread(target=ouvrir_navigateur, daemon=True).start()
subprocess.run([sys.executable, "app.py"], cwd=site_dir)
