const App = {
  data: {
    ias: [],
    clics: [],
    currentView: 'dashboard',
    timeFilter: 'all',
    granularity: 'day',
    charts: {},
    currentTheme: 'nuit-foret'
  },

  async init() {
    try {
      this.loadTheme();
      this.setupThemeSelector();
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

  loadTheme() {
    const savedTheme = localStorage.getItem('theme') || 'nuit-foret';
    this.data.currentTheme = savedTheme;
    document.documentElement.setAttribute('data-theme', savedTheme);

    document.querySelectorAll('.theme-btn').forEach(btn => {
      btn.classList.toggle('active', btn.dataset.theme === savedTheme);
    });
  },

  setTheme(theme) {
    this.data.currentTheme = theme;
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('theme', theme);

    document.querySelectorAll('.theme-btn').forEach(btn => {
      btn.classList.toggle('active', btn.dataset.theme === theme);
    });

    if (this.data.currentView === 'stats' && Object.keys(this.data.charts).length > 0) {
      this.updateChartsColors();
    }
  },

  setupThemeSelector() {
    document.querySelectorAll('.theme-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        this.setTheme(btn.dataset.theme);
      });
    });
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
    const filteredClics = this.getFilteredClics();
    const totalClics = filteredClics.length;
    const clicsLocaux = filteredClics.filter(c => {
      const ia = this.data.ias.find(i => i.id === c.ia_id);
      return ia && ia.type === 'local';
    }).length;
    const clicsCloud = totalClics - clicsLocaux;
    const ratioLocal = totalClics > 0 ? Math.round((clicsLocaux / totalClics) * 100) : 0;
    const objectifAtteint = ratioLocal >= 70;

    let html = '<div class="stats-container">';

    html += `
      <div class="filters-bar">
        <div class="filters-group">
          <span class="filters-label">Période:</span>
          <button class="filter-btn ${this.data.timeFilter === 'today' ? 'active' : ''}" data-filter="today">Aujourd'hui</button>
          <button class="filter-btn ${this.data.timeFilter === '7days' ? 'active' : ''}" data-filter="7days">7 jours</button>
          <button class="filter-btn ${this.data.timeFilter === '30days' ? 'active' : ''}" data-filter="30days">30 jours</button>
          <button class="filter-btn ${this.data.timeFilter === 'all' ? 'active' : ''}" data-filter="all">Tout</button>
        </div>
        <div class="filters-group">
          <span class="filters-label">Granularité:</span>
          <button class="filter-btn ${this.data.granularity === 'hour' ? 'active' : ''}" data-granularity="hour">Par heure</button>
          <button class="filter-btn ${this.data.granularity === 'day' ? 'active' : ''}" data-granularity="day">Par jour</button>
          <button class="filter-btn ${this.data.granularity === 'week' ? 'active' : ''}" data-granularity="week">Par semaine</button>
        </div>
        <div class="action-buttons">
          <button class="action-btn" id="btn-refresh">Rafraîchir</button>
          <button class="action-btn" id="btn-export-png">Export PNG</button>
        </div>
      </div>
    `;

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

    html += '<div class="charts-grid">';

    html += `
      <div class="chart-container full-width">
        <div class="chart-title">Évolution des clics</div>
        <div class="chart-canvas">
          <canvas id="chart-evolution"></canvas>
        </div>
      </div>
    `;

    html += `
      <div class="chart-container">
        <div class="chart-title">Répartition Local vs Cloud</div>
        <div class="chart-canvas">
          <canvas id="chart-donut"></canvas>
        </div>
      </div>
    `;

    html += `
      <div class="chart-container">
        <div class="chart-title">Répartition par IA</div>
        <div class="chart-canvas">
          <canvas id="chart-ia-bars"></canvas>
        </div>
      </div>
    `;

    html += `
      <div class="chart-container full-width">
        <div class="chart-title">Comparaison Local vs Cloud dans le temps</div>
        <div class="chart-canvas">
          <canvas id="chart-comparison"></canvas>
        </div>
      </div>
    `;

    html += `
      <div class="chart-container full-width">
        <div class="chart-title">Activité par heure de la journée</div>
        <div class="chart-canvas">
          <canvas id="chart-hourly"></canvas>
        </div>
      </div>
    `;

    html += '</div>';

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
        const clicsIA = filteredClics.filter(c => c.ia_id === ia.id).length;
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

  getFilteredClics() {
    const now = new Date();
    let startDate = null;

    switch(this.data.timeFilter) {
      case 'today':
        startDate = new Date(now.getFullYear(), now.getMonth(), now.getDate());
        break;
      case '7days':
        startDate = new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000);
        break;
      case '30days':
        startDate = new Date(now.getTime() - 30 * 24 * 60 * 60 * 1000);
        break;
      default:
        return this.data.clics;
    }

    return this.data.clics.filter(c => new Date(c.timestamp) >= startDate);
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

    if (view === 'stats') {
      document.querySelectorAll('.filter-btn[data-filter]').forEach(btn => {
        btn.addEventListener('click', (e) => {
          this.data.timeFilter = e.target.dataset.filter;
          this.render('stats');
        });
      });

      document.querySelectorAll('.filter-btn[data-granularity]').forEach(btn => {
        btn.addEventListener('click', (e) => {
          this.data.granularity = e.target.dataset.granularity;
          this.render('stats');
        });
      });

      const btnRefresh = document.getElementById('btn-refresh');
      if (btnRefresh) {
        btnRefresh.addEventListener('click', async () => {
          await this.loadClics();
          await this.loadIAs();
          this.updateStatsHeader();
          this.render('stats');
          this.showNotification('Données actualisées', 'success');
        });
      }

      const btnExportPng = document.getElementById('btn-export-png');
      if (btnExportPng) {
        btnExportPng.addEventListener('click', () => {
          this.exportChartsAsPNG();
        });
      }

      this.createCharts();
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
  },

  destroyCharts() {
    Object.keys(this.data.charts).forEach(key => {
      if (this.data.charts[key]) {
        this.data.charts[key].destroy();
      }
    });
    this.data.charts = {};
  },

  createCharts() {
    this.destroyCharts();

    setTimeout(() => {
      this.createEvolutionChart();
      this.createDonutChart();
      this.createIABarsChart();
      this.createComparisonChart();
      this.createHourlyChart();
    }, 100);
  },

  getTimeSeriesData() {
    const filteredClics = this.getFilteredClics();
    const grouped = {};

    filteredClics.forEach(clic => {
      const date = new Date(clic.timestamp);
      let key;

      switch(this.data.granularity) {
        case 'hour':
          key = `${date.getFullYear()}-${String(date.getMonth()+1).padStart(2,'0')}-${String(date.getDate()).padStart(2,'0')} ${String(date.getHours()).padStart(2,'0')}:00`;
          break;
        case 'week':
          const weekStart = new Date(date);
          weekStart.setDate(date.getDate() - date.getDay());
          key = `${weekStart.getFullYear()}-${String(weekStart.getMonth()+1).padStart(2,'0')}-${String(weekStart.getDate()).padStart(2,'0')}`;
          break;
        default:
          key = `${date.getFullYear()}-${String(date.getMonth()+1).padStart(2,'0')}-${String(date.getDate()).padStart(2,'0')}`;
      }

      if (!grouped[key]) {
        grouped[key] = { total: 0, local: 0, cloud: 0 };
      }

      grouped[key].total++;

      const ia = this.data.ias.find(i => i.id === clic.ia_id);
      if (ia && ia.type === 'local') {
        grouped[key].local++;
      } else {
        grouped[key].cloud++;
      }
    });

    const sortedKeys = Object.keys(grouped).sort();
    return sortedKeys.map(key => ({
      date: key,
      total: grouped[key].total,
      local: grouped[key].local,
      cloud: grouped[key].cloud
    }));
  },

  createEvolutionChart() {
    const canvas = document.getElementById('chart-evolution');
    if (!canvas) return;

    const timeData = this.getTimeSeriesData();
    const colors = this.getThemeColors();

    this.data.charts.evolution = new Chart(canvas, {
      type: 'line',
      data: {
        labels: timeData.map(d => d.date),
        datasets: [{
          label: 'Total clics',
          data: timeData.map(d => d.total),
          borderColor: colors.accentLocal,
          backgroundColor: colors.accentLocal + '1a',
          tension: 0.3,
          fill: true
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            labels: { color: colors.textPrimary }
          }
        },
        scales: {
          y: {
            beginAtZero: true,
            ticks: { color: colors.textPrimary, precision: 0 },
            grid: { color: colors.gridColor }
          },
          x: {
            ticks: { color: colors.textPrimary, maxRotation: 45, minRotation: 45 },
            grid: { color: colors.gridColor }
          }
        }
      }
    });
  },

  createDonutChart() {
    const canvas = document.getElementById('chart-donut');
    if (!canvas) return;

    const filteredClics = this.getFilteredClics();
    const clicsLocaux = filteredClics.filter(c => {
      const ia = this.data.ias.find(i => i.id === c.ia_id);
      return ia && ia.type === 'local';
    }).length;
    const clicsCloud = filteredClics.length - clicsLocaux;
    const colors = this.getThemeColors();

    this.data.charts.donut = new Chart(canvas, {
      type: 'doughnut',
      data: {
        labels: ['Local', 'Cloud'],
        datasets: [{
          data: [clicsLocaux, clicsCloud],
          backgroundColor: [colors.accentLocal, colors.accentCloud],
          borderColor: colors.bgMain,
          borderWidth: 2
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: 'bottom',
            labels: { color: colors.textPrimary, padding: 15 }
          }
        }
      }
    });
  },

  createIABarsChart() {
    const canvas = document.getElementById('chart-ia-bars');
    if (!canvas) return;

    const filteredClics = this.getFilteredClics();
    const iaStats = this.data.ias.map(ia => ({
      nom: ia.nom,
      clics: filteredClics.filter(c => c.ia_id === ia.id).length,
      type: ia.type
    })).sort((a, b) => b.clics - a.clics);
    const colors = this.getThemeColors();

    this.data.charts.iaBars = new Chart(canvas, {
      type: 'bar',
      data: {
        labels: iaStats.map(s => s.nom),
        datasets: [{
          label: 'Clics',
          data: iaStats.map(s => s.clics),
          backgroundColor: iaStats.map(s => s.type === 'local' ? colors.accentLocal : colors.accentCloud),
          borderColor: colors.bgMain,
          borderWidth: 1
        }]
      },
      options: {
        indexAxis: 'y',
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false }
        },
        scales: {
          x: {
            beginAtZero: true,
            ticks: { color: colors.textPrimary, precision: 0 },
            grid: { color: colors.gridColor }
          },
          y: {
            ticks: { color: colors.textPrimary },
            grid: { display: false }
          }
        }
      }
    });
  },

  createComparisonChart() {
    const canvas = document.getElementById('chart-comparison');
    if (!canvas) return;

    const timeData = this.getTimeSeriesData();
    const colors = this.getThemeColors();

    this.data.charts.comparison = new Chart(canvas, {
      type: 'line',
      data: {
        labels: timeData.map(d => d.date),
        datasets: [
          {
            label: 'Local',
            data: timeData.map(d => d.local),
            borderColor: colors.accentLocal,
            backgroundColor: colors.accentLocal + '33',
            tension: 0.3,
            fill: true
          },
          {
            label: 'Cloud',
            data: timeData.map(d => d.cloud),
            borderColor: colors.accentCloud,
            backgroundColor: colors.accentCloud + '33',
            tension: 0.3,
            fill: true
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            labels: { color: colors.textPrimary }
          }
        },
        scales: {
          y: {
            beginAtZero: true,
            ticks: { color: colors.textPrimary, precision: 0 },
            grid: { color: colors.gridColor }
          },
          x: {
            ticks: { color: colors.textPrimary, maxRotation: 45, minRotation: 45 },
            grid: { color: colors.gridColor }
          }
        }
      }
    });
  },

  createHourlyChart() {
    const canvas = document.getElementById('chart-hourly');
    if (!canvas) return;

    const filteredClics = this.getFilteredClics();
    const hourlyData = new Array(24).fill(0);

    filteredClics.forEach(clic => {
      const hour = new Date(clic.timestamp).getHours();
      hourlyData[hour]++;
    });
    const colors = this.getThemeColors();

    this.data.charts.hourly = new Chart(canvas, {
      type: 'bar',
      data: {
        labels: Array.from({length: 24}, (_, i) => `${String(i).padStart(2, '0')}h`),
        datasets: [{
          label: 'Clics',
          data: hourlyData,
          backgroundColor: colors.accentLocal,
          borderColor: colors.bgMain,
          borderWidth: 1
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false }
        },
        scales: {
          y: {
            beginAtZero: true,
            ticks: { color: colors.textPrimary, precision: 0 },
            grid: { color: colors.gridColor }
          },
          x: {
            ticks: { color: colors.textPrimary },
            grid: { color: colors.gridColor }
          }
        }
      }
    });
  },

  exportChartsAsPNG() {
    const chartIds = ['chart-evolution', 'chart-donut', 'chart-ia-bars', 'chart-comparison', 'chart-hourly'];

    chartIds.forEach((id, index) => {
      const canvas = document.getElementById(id);
      if (canvas) {
        setTimeout(() => {
          const link = document.createElement('a');
          link.download = `${id}-${new Date().getTime()}.png`;
          link.href = canvas.toDataURL('image/png');
          link.click();
        }, index * 200);
      }
    });

    this.showNotification('Export des graphiques en cours...', 'success');
  },

  getThemeColors() {
    const root = getComputedStyle(document.documentElement);
    return {
      accentLocal: root.getPropertyValue('--accent-local').trim(),
      accentCloud: root.getPropertyValue('--accent-cloud').trim(),
      textPrimary: root.getPropertyValue('--text-primary').trim(),
      gridColor: root.getPropertyValue('--grid-color').trim(),
      bgMain: root.getPropertyValue('--bg-main').trim()
    };
  },

  updateChartsColors() {
    this.destroyCharts();
    this.createCharts();
  }
};

document.addEventListener('DOMContentLoaded', () => {
  App.init();
});
