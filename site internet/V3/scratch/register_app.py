import sys
import os

base_dir = os.getcwd()
v3_dir = os.path.join(base_dir, 'v3')
sys.path.insert(0, v3_dir)

from app import create_app
from backend.models import db, App

app = create_app()
with app.app_context():
    apps = [a.name for a in App.query.all()]
    print(f"Current apps: {apps}")
    
    app_name = "Présentation"
    if app_name not in apps:
        new_app = App(name=app_name, html_path="presentation/index.html")
        db.session.add(new_app)
        db.session.commit()
        print(f"Registered {app_name}")
    else:
        print(f"{app_name} already registered")
