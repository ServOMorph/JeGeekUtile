/* =================================================================
   MODÈLE STANDARD - APPLICATIONS JE GEEK UTILE
   Structure application Vanilla JS
   ================================================================= */

const App = {
  data: {
    currentView: 'view1'
    // Ajouter vos données ici
  },

  async init() {
    try {
      this.setFooterDate();
      await this.loadData();
      this.setupNavigation();
      this.updateStatsHeader();
      this.render('view1');
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

  async loadData() {
    try {
      // Charger vos données ici
      // Exemple:
      // const res = await fetch('donnees/data.json');
      // this.data.items = await res.json();
    } catch (error) {
      console.error('Erreur chargement données:', error);
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
    // Mettre à jour les statistiques du header
    // Exemple:
    // document.getElementById('stat-1').textContent = this.data.count;
  },

  render(view) {
    this.data.currentView = view;
    const views = {
      view1: this.renderView1.bind(this),
      view2: this.renderView2.bind(this),
      view3: this.renderView3.bind(this)
    };

    if (views[view]) {
      document.getElementById('view').innerHTML = views[view]();
      this.attachViewEvents(view);
    }
  },

  renderView1() {
    return `
      <div class="text-center">
        <h2 style="color: var(--text-secondary); margin-bottom: 20px;">Vue 1</h2>
        <p>Contenu de la vue 1</p>
      </div>
    `;
  },

  renderView2() {
    return `
      <div class="text-center">
        <h2 style="color: var(--text-secondary); margin-bottom: 20px;">Vue 2</h2>
        <p>Contenu de la vue 2</p>
      </div>
    `;
  },

  renderView3() {
    return `
      <div class="text-center">
        <h2 style="color: var(--text-secondary); margin-bottom: 20px;">Vue 3</h2>
        <p>Contenu de la vue 3</p>
      </div>
    `;
  },

  attachViewEvents(view) {
    // Attacher les événements spécifiques à chaque vue
    if (view === 'view1') {
      // Événements vue 1
    }

    if (view === 'view2') {
      // Événements vue 2
    }

    if (view === 'view3') {
      // Événements vue 3
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

// Initialisation au chargement DOM
document.addEventListener('DOMContentLoaded', () => {
  App.init();
});
