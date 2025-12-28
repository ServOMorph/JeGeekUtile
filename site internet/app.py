from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date
from functools import wraps
import os
import uuid
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///jegeekutile.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Veuillez vous connecter pour acceder a cette page.'

user_appetences = db.Table('user_appetences',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('appetence_id', db.Integer, db.ForeignKey('appetence.id'), primary_key=True)
)

class Appetence(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), unique=True, nullable=False)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    nom = db.Column(db.String(100), nullable=False)
    prenom = db.Column(db.String(100), nullable=False)
    date_inscription = db.Column(db.DateTime, default=datetime.utcnow)
    is_admin = db.Column(db.Boolean, default=False)
    is_benevole = db.Column(db.Boolean, default=False)
    date_naissance = db.Column(db.Date, nullable=True)
    adresse = db.Column(db.String(300), nullable=True)
    motivation = db.Column(db.Text, nullable=True)
    temps_disponible = db.Column(db.String(100), nullable=True)
    missions_realisees = db.Column(db.Text, nullable=True)
    missions_en_cours = db.Column(db.Text, nullable=True)
    monnaie = db.Column(db.Integer, default=0)
    appetences = db.relationship('Appetence', secondary=user_appetences, lazy='subquery',
        backref=db.backref('users', lazy=True))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_age(self):
        if self.date_naissance:
            today = date.today()
            return today.year - self.date_naissance.year - ((today.month, today.day) < (self.date_naissance.month, self.date_naissance.day))
        return None

class ActivityLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    session_id = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    page = db.Column(db.String(200))
    event_type = db.Column(db.String(50))
    element = db.Column(db.String(200))
    details = db.Column(db.Text)

    user = db.relationship('User', backref=db.backref('activity_logs', lazy=True))

class Evenement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    date_evenement = db.Column(db.Date, nullable=False)
    heure_debut = db.Column(db.String(10))
    heure_fin = db.Column(db.String(10))
    lieu = db.Column(db.String(200))
    statut = db.Column(db.String(20), default='ouvert')
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('Acces reserve aux administrateurs.', 'error')
            return redirect(url_for('accueil'))
        return f(*args, **kwargs)
    return decorated_function

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.context_processor
def inject_now():
    return {'now': datetime.now}

@app.route('/')
def accueil():
    return render_template('accueil.html')

@app.route('/a-propos')
def a_propos():
    return render_template('a_propos.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/mentions-legales')
def mentions_legales():
    return render_template('mentions_legales.html')

@app.route('/politique-confidentialite')
def politique_confidentialite():
    return render_template('politique_confidentialite.html')

