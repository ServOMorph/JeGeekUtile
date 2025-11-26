const App = {
  data: {
    config: null,
    agents: [],
    sessions: null,
    currentView: 'pyramide'
  },

  async init() {
    try {
      await this.loadConfig();
      await this.loadAgents();
      await this.loadSessions();
      this.setupNavigation();
      this.updateStatsHeader();
      this.render('pyramide');
    } catch (error) {
      this.showNotification('Erreur initialisation: ' + error.message, 'error');
    }
  },

  async loadConfig() {
    try {
      const res = await fetch('config.json');
      if (!res.ok) throw new Error('Config non trouvée');
      this.data.config = await res.json();
    } catch (error) {
      console.error('Erreur chargement config:', error);
      this.data.config = {ui: {refresh_ms: 5000}, tests: {}, trace: {}};
    }
  },

  async loadAgents() {
    try {
      const res = await fetch('donnees/agents.json');
      if (!res.ok) throw new Error('Agents non trouvés');
      const data = await res.json();
      this.data.agents = data.agents;
    } catch (error) {
      console.error('Erreur chargement agents:', error);
      this.data.agents = [];
    }
  },

  async loadSessions() {
    try {
      const res = await fetch('donnees/sessions.json');
      if (!res.ok) throw new Error('Sessions non trouvées');
      this.data.sessions = await res.json();
    } catch (error) {
      console.error('Erreur chargement sessions:', error);
      this.data.sessions = {sessions: [], index: {}, stats: {total_sessions: 0, score_moyen: 0}};
    }
  },

  setupNavigation() {
    const buttons = document.querySelectorAll('nav button');
    buttons.forEach(btn => {
      btn.addEventListener('click', () => {
        buttons.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        const view = btn.dataset.view;
        this.render(view);
      });
    });
  },

  updateStatsHeader() {
    const stats = this.data.sessions.stats;
    const html = `
      <div class="stat-item">
        <span class="stat-label">Sessions</span>
        <span class="stat-value">${stats.total_sessions}</span>
      </div>
      <div class="stat-item">
        <span class="stat-label">Score moyen</span>
        <span class="stat-value">${stats.score_moyen}%</span>
      </div>
      <div class="stat-item">
        <span class="stat-label">Agents</span>
        <span class="stat-value">${this.data.agents.length}</span>
      </div>
    `;
    document.getElementById('stats-header').innerHTML = html;
  },

  render(view) {
    this.data.currentView = view;
    const views = {
      pyramide: this.renderPyramide.bind(this),
      tests: this.renderTests.bind(this),
      config: this.renderConfig.bind(this),
      recherche: this.renderRecherche.bind(this)
    };

    if (views[view]) {
      document.getElementById('view').innerHTML = views[view]();
      this.attachViewEvents(view);
    }
  },

  renderPyramide() {
    const niveaux = {};
    this.data.agents.forEach(agent => {
      if (!niveaux[agent.niveau]) niveaux[agent.niveau] = [];
      niveaux[agent.niveau].push(agent);
    });

    let html = '<div class="pyramide">';

    Object.keys(niveaux).sort().forEach(niveau => {
      html += '<div class="pyramide-niveau">';
      niveaux[niveau].forEach(agent => {
        html += `
          <div class="agent-card niveau-${agent.niveau}" data-agent-id="${agent.id}">
            <div class="agent-nom">${agent.nom}</div>
            <div class="agent-role">${agent.role}</div>
            <div class="agent-competences">
              ${agent.competences.map(c => `<span class="competence-tag">${c}</span>`).join('')}
            </div>
            <div class="agent-score">${agent.score}%</div>
          </div>
        `;
      });
      html += '</div>';
    });

    html += `
      <button class="btn-creer-agent" id="btn-creer-agent">+ Créer nouvel agent</button>
    </div>`;

    return html;
  },

  renderTests() {
    let html = '<div class="tests-container">';

    html += '<div class="metrics-grid">';

    const sessions = this.data.sessions.sessions;
    const derniereSession = sessions[sessions.length - 1];

    html += `
      <div class="metric-card">
        <div class="metric-label">Dernier score</div>
        <div class="metric-value">${derniereSession ? derniereSession.score : 0}%</div>
        <div class="metric-detail">${derniereSession ? new Date(derniereSession.date).toLocaleString('fr-FR') : 'Aucun test'}</div>
      </div>
      <div class="metric-card">
        <div class="metric-label">Tests totaux</div>
        <div class="metric-value">${this.data.sessions.stats.total_sessions}</div>
        <div class="metric-detail">Score moyen: ${this.data.sessions.stats.score_moyen}%</div>
      </div>
      <div class="metric-card">
        <div class="metric-label">Derniers résultats</div>
        <div class="metric-value">${derniereSession ? `${derniereSession.reussis}/${derniereSession.total}` : '0/0'}</div>
        <div class="metric-detail">${derniereSession ? 'tests réussis' : 'Aucune session'}</div>
      </div>
    `;

    html += '</div>';

    html += '<button class="btn-executer-tests" id="btn-executer-tests">▶ Exécuter tous les tests</button>';

    html += '<div class="test-section"><h3>Historique des sessions</h3>';

    if (sessions.length > 0) {
      sessions.slice().reverse().forEach((session) => {
        const statusClass = session.score >= 90 ? 'ok' : session.score >= 80 ? 'ok' : 'erreur';
        html += `
          <div class="test-item">
            <span class="test-nom">
              ${session.id} - ${new Date(session.date).toLocaleString('fr-FR')}
              <br><small style="color: #6b8e23;">Agents: ${session.agents ? session.agents.join(', ') : 'N/A'}</small>
            </span>
            <span class="test-statut ${statusClass}">${session.score}% (${session.reussis}/${session.total})</span>
          </div>
        `;
      });
    } else {
      html += '<p style="color: #6b8e23; padding: 20px; text-align: center;">Aucune session enregistrée</p>';
    }

    html += '</div>';

    this.data.agents.forEach(agent => {
      html += `
        <div class="test-section">
          <h3>${agent.nom} - ${agent.tests.length} tests configurés</h3>
          ${agent.tests.map(test => `
            <div class="test-item">
              <span class="test-nom">${test.nom}</span>
              <span class="test-statut ok">Prêt</span>
            </div>
          `).join('')}
        </div>
      `;
    });

    html += '</div>';

    return html;
  },

  renderConfig() {
    const config = this.data.config;

    let html = '<div class="config-container">';

    html += `
      <div class="config-section">
        <h3>Interface</h3>
        <div class="form-group">
          <label>Rafraîchissement (ms)</label>
          <input type="number" id="config-refresh" value="${config.ui.refresh_ms}">
        </div>
        <div class="form-group">
          <label>Pixels blancs max (%)</label>
          <input type="number" id="config-pixels" value="${config.ui.pixels_blancs_max_pct}">
        </div>
      </div>

      <div class="config-section">
        <h3>Tests</h3>
        <div class="form-group">
          <label>Seuil réussite (%)</label>
          <input type="number" id="config-seuil" value="${config.tests.seuil_reussite}">
        </div>
        <div class="form-group">
          <label>Timeout (secondes)</label>
          <input type="number" id="config-timeout" value="${config.tests.timeout_sec}">
        </div>
        <div class="form-group">
          <label>Itérations</label>
          <input type="number" id="config-iterations" value="${config.tests.iterations}">
        </div>
      </div>

      <div class="config-section">
        <h3>Traçabilité</h3>
        <div class="form-group">
          <label>Rétention (jours)</label>
          <input type="number" id="config-retention" value="${config.trace.retention_jours}">
        </div>
        <div class="form-group">
          <label>Niveau détail</label>
          <select id="config-niveau">
            <option value="minimal" ${config.trace.niveau === 'minimal' ? 'selected' : ''}>Minimal</option>
            <option value="standard" ${config.trace.niveau === 'standard' ? 'selected' : ''}>Standard</option>
            <option value="complet" ${config.trace.niveau === 'complet' ? 'selected' : ''}>Complet</option>
          </select>
        </div>
      </div>

      <button class="btn-sauvegarder" id="btn-sauvegarder-config">Sauvegarder configuration</button>
    </div>`;

    return html;
  },

  renderRecherche() {
    let html = '<div class="search-container">';

    html += `
      <div class="search-box">
        <input type="text" class="search-input" id="search-input" placeholder="Rechercher dans l'historique...">
        <div class="search-filters">
          <button class="filter-btn" data-filter="all">Tout</button>
          <button class="filter-btn" data-filter="robert">Robert</button>
          <button class="filter-btn" data-filter="halu">Halu</button>
          <button class="filter-btn" data-filter="promptparfait">PromptParfait</button>
          <button class="filter-btn" data-filter="score-90">Score ≥ 90%</button>
          <button class="filter-btn" data-filter="score-80">Score ≥ 80%</button>
        </div>
      </div>

      <div class="search-results" id="search-results">
        ${this.renderSearchResults(this.data.sessions.sessions)}
      </div>
    </div>`;

    return html;
  },

  renderSearchResults(sessions) {
    if (!sessions || sessions.length === 0) {
      return '<p style="color: #6b8e23; text-align: center; padding: 40px;">Aucune session trouvée</p>';
    }

    const sortedSessions = [...sessions].reverse();

    return sortedSessions.map(session => `
      <div class="result-item" data-session-id="${session.id}">
        <div class="result-header">
          <span class="result-id">${session.id}</span>
          <span class="result-score">${session.score}%</span>
        </div>
        <div class="result-meta">
          ${new Date(session.date).toLocaleString('fr-FR')} |
          Agents: ${session.agents ? session.agents.join(', ') : 'N/A'} |
          ${session.reussis}/${session.total} tests réussis
        </div>
      </div>
    `).join('');
  },

  attachViewEvents(view) {
    if (view === 'pyramide') {
      const btnCreer = document.getElementById('btn-creer-agent');
      if (btnCreer) {
        btnCreer.addEventListener('click', () => this.creerAgent());
      }
    }

    if (view === 'tests') {
      const btnExecuter = document.getElementById('btn-executer-tests');
      if (btnExecuter) {
        btnExecuter.addEventListener('click', () => this.executerTests());
      }
    }

    if (view === 'config') {
      const btnSauvegarder = document.getElementById('btn-sauvegarder-config');
      if (btnSauvegarder) {
        btnSauvegarder.addEventListener('click', () => this.sauvegarderConfig());
      }
    }

    if (view === 'recherche') {
      const searchInput = document.getElementById('search-input');
      const filterBtns = document.querySelectorAll('.filter-btn');

      if (searchInput) {
        searchInput.addEventListener('input', (e) => this.rechercherSessions(e.target.value));
      }

      filterBtns.forEach(btn => {
        btn.addEventListener('click', () => {
          filterBtns.forEach(b => b.classList.remove('active'));
          btn.classList.add('active');
          this.filtrerSessions(btn.dataset.filter);
        });
      });
    }
  },

  creerAgent() {
    const nom = prompt('Nom de l\'agent:');
    if (!nom) return;

    const role = prompt('Rôle:');
    if (!role) return;

    const competences = prompt('Compétences (séparées par virgules):');
    if (!competences) return;

    const nouvelAgent = {
      id: nom.toLowerCase().replace(/\s+/g, ''),
      nom: nom,
      role: role,
      niveau: 1,
      parent: 'robert',
      competences: competences.split(',').map(c => c.trim()),
      score: 0,
      tests: []
    };

    this.data.agents.push(nouvelAgent);
    this.showNotification(`Agent ${nom} créé avec succès`, 'success');
    this.render('pyramide');
  },

  async executerTests() {
    const btn = document.getElementById('btn-executer-tests');
    if (btn) {
      btn.disabled = true;
      btn.innerHTML = '<span class="loading"></span> Exécution en cours...';
    }

    this.showNotification('Lancement tests Python...', 'success');

    try {
      const response = await fetch('/run-tests', {
        method: 'POST'
      });

      if (!response.ok) {
        throw new Error('Erreur exécution tests');
      }

      const result = await response.json();

      await this.loadSessions();
      await this.loadAgents();
      this.updateStatsHeader();

      this.showNotification(`Tests terminés: ${result.score}% (${result.reussis}/${result.total})`, 'success');
      this.render('tests');
    } catch (error) {
      this.showNotification('Tests Python non disponibles - Simulation activée', 'error');

      await new Promise(resolve => setTimeout(resolve, 1000));

      await this.loadSessions();
      await this.loadAgents();
      this.updateStatsHeader();
      this.render('tests');

      this.showNotification('Résultats mis à jour', 'success');
    } finally {
      if (btn) {
        btn.disabled = false;
        btn.innerHTML = '▶ Exécuter tous les tests';
      }
    }
  },

  sauvegarderConfig() {
    this.data.config.ui.refresh_ms = parseInt(document.getElementById('config-refresh').value);
    this.data.config.ui.pixels_blancs_max_pct = parseInt(document.getElementById('config-pixels').value);
    this.data.config.tests.seuil_reussite = parseInt(document.getElementById('config-seuil').value);
    this.data.config.tests.timeout_sec = parseInt(document.getElementById('config-timeout').value);
    this.data.config.tests.iterations = parseInt(document.getElementById('config-iterations').value);
    this.data.config.trace.retention_jours = parseInt(document.getElementById('config-retention').value);
    this.data.config.trace.niveau = document.getElementById('config-niveau').value;

    this.showNotification('Configuration sauvegardée', 'success');
  },

  rechercherSessions(query) {
    const filtered = this.data.sessions.sessions.filter(s =>
      s.id.toLowerCase().includes(query.toLowerCase()) ||
      (s.agents && s.agents.some(a => a.toLowerCase().includes(query.toLowerCase())))
    );

    document.getElementById('search-results').innerHTML = this.renderSearchResults(filtered);
  },

  filtrerSessions(filter) {
    let filtered = this.data.sessions.sessions;

    if (filter === 'robert') {
      filtered = filtered.filter(s => s.agents && s.agents.includes('robert'));
    } else if (filter === 'halu') {
      filtered = filtered.filter(s => s.agents && s.agents.includes('halu'));
    } else if (filter === 'promptparfait') {
      filtered = filtered.filter(s => s.agents && s.agents.includes('promptparfait'));
    } else if (filter === 'score-90') {
      filtered = filtered.filter(s => s.score >= 90);
    } else if (filter === 'score-80') {
      filtered = filtered.filter(s => s.score >= 80);
    }

    document.getElementById('search-results').innerHTML = this.renderSearchResults(filtered);
  },

  showNotification(message, type = 'success') {
    const notification = document.getElementById('notification');
    notification.textContent = message;
    notification.className = `notification ${type}`;

    setTimeout(() => {
      notification.classList.add('hidden');
    }, 3000);
  }
};

document.addEventListener('DOMContentLoaded', () => {
  App.init();
});
