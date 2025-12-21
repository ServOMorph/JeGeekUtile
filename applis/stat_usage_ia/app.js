const App = {
  data: {
    ias: [],
    clics: [],
    currentView: 'dashboard'
  },

  async init() {
    try {
      this.setFooterDate();
      await this.loadIAs();
      await this.loadClics();
      this.setupNavigation();
      this.updateStatsHeader();
      this.render('dashboard');
    } catch (error) {
      this.showNotification('Erreur initialisation: ' + error.message, 'error');
    }
  },

  setFooterDate() {
    const now = new Date();
    const dateStr = now.toLocaleDateString('fr-FR', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit'
    });
    const footerDate = document.getElementById('footer-date');
    if (footerDate) {
      footerDate.textContent = dateStr;
    }
  },

  async loadIAs() {
    try {
      const res = await fetch('donnees/ias.json');
      if (!res.ok) {
        console.error('Erreur HTTP:', res.status, res.statusText);
        throw new Error('IAs non trouvées (HTTP ' + res.status + ')');
      }
      const data = await res.json();
      this.data.ias = data.ias || [];
      console.log('IAs chargées:', this.data.ias.length);
    } catch (error) {
      console.error('Erreur chargement IAs:', error);
      this.data.ias = [];
      this.showNotification('Erreur chargement IAs: ' + error.message, 'error');
    }
  },

  async loadClics() {
    try {
      const res = await fetch('donnees/clics.json');
      if (!res.ok) throw new Error('Clics non trouvés');
      const data = await res.json();
      this.data.clics = data.clics;
    } catch (error) {
      console.error('Erreur chargement clics:', error);
      this.data.clics = [];
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
    const totalClics = this.data.clics.length;
    const clicsLocaux = this.data.clics.filter(c => {
      const ia = this.data.ias.find(i => i.id === c.ia_id);
      return ia && ia.type === 'local';
    }).length;

    const ratioLocal = totalClics > 0 ? Math.round((clicsLocaux / totalClics) * 100) : 0;

    document.getElementById('total-clics').textContent = totalClics;
    document.getElementById('ratio-local').textContent = ratioLocal + '%';
  },

  render(view) {
    this.data.currentView = view;
    const views = {
      dashboard: this.renderDashboard.bind(this),
      gestion: this.renderGestion.bind(this),
      stats: this.renderStats.bind(this)
    };

    if (views[view]) {
      document.getElementById('view').innerHTML = views[view]();
      this.attachViewEvents(view);
    }
  },

  renderDashboard() {
    if (this.data.ias.length === 0) {
      return `
        <div style="text-align: center; padding: 60px 20px;">
          <p style="color: #6b8e23; font-size: 16px; margin-bottom: 20px;">
            Aucune IA configurée
          </p>
          <button class="btn-add-ia" onclick="App.render('gestion')">
            Ajouter votre première IA
          </button>
        </div>
      `;
    }

    const iasLocales = this.data.ias.filter(ia => ia.type === 'local');
    const iasCloud = this.data.ias.filter(ia => ia.type === 'cloud');

    let html = '<div class="dashboard-wrapper">';

    // Section IAs Locales
    if (iasLocales.length > 0) {
      html += `
        <div class="ia-section">
          <div class="ia-section-header local">
            <h2>IAs Locales</h2>
            <span class="ia-count">${iasLocales.length} IA${iasLocales.length > 1 ? 's' : ''}</span>
          </div>
          <div class="dashboard-container">
      `;

      iasLocales.forEach(ia => {
        const clicsIA = this.data.clics.filter(c => c.ia_id === ia.id).length;
        html += `
          <div class="ia-card local" data-ia-id="${ia.id}">
            <div class="ia-nom">${ia.nom}</div>
            <div class="ia-type local">Local</div>
            <div class="ia-compteur">${clicsIA} clics</div>
          </div>
        `;
      });

      html += '</div></div>';
    }

    // Section IAs Cloud
    if (iasCloud.length > 0) {
      html += `
        <div class="ia-section">
          <div class="ia-section-header cloud">
            <h2>IAs Cloud</h2>
            <span class="ia-count">${iasCloud.length} IA${iasCloud.length > 1 ? 's' : ''}</span>
          </div>
          <div class="dashboard-container">
      `;

      iasCloud.forEach(ia => {
        const clicsIA = this.data.clics.filter(c => c.ia_id === ia.id).length;
        html += `
          <div class="ia-card cloud" data-ia-id="${ia.id}">
            <div class="ia-nom">${ia.nom}</div>
            <div class="ia-type cloud">Cloud</div>
            <div class="ia-compteur">${clicsIA} clics</div>
          </div>
        `;
      });

      html += '</div></div>';
    }

    html += '</div>';

    return html;
  },

  renderGestion() {
    let html = '<div class="form-container">';
    html += '<h2 style="color: #6b8e23; margin-bottom: 20px;">Ajouter une IA</h2>';
    html += `
      <form id="form-add-ia">
        <div class="form-group">
          <label>Nom de l'IA</label>
          <input type="text" id="ia-nom" placeholder="Ex: Claude, GPT-4, LLaMA..." required>
        </div>
        <div class="form-group">
          <label>Type</label>
          <select id="ia-type" required>
            <option value="local">Local</option>
            <option value="cloud">Cloud</option>
          </select>
        </div>
        <button type="submit" class="btn-submit">Ajouter</button>
      </form>
    `;
    html += '</div>';

    if (this.data.ias.length > 0) {
      html += '<div style="max-width: 600px; margin: 40px auto;">';
      html += '<h2 style="color: #6b8e23; margin-bottom: 20px;">IAs configurées</h2>';
      html += '<div class="ia-list">';

      this.data.ias.forEach(ia => {
        const clicsIA = this.data.clics.filter(c => c.ia_id === ia.id).length;
        html += `
          <div class="ia-item ${ia.type}">
            <div class="ia-info">
              <div class="ia-nom">${ia.nom}</div>
              <div class="ia-type ${ia.type}">${ia.type === 'local' ? 'Local' : 'Cloud'} - ${clicsIA} clics</div>
            </div>
            <div class="ia-actions">
              <button class="btn-delete" data-ia-id="${ia.id}">Supprimer</button>
            </div>
          </div>
        `;
      });

      html += '</div></div>';
    }

    return html;
  },

  renderStats() {
    const totalClics = this.data.clics.length;
    const clicsLocaux = this.data.clics.filter(c => {
      const ia = this.data.ias.find(i => i.id === c.ia_id);
      return ia && ia.type === 'local';
    }).length;
    const clicsCloud = totalClics - clicsLocaux;
    const ratioLocal = totalClics > 0 ? Math.round((clicsLocaux / totalClics) * 100) : 0;
    const objectifAtteint = ratioLocal >= 70;

    let html = '<div class="stats-container">';

    html += '<div class="stats-grid">';
    html += `
      <div class="metric-card">
        <div class="metric-label">Total clics</div>
        <div class="metric-value">${totalClics}</div>
      </div>
      <div class="metric-card">
        <div class="metric-label">IA Locales</div>
        <div class="metric-value">${clicsLocaux}</div>
        <div class="metric-detail">${ratioLocal}% du total</div>
      </div>
      <div class="metric-card">
        <div class="metric-label">IA Cloud</div>
        <div class="metric-value">${clicsCloud}</div>
        <div class="metric-detail">${100 - ratioLocal}% du total</div>
      </div>
    `;
    html += '</div>';

    html += `
      <div class="metric-card">
        <div class="metric-label">Objectif: 70% Local</div>
        <div class="progress-bar">
          <div class="progress-fill ${objectifAtteint ? '' : 'warning'}" style="width: ${ratioLocal}%">
            ${ratioLocal}%
          </div>
        </div>
        <div class="metric-detail" style="margin-top: 10px;">
          ${objectifAtteint ? 'Objectif atteint!' : 'Objectif non atteint'}
        </div>
      </div>
    `;

    if (this.data.ias.length > 0) {
      html += '<div class="table-container">';
      html += '<h3 style="color: #6b8e23; margin-bottom: 15px;">Détail par IA</h3>';
      html += `
        <table>
          <thead>
            <tr>
              <th>IA</th>
              <th>Type</th>
              <th>Clics</th>
              <th>% Total</th>
            </tr>
          </thead>
          <tbody>
      `;

      this.data.ias.forEach(ia => {
        const clicsIA = this.data.clics.filter(c => c.ia_id === ia.id).length;
        const pct = totalClics > 0 ? Math.round((clicsIA / totalClics) * 100) : 0;
        html += `
          <tr>
            <td>${ia.nom}</td>
            <td style="color: ${ia.type === 'local' ? '#6b8e23' : '#ff8c00'}">
              ${ia.type === 'local' ? 'Local' : 'Cloud'}
            </td>
            <td>${clicsIA}</td>
            <td>${pct}%</td>
          </tr>
        `;
      });

      html += '</tbody></table></div>';
    }

    html += '</div>';

    return html;
  },

  attachViewEvents(view) {
    if (view === 'dashboard') {
      document.querySelectorAll('.ia-card').forEach(card => {
        card.addEventListener('click', async (e) => {
          const iaId = e.currentTarget.dataset.iaId;
          await this.enregistrerClic(iaId);
        });
      });
    }

    if (view === 'gestion') {
      const form = document.getElementById('form-add-ia');
      if (form) {
        form.addEventListener('submit', async (e) => {
          e.preventDefault();
          await this.ajouterIA();
        });
      }

      document.querySelectorAll('.btn-delete').forEach(btn => {
        btn.addEventListener('click', async (e) => {
          const iaId = e.target.dataset.iaId;
          await this.supprimerIA(iaId);
        });
      });
    }
  },

  async enregistrerClic(iaId) {
    try {
      const res = await fetch('/api/clic', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ia_id: iaId})
      });

      if (!res.ok) throw new Error('Erreur enregistrement');

      await this.loadClics();
      this.updateStatsHeader();
      this.render(this.data.currentView);

      const ia = this.data.ias.find(i => i.id === iaId);
      this.showNotification(`Clic enregistré pour ${ia.nom}`, 'success');
    } catch (error) {
      this.showNotification('Erreur: ' + error.message, 'error');
    }
  },

  async ajouterIA() {
    const nom = document.getElementById('ia-nom').value;
    const type = document.getElementById('ia-type').value;

    if (!nom || !nom.trim()) {
      this.showNotification('Le nom est obligatoire', 'error');
      return;
    }

    try {
      const res = await fetch('/api/ia', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({nom, type})
      });

      if (!res.ok) {
        const errorData = await res.json();
        throw new Error(errorData.error || 'Erreur ajout IA');
      }

      await this.loadIAs();
      this.showNotification(`IA ${nom} ajoutée`, 'success');
      this.render('gestion');
    } catch (error) {
      this.showNotification('Erreur: ' + error.message, 'error');
    }
  },

  async supprimerIA(iaId) {
    if (!confirm('Supprimer cette IA et tous ses clics ?')) return;

    try {
      const res = await fetch(`/api/ia/${iaId}`, {method: 'DELETE'});

      if (!res.ok) throw new Error('Erreur suppression');

      await this.loadIAs();
      await this.loadClics();
      this.updateStatsHeader();
      this.showNotification('IA supprimée', 'success');
      this.render('gestion');
    } catch (error) {
      this.showNotification('Erreur: ' + error.message, 'error');
    }
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