@app.route('/politique-cookies')
def politique_cookies():
    return render_template('politique_cookies.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        nom = request.form.get('nom')
        email = request.form.get('email')
        message = request.form.get('message')
        rgpd_consent = request.form.get('rgpd_consent')
        if not rgpd_consent:
            flash('Vous devez accepter la politique de confidentialite.', 'error')
            return redirect(url_for('contact'))
        flash('Votre message a ete envoye avec succes.', 'success')
        return redirect(url_for('contact'))
    return render_template('contact.html')

@app.route('/inscription', methods=['GET', 'POST'])
def inscription():
    if current_user.is_authenticated:
        return redirect(url_for('espace_membre'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        nom = request.form.get('nom')
        prenom = request.form.get('prenom')
        type_compte = request.form.get('type_compte')
        rgpd_consent = request.form.get('rgpd_consent')

        if not rgpd_consent:
            flash('Vous devez accepter la politique de confidentialite.', 'error')
            return redirect(url_for('inscription'))

        if User.query.filter_by(email=email).first():
            flash('Cet email est deja utilise.', 'error')
            return redirect(url_for('inscription'))

        user = User(email=email, nom=nom, prenom=prenom)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        if type_compte == 'benevole':
            session['nouveau_benevole_id'] = user.id
            flash('Compte cree. Completez votre profil benevole.', 'success')
            return redirect(url_for('formulaire_benevole'))

        flash('Inscription reussie. Vous pouvez maintenant vous connecter.', 'success')
        return redirect(url_for('login'))

    return render_template('inscription.html')

@app.route('/connexion', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('espace_membre'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('espace_membre'))

        flash('Email ou mot de passe incorrect.', 'error')

    return render_template('login.html')

@app.route('/deconnexion')
@login_required
def logout():
    logout_user()
    flash('Vous avez ete deconnecte.', 'success')
    return redirect(url_for('accueil'))

@app.route('/espace-membre')
@login_required
def espace_membre():
    dashboard_data = {}

    if current_user.is_admin:
        total_benevoles = User.query.filter_by(is_benevole=True).count()
        total_users = User.query.count()
        recent_users = User.query.order_by(User.date_inscription.desc()).limit(5).all()
        total_geekos = db.session.query(db.func.sum(User.monnaie)).filter(User.is_benevole==True).scalar() or 0
        recent_logs = ActivityLog.query.order_by(ActivityLog.timestamp.desc()).limit(10).all()

        dashboard_data = {
            'total_benevoles': total_benevoles,
            'total_users': total_users,
            'recent_users': recent_users,
            'total_geekos': total_geekos,
            'recent_logs': recent_logs
        }

    if current_user.is_benevole:
        appetences = current_user.appetences
        dashboard_data['appetences'] = appetences
        evenements = Evenement.query.filter(Evenement.date_evenement >= date.today()).order_by(Evenement.date_evenement.asc()).limit(5).all()
        dashboard_data['evenements'] = evenements

    return render_template('espace_membre.html', dashboard_data=dashboard_data)

@app.route('/profil', methods=['GET', 'POST'])
@login_required
def profil():
    appetences = Appetence.query.all()
    if request.method == 'POST':
        current_user.nom = request.form.get('nom')
        current_user.prenom = request.form.get('prenom')
        date_naissance_str = request.form.get('date_naissance')
        if date_naissance_str:
            current_user.date_naissance = datetime.strptime(date_naissance_str, '%Y-%m-%d').date()
        current_user.adresse = request.form.get('adresse')
        if current_user.is_benevole:
            current_user.motivation = request.form.get('motivation')
            current_user.temps_disponible = request.form.get('temps_disponible')
            appetences_selectionnees = request.form.getlist('appetences')
            current_user.appetences = Appetence.query.filter(Appetence.id.in_(appetences_selectionnees)).all()
        db.session.commit()
        flash('Profil mis a jour.', 'success')
    return render_template('profil.html', appetences=appetences)

@app.route('/mes-donnees')
@login_required
def export_donnees():
    user = current_user
    data = {
        'informations_personnelles': {
            'id': user.id,
            'email': user.email,
            'nom': user.nom,
            'prenom': user.prenom,
            'date_inscription': user.date_inscription.isoformat() if user.date_inscription else None,
            'date_naissance': user.date_naissance.isoformat() if user.date_naissance else None,
            'adresse': user.adresse,
            'is_benevole': user.is_benevole,
            'is_admin': user.is_admin
        },
        'donnees_benevole': {
            'motivation': user.motivation,
            'temps_disponible': user.temps_disponible,
            'missions_realisees': user.missions_realisees,
            'missions_en_cours': user.missions_en_cours,
            'monnaie_geekos': user.monnaie,
            'appetences': [a.nom for a in user.appetences]
        } if user.is_benevole else None,
        'activite': [
            {
                'timestamp': log.timestamp.isoformat(),
                'page': log.page,
                'event_type': log.event_type
            } for log in user.activity_logs
        ],
        'export_date': datetime.utcnow().isoformat(),
        'rgpd_info': 'Export conforme RGPD - Article 20 Droit a la portabilite'
    }
    response = jsonify(data)
    response.headers['Content-Disposition'] = f'attachment; filename=mes_donnees_jegeekutile_{user.id}.json'
    return response

@app.route('/supprimer-compte', methods=['GET', 'POST'])
@login_required
def supprimer_compte():
    if request.method == 'POST':
        confirmation = request.form.get('confirmation')
        if confirmation != current_user.email:
            flash('Email de confirmation incorrect.', 'error')
            return redirect(url_for('supprimer_compte'))

        user_id = current_user.id
        ActivityLog.query.filter_by(user_id=user_id).delete()
        user = User.query.get(user_id)
        user.appetences = []
        db.session.delete(user)
        db.session.commit()
        logout_user()
        flash('Votre compte a ete supprime definitivement.', 'success')
        return redirect(url_for('accueil'))

    return render_template('supprimer_compte.html')

@app.route('/formulaire-benevole', methods=['GET', 'POST'])
def formulaire_benevole():
    user_id = session.get('nouveau_benevole_id')
    if not user_id:
        flash('Acces non autorise.', 'error')
        return redirect(url_for('inscription'))

    user = User.query.get(user_id)
    if not user:
        flash('Utilisateur introuvable.', 'error')
        return redirect(url_for('inscription'))

    appetences = Appetence.query.all()

    if request.method == 'POST':
        rgpd_consent = request.form.get('rgpd_consent')
        if not rgpd_consent:
            flash('Vous devez accepter la politique de confidentialite.', 'error')
            return redirect(url_for('formulaire_benevole'))

        date_naissance_str = request.form.get('date_naissance')
        if date_naissance_str:
            user.date_naissance = datetime.strptime(date_naissance_str, '%Y-%m-%d').date()
        user.adresse = request.form.get('adresse')
        user.motivation = request.form.get('motivation')
        user.temps_disponible = request.form.get('temps_disponible')
        user.is_benevole = True

        appetences_selectionnees = request.form.getlist('appetences')
        user.appetences = Appetence.query.filter(Appetence.id.in_(appetences_selectionnees)).all()

        db.session.commit()
        session.pop('nouveau_benevole_id', None)
        flash('Profil benevole complete. Vous pouvez vous connecter.', 'success')
        return redirect(url_for('login'))

    return render_template('formulaire_benevole.html', appetences=appetences)

@app.route('/admin')
@login_required
@admin_required
def admin():
    benevoles = User.query.filter_by(is_benevole=True).all()
    appetences = Appetence.query.all()
    return render_template('admin.html', benevoles=benevoles, appetences=appetences)

@app.route('/admin/stats')
@login_required
@admin_required
def admin_stats():
    benevoles = User.query.filter_by(is_benevole=True).all()
    appetences = Appetence.query.all()

    total_benevoles = len(benevoles)
    total_geekos = sum(b.monnaie for b in benevoles)
    moyenne_geekos = total_geekos / total_benevoles if total_benevoles > 0 else 0

    temps_stats = {}
    for b in benevoles:
        t = b.temps_disponible or 'non_renseigne'
        temps_stats[t] = temps_stats.get(t, 0) + 1

    appetences_stats = {}
    for app in appetences:
        appetences_stats[app.nom] = len(app.users)

    ages = [b.get_age() for b in benevoles if b.get_age()]
    age_stats = {
        'moins_18': len([a for a in ages if a < 18]),
        '18_25': len([a for a in ages if 18 <= a < 25]),
        '25_35': len([a for a in ages if 25 <= a < 35]),
        '35_50': len([a for a in ages if 35 <= a < 50]),
        'plus_50': len([a for a in ages if a >= 50]),
        'non_renseigne': total_benevoles - len(ages)
    }
    moyenne_age = sum(ages) / len(ages) if ages else 0

    inscriptions_par_mois = {}
    for b in benevoles:
        mois = b.date_inscription.strftime('%Y-%m')
        inscriptions_par_mois[mois] = inscriptions_par_mois.get(mois, 0) + 1
    inscriptions_par_mois = dict(sorted(inscriptions_par_mois.items()))

    top_geekos = sorted(benevoles, key=lambda x: x.monnaie, reverse=True)[:5]

    return render_template('admin_stats.html',
        total_benevoles=total_benevoles,
        total_geekos=total_geekos,
        moyenne_geekos=round(moyenne_geekos, 1),
        temps_stats=temps_stats,
        appetences_stats=appetences_stats,
        age_stats=age_stats,
        moyenne_age=round(moyenne_age, 1),
        inscriptions_par_mois=inscriptions_par_mois,
        top_geekos=top_geekos
    )

@app.route('/admin/benevole/<int:user_id>')
@login_required
@admin_required
def admin_benevole_detail(user_id):
    benevole = User.query.get_or_404(user_id)
    if not benevole.is_benevole:
        flash('Cet utilisateur n\'est pas benevole.', 'error')
        return redirect(url_for('admin'))
    return render_template('admin_benevole_detail.html', benevole=benevole)

@app.route('/admin/benevole/<int:user_id>/modifier', methods=['POST'])
@login_required
@admin_required
def admin_modifier_benevole(user_id):
    benevole = User.query.get_or_404(user_id)
    if not benevole.is_benevole:
        flash('Cet utilisateur n\'est pas benevole.', 'error')
        return redirect(url_for('admin'))

    benevole.missions_realisees = request.form.get('missions_realisees')
    benevole.missions_en_cours = request.form.get('missions_en_cours')
    benevole.monnaie = int(request.form.get('monnaie', 0))
    db.session.commit()
    flash('Informations du benevole mises a jour.', 'success')
    return redirect(url_for('admin_benevole_detail', user_id=user_id))

@app.route('/admin/preview-benevole')
@login_required
@admin_required
def admin_preview_benevole():
    evenements = Evenement.query.filter(Evenement.date_evenement >= date.today()).order_by(Evenement.date_evenement.asc()).limit(5).all()
    appetences = Appetence.query.all()
    preview_data = {
        'evenements': evenements,
        'appetences': appetences
    }
    return render_template('admin_preview_benevole.html', preview_data=preview_data)

@app.route('/api/log', methods=['POST'])
def api_log():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Donnees manquantes'}), 400

    if 'tracking_session' not in session:
        session['tracking_session'] = str(uuid.uuid4())

    log = ActivityLog(
        session_id=session['tracking_session'],
        user_id=current_user.id if current_user.is_authenticated else None,
        page=data.get('page'),
        event_type=data.get('type'),
        element=data.get('element'),
        details=json.dumps(data.get('details', {}))
    )
    db.session.add(log)
    db.session.commit()
    return jsonify({'status': 'ok'})

@app.route('/admin/logs')
@login_required
@admin_required
def admin_logs():
    page = request.args.get('page', 1, type=int)
    logs = ActivityLog.query.order_by(ActivityLog.timestamp.desc()).paginate(page=page, per_page=50)
    return render_template('admin_logs.html', logs=logs)

@app.route('/admin/logs/export')
@login_required
@admin_required
def admin_logs_export():
    logs = ActivityLog.query.order_by(ActivityLog.timestamp.desc()).all()
    data = []
    for log in logs:
        data.append({
            'timestamp': log.timestamp.isoformat(),
            'session_id': log.session_id,
            'user_id': log.user_id,
            'user_email': log.user.email if log.user else None,
            'page': log.page,
            'event_type': log.event_type,
            'element': log.element,
            'details': json.loads(log.details) if log.details else {}
        })
    return jsonify(data)

@app.route('/admin/evenements')
@login_required
@admin_required
def admin_evenements():
    evenements = Evenement.query.order_by(Evenement.date_evenement.desc()).all()
    return render_template('admin_evenements.html', evenements=evenements)

@app.route('/admin/evenements/ajouter', methods=['POST'])
@login_required
@admin_required
def admin_ajouter_evenement():
    titre = request.form.get('titre')
    description = request.form.get('description')
    date_str = request.form.get('date_evenement')
    heure_debut = request.form.get('heure_debut')
    heure_fin = request.form.get('heure_fin')
    lieu = request.form.get('lieu')
    statut = request.form.get('statut', 'ouvert')

    if not titre or not date_str:
        flash('Titre et date sont obligatoires.', 'error')
        return redirect(url_for('admin_evenements'))

    date_evenement = datetime.strptime(date_str, '%Y-%m-%d').date()
    evenement = Evenement(
        titre=titre,
        description=description,
        date_evenement=date_evenement,
        heure_debut=heure_debut,
        heure_fin=heure_fin,
        lieu=lieu,
        statut=statut
    )
    db.session.add(evenement)
    db.session.commit()
    flash('Evenement ajoute avec succes.', 'success')
    return redirect(url_for('admin_evenements'))

@app.route('/admin/evenements/<int:event_id>/modifier', methods=['POST'])
@login_required
@admin_required
def admin_modifier_evenement(event_id):
    evenement = Evenement.query.get_or_404(event_id)
    evenement.titre = request.form.get('titre')
    evenement.description = request.form.get('description')
    date_str = request.form.get('date_evenement')
    if date_str:
        evenement.date_evenement = datetime.strptime(date_str, '%Y-%m-%d').date()
    evenement.heure_debut = request.form.get('heure_debut')
    evenement.heure_fin = request.form.get('heure_fin')
    evenement.lieu = request.form.get('lieu')
    evenement.statut = request.form.get('statut')
    db.session.commit()
    flash('Evenement modifie avec succes.', 'success')
    return redirect(url_for('admin_evenements'))

@app.route('/admin/evenements/<int:event_id>/supprimer', methods=['POST'])
@login_required
@admin_required
def admin_supprimer_evenement(event_id):
    evenement = Evenement.query.get_or_404(event_id)
    db.session.delete(evenement)
    db.session.commit()
    flash('Evenement supprime.', 'success')
    return redirect(url_for('admin_evenements'))

def init_db():
    db.create_all()

    admin_email = os.environ.get('ADMIN_EMAIL')
    admin_password = os.environ.get('ADMIN_PASSWORD')
    if admin_email and admin_password:
        if not User.query.filter_by(email=admin_email).first():
            admin = User(
                email=admin_email,
                nom='Admin',
                prenom='Admin',
                is_admin=True
            )
            admin.set_password(admin_password)
            db.session.add(admin)

    appetences_defaut = [
        'Informatique',
        'Communication',
        'Evenementiel',
        'Formation',
        'Redaction',
        'Design graphique',
        'Comptabilite',
        'Logistique',
        'Accueil',
        'Animation'
    ]
    for nom in appetences_defaut:
        if not Appetence.query.filter_by(nom=nom).first():
            db.session.add(Appetence(nom=nom))

    db.session.commit()

with app.app_context():
    init_db()

if __name__ == '__main__':
    app.run(debug=True, port=5000)
