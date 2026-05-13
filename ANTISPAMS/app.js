const App = {
  data: {
    currentView: 'liste',
    emails: [],
    selectedEmail: null,
    selectedAnalysis: null,
    rapports: [],
    stats: { total: 0, avg: 0, hautRisque: 0, rapports: 0 },
    configStatus: null,
    loading: false,
    validationChecked: false,
  },

  async init() {
    this.setFooterDate();
    this.setupNavigation();
    await this.checkHealth();
    await this.render('liste');
  },

  setFooterDate() {
    const el = document.getElementById('footer-date');
    if (el) el.textContent = new Date().toLocaleDateString('fr-FR');
  },

  setupNavigation() {
    document.querySelectorAll('nav button').forEach(btn => {
      btn.addEventListener('click', () => {
        document.querySelectorAll('nav button').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        this.render(btn.dataset.view);
      });
    });
  },

  async checkHealth() {
    try {
      const res = await fetch('/api/health');
      this.data.configStatus = await res.json();
    } catch {
      this.data.configStatus = { status: 'error', message: 'Serveur injoignable' };
    }
  },

  async render(view) {
    this.data.currentView = view;
    const main = document.getElementById('view');
    main.innerHTML = '<div class="loading">Chargement...</div>';

    if (view === 'liste') await this.renderListe(main);
    else if (view === 'detail') this.renderDetail(main);
    else if (view === 'rapports') await this.renderRapports(main);
    else if (view === 'config') this.renderConfig(main);
  },

  async renderListe(main) {
    if (this.data.configStatus?.status !== 'ok') {
      main.innerHTML = this.renderConfigWarning();
      return;
    }

    try {
      const res = await fetch('/api/emails?limit=100');
      const data = await res.json();
      if (data.error) throw new Error(data.error);

      this.data.emails = data.emails || [];
      this.updateStats();
      main.innerHTML = this.buildListeHTML();
      this.attachListeEvents();
    } catch (err) {
      main.innerHTML = `<div class="empty-state">Erreur chargement emails : ${err.message}</div>`;
    }
  },

  buildListeHTML() {
    if (this.data.emails.length === 0) {
      return '<div class="empty-state">Aucun email récupéré. Vérifiez la configuration IMAP.</div>';
    }

    const rows = this.data.emails.map(e => {
      const badge = this.scoreBadge(e.score, e.score_label);
      const from = this.escapeHtml(e.from || '');
      const subject = this.escapeHtml(e.subject || '(sans objet)');
      const date = this.formatDate(e.date);
      return `<tr data-uid="${e.uid}" class="email-row">
        <td>${date}</td>
        <td>${from}</td>
        <td>${subject}</td>
        <td>${badge}</td>
        <td>
          <button class="btn btn-primary btn-analyze" data-uid="${e.uid}">Analyser</button>
        </td>
      </tr>`;
    }).join('');

    return `<table>
      <thead>
        <tr>
          <th>Date</th>
          <th>Expéditeur</th>
          <th>Sujet</th>
          <th>Score</th>
          <th>Action</th>
        </tr>
      </thead>
      <tbody>${rows}</tbody>
    </table>`;
  },

  attachListeEvents() {
    document.querySelectorAll('.btn-analyze').forEach(btn => {
      btn.addEventListener('click', async (e) => {
        e.stopPropagation();
        const uid = btn.dataset.uid;
        await this.loadAndShowAnalysis(uid);
      });
    });
  },

  async loadAndShowAnalysis(uid) {
    const navBtn = document.querySelector('nav button[data-view="detail"]');
    document.querySelectorAll('nav button').forEach(b => b.classList.remove('active'));
    if (navBtn) navBtn.classList.add('active');

    const main = document.getElementById('view');
    main.innerHTML = '<div class="loading">Analyse en cours...</div>';

    try {
      const res = await fetch(`/api/email/${uid}`);
      const data = await res.json();
      if (data.error) throw new Error(data.error);
      this.data.selectedEmail = this.data.emails.find(e => e.uid === uid) || {};
      this.data.selectedAnalysis = data;
      this.data.validationChecked = false;
      this.renderDetail(main);
    } catch (err) {
      main.innerHTML = `<div class="empty-state">Erreur analyse : ${err.message}</div>`;
    }
  },

  renderDetail(main) {
    if (!this.data.selectedAnalysis) {
      main.innerHTML = `<div class="empty-state">
        Sélectionnez un email depuis la vue <strong>Liste</strong> et cliquez sur [Analyser].
      </div>`;
      return;
    }

    const a = this.data.selectedAnalysis;
    const h = a.headers || {};
    const scoreColor = a.score_label === 'danger' ? 'var(--danger-text)' : a.score_label === 'warning' ? 'var(--warning-text)' : 'var(--success-text)';

    const criteriaHTML = (a.criteria || []).map(c => {
      const cls = c.triggered ? 'criteria-triggered' : 'criteria-ok';
      const icon = c.triggered ? '⚠' : '✓';
      const pts = c.triggered ? `+${c.points}` : '0';
      return `<li>
        <span class="${cls}">${icon} ${this.escapeHtml(c.label)}</span>
        <span class="criteria-points">${pts} pts</span>
      </li>`;
    }).join('');

    main.innerHTML = `
      <div class="detail-grid">
        <div>
          <div class="card">
            <h3>Métadonnées</h3>
            <div class="email-meta">De : <span>${this.escapeHtml(h.from || '')}</span></div>
            <div class="email-meta">Sujet : <span>${this.escapeHtml(h.subject || '')}</span></div>
            <div class="email-meta">Date : <span>${this.escapeHtml(h.date || '')}</span></div>
            <div class="email-meta">Reply-To : <span>${this.escapeHtml(h.reply_to || '(absent)')}</span></div>
            <div class="email-meta">List-Unsubscribe : <span>${this.escapeHtml(h.list_unsubscribe || '(absent)')}</span></div>
          </div>

          <div class="card">
            <h3>Critères RGPD</h3>
            <ul class="criteria-list">${criteriaHTML}</ul>
          </div>

          ${a.body_preview ? `<div class="card">
            <h3>Aperçu contenu</h3>
            <pre style="font-size:11px;white-space:pre-wrap;color:var(--text-secondary);max-height:150px;overflow-y:auto;">${this.escapeHtml(a.body_preview)}</pre>
          </div>` : ''}
        </div>

        <div>
          <div class="card" style="text-align:center;padding:24px 16px;">
            <div class="score-label">Score de risque</div>
            <div class="score-big" style="color:${scoreColor};margin:12px 0;">${a.score}</div>
            <div class="score-label">/100</div>
            <div style="margin-top:8px;">${this.scoreBadge(a.score, a.score_label)}</div>
          </div>

          <div class="card">
            <h3>Actions</h3>
            <label class="checkbox-validation">
              <input type="checkbox" id="validation-check" ${this.data.validationChecked ? 'checked' : ''}>
              J'ai vérifié manuellement le contenu et j'autorise l'export
            </label>
            <div class="action-bar" style="flex-direction:column;gap:8px;">
              <button class="btn btn-primary" id="btn-rapport" style="width:100%;">Générer Rapport</button>
              <button class="btn btn-secondary" id="btn-anonymize" style="width:100%;">Anonymiser</button>
              <button class="btn btn-secondary" id="btn-retour" style="width:100%;">← Retour Liste</button>
            </div>
          </div>
        </div>
      </div>`;

    document.getElementById('validation-check').addEventListener('change', (e) => {
      this.data.validationChecked = e.target.checked;
    });

    document.getElementById('btn-rapport').addEventListener('click', () => this.generateRapport(a.uid));
    document.getElementById('btn-anonymize').addEventListener('click', () => this.anonymizeEmail(a.uid));
    document.getElementById('btn-retour').addEventListener('click', () => {
      document.querySelectorAll('nav button').forEach(b => b.classList.remove('active'));
      document.querySelector('nav button[data-view="liste"]').classList.add('active');
      this.render('liste');
    });
  },

  async generateRapport(uid) {
    if (!this.data.validationChecked) {
      this.showNotification('Cochez la case de validation humaine avant de générer le rapport', 'error');
      return;
    }
    try {
      const res = await fetch(`/api/rapport/${uid}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ validated: true })
      });
      const data = await res.json();
      if (data.error) throw new Error(data.error);
      this.showNotification(`Rapport généré : ${data.filename} (score: ${data.score}/100)`, 'success');
    } catch (err) {
      this.showNotification(`Erreur génération : ${err.message}`, 'error');
    }
  },

  async anonymizeEmail(uid) {
    try {
      const res = await fetch(`/api/anonymize/${uid}`);
      const data = await res.json();
      if (data.error) throw new Error(data.error);
      this.data.selectedAnalysis = data;
      this.renderDetail(document.getElementById('view'));
      this.showNotification('Email anonymisé (données personnelles masquées)', 'success');
    } catch (err) {
      this.showNotification(`Erreur anonymisation : ${err.message}`, 'error');
    }
  },

  async renderRapports(main) {
    try {
      const res = await fetch('/api/rapports');
      const data = await res.json();
      this.data.rapports = data.rapports || [];
      this.updateStatsRapports();

      if (this.data.rapports.length === 0) {
        main.innerHTML = '<div class="empty-state">Aucun rapport généré. Analysez des emails et générez des rapports depuis la vue Analyse.</div>';
        return;
      }

      const rows = this.data.rapports.map(r => {
        const riskLabel = r.risk_level === 'high' ? '🔴 Haut' : r.risk_level === 'medium' ? '🟡 Moyen' : '🟢 OK';
        return `<div class="rapport-item">
          <div>
            <div style="font-size:12px;color:var(--text-primary);">${this.escapeHtml(r.subject || '(sans objet)')}</div>
            <div style="font-size:11px;color:var(--text-secondary);">${this.escapeHtml(r.from || '')} — ${this.formatDateISO(r.generated_at)}</div>
          </div>
          <div style="display:flex;align-items:center;gap:12px;">
            ${this.scoreBadge(r.score, r.risk_level === 'high' ? 'danger' : r.risk_level === 'medium' ? 'warning' : 'ok')}
            <button class="btn btn-secondary" data-file="${r.filename}" style="font-size:11px;">Voir JSON</button>
            <button class="btn btn-secondary btn-dl-md" data-file="${r.filename}" style="font-size:11px;">Voir MD</button>
          </div>
        </div>`;
      }).join('');

      main.innerHTML = `<div class="card"><h3>${this.data.rapports.length} rapport(s) archivé(s)</h3></div>${rows}`;

      main.querySelectorAll('.btn-secondary:not(.btn-dl-md)').forEach(btn => {
        btn.addEventListener('click', async () => {
          const file = btn.dataset.file;
          try {
            const res = await fetch(`/api/rapports/${file}`);
            const data = await res.json();
            alert(JSON.stringify(data, null, 2));
          } catch (err) {
            this.showNotification(`Erreur lecture rapport : ${err.message}`, 'error');
          }
        });
      });

      main.querySelectorAll('.btn-dl-md').forEach(btn => {
        btn.addEventListener('click', async () => {
          const file = btn.dataset.file;
          try {
            const res = await fetch(`/api/rapports/${file}/md`);
            const text = await res.text();
            const blob = new Blob([text], { type: 'text/markdown' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = file.replace('.json', '.md');
            a.click();
            URL.revokeObjectURL(url);
          } catch (err) {
            this.showNotification(`Erreur téléchargement MD : ${err.message}`, 'error');
          }
        });
      });
    } catch (err) {
      main.innerHTML = `<div class="empty-state">Erreur chargement rapports : ${err.message}</div>`;
    }
  },

  renderConfig(main) {
    const cfg = this.data.configStatus || {};
    const statusHTML = cfg.status === 'ok'
      ? `<div class="status-ok">✓ Connexion IMAP configurée — ${cfg.imap_user} @ ${cfg.imap_host}:${cfg.imap_port}</div>`
      : `<div class="status-err">✗ ${cfg.message || 'Config manquante'}</div>`;

    main.innerHTML = `
      <div class="card config-form">
        <h3>Statut Configuration</h3>
        ${statusHTML}
      </div>
      <div class="card config-form">
        <h3>Instructions</h3>
        <p style="font-size:12px;color:var(--text-secondary);line-height:1.7;">
          1. Copiez <code>donnees/config.example.json</code> vers <code>donnees/config.json</code><br>
          2. Remplissez vos identifiants IMAP Free.fr :<br>
          &nbsp;&nbsp;• host : <strong>imap.free.fr</strong><br>
          &nbsp;&nbsp;• port : <strong>993</strong> (SSL)<br>
          &nbsp;&nbsp;• user : votre adresse Free<br>
          &nbsp;&nbsp;• password : votre mot de passe Free<br>
          3. Redémarrez le serveur <code>python ANTISPAMS/main.py</code><br>
          4. <strong>Ne commitez jamais config.json</strong> (exclu par .gitignore)
        </p>
      </div>
      <div class="card config-form">
        <h3>Scoring RGPD</h3>
        <table>
          <thead><tr><th>Critère</th><th>Points</th></tr></thead>
          <tbody>
            <tr><td>Pixel de tracking détecté</td><td>+20</td></tr>
            <tr><td>Pas de lien désabonnement</td><td>+25</td></tr>
            <tr><td>Header List-Unsubscribe absent</td><td>+15</td></tr>
            <tr><td>Liens de tracking</td><td>+20</td></tr>
            <tr><td>Expéditeur suspect (From/Reply-To)</td><td>+10</td></tr>
            <tr><td>Pas de mention RGPD (email en masse)</td><td>+10</td></tr>
          </tbody>
        </table>
        <p style="font-size:11px;color:var(--text-secondary);margin-top:8px;">Seuil haut risque : ≥60 | Risque modéré : 30-59 | Conforme : &lt;30</p>
      </div>
      <div style="text-align:right;margin-top:8px;">
        <button class="btn btn-primary" id="btn-refresh-config">Vérifier config</button>
      </div>`;

    document.getElementById('btn-refresh-config').addEventListener('click', async () => {
      await this.checkHealth();
      this.renderConfig(main);
    });
  },

  renderConfigWarning() {
    const msg = this.data.configStatus?.message || 'Configuration IMAP manquante';
    return `<div class="empty-state">
      <div style="color:var(--danger-text);margin-bottom:16px;">✗ ${msg}</div>
      <p style="font-size:12px;">Allez dans l'onglet <strong>Config</strong> pour les instructions de configuration.</p>
    </div>`;
  },

  updateStats() {
    const emails = this.data.emails;
    const total = emails.length;
    const avg = total > 0 ? Math.round(emails.reduce((s, e) => s + (e.score || 0), 0) / total) : 0;
    const haut = emails.filter(e => e.score >= 60).length;
    this.data.stats = { ...this.data.stats, total, avg, hautRisque: haut };
    this.renderStats();
  },

  updateStatsRapports() {
    this.data.stats.rapports = this.data.rapports.length;
    document.getElementById('stat-rapports').textContent = this.data.stats.rapports;
  },

  renderStats() {
    document.getElementById('stat-total').textContent = this.data.stats.total;
    document.getElementById('stat-avg').textContent = this.data.stats.avg;
    document.getElementById('stat-haut-risque').textContent = this.data.stats.hautRisque;
    document.getElementById('stat-rapports').textContent = this.data.stats.rapports;
  },

  scoreBadge(score, label) {
    const cls = label === 'danger' ? 'badge-danger' : label === 'warning' ? 'badge-warning' : 'badge-ok';
    return `<span class="badge ${cls}">${score}</span>`;
  },

  formatDate(dateStr) {
    if (!dateStr) return '—';
    try {
      const d = new Date(dateStr);
      return d.toLocaleDateString('fr-FR', { day: '2-digit', month: '2-digit', year: '2-digit' });
    } catch { return dateStr; }
  },

  formatDateISO(isoStr) {
    if (!isoStr) return '—';
    try {
      return new Date(isoStr).toLocaleString('fr-FR');
    } catch { return isoStr; }
  },

  escapeHtml(str) {
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  },

  showNotification(msg, type = 'success') {
    const el = document.getElementById('notification');
    el.textContent = msg;
    el.className = `notification ${type}`;
    setTimeout(() => { el.className = 'notification hidden'; }, 4000);
  }
};

document.addEventListener('DOMContentLoaded', () => App.init());
