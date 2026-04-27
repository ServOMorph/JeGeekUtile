import sys
import os

base_dir = os.getcwd()
v3_dir = os.path.join(base_dir, 'v3')
sys.path.insert(0, v3_dir)

from app import create_app
from backend.models import db, App

app = create_app()
with app.app_context():
    app_name = "Présentation"
    p = App.query.filter_by(name=app_name).first()
    if p:
        db.session.delete(p)
        db.session.commit()
        print(f"Removed {app_name} from DB")
    else:
        # Try without accent just in case
        p = App.query.filter_by(name="Presentation").first()
        if p:
            db.session.delete(p)
            db.session.commit()
            print("Removed Presentation from DB")
        else:
            print("App not found in DB")
