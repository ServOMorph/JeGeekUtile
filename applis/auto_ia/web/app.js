let historyLocal = [];

async function checkHealth() {
  const apiUrl = document.getElementById('api-url').value;
  const healthDot = document.getElementById('health-dot');
  const healthText = document.getElementById('health-text');

  try {
    const response = await fetch(`${apiUrl}/health`);
    const data = await response.json();

    if (data.status === 'ok') {
      healthDot.className = 'health-dot ok';
      healthText.textContent = 'Serveur actif';
    } else {
      healthDot.className = 'health-dot error';
      healthText.textContent = 'Erreur serveur';
    }
  } catch (error) {
    healthDot.className = 'health-dot error';
    healthText.textContent = 'Serveur injoignable';
  }
}

async function getWorkerStatus() {
  const apiUrl = document.getElementById('api-url').value;
  try {
    const response = await fetch(`${apiUrl}/queue/status`);
    const data = await response.json();
    return data;
  } catch (error) {
    return null;
  }
}

async function getConfigStatus() {
  const apiUrl = document.getElementById('api-url').value;
  try {
    const response = await fetch(`${apiUrl}/config/status`);
    const data = await response.json();
    return data;
  } catch (error) {
    return null;
  }
}

async function fetchZones() {
  const apiUrl = document.getElementById('api-url').value;
  try {
    const response = await fetch(`${apiUrl}/zones`);
    const data = await response.json();
    return data.zones || [];
  } catch (error) {
    return [];
  }
}

async function createZone(name, x, y, width, height) {
  const apiUrl = document.getElementById('api-url').value;
  try {
    const response = await fetch(`${apiUrl}/zones`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name, x, y, width, height })
    });
    return await response.json();
  } catch (error) {
    return { status: 'error', message: error.message };
  }
}

async function deleteZone(name) {
  const apiUrl = document.getElementById('api-url').value;
  try {
    const response = await fetch(`${apiUrl}/zones/${name}`, {
      method: 'DELETE'
    });
    return await response.json();
  } catch (error) {
    return { status: 'error', message: error.message };
  }
}

async function fetchQueue() {
  const apiUrl = document.getElementById('api-url').value;
  try {
    const response = await fetch(`${apiUrl}/queue/actions`);
    const data = await response.json();
    return data.items || [];
  } catch (error) {
    return [];
  }
}

async function addToQueue(type, params, source = 'web', priority = 0, label = null) {
  const apiUrl = document.getElementById('api-url').value;
  try {
    const response = await fetch(`${apiUrl}/queue/actions`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ type, params, source, priority, label })
    });
    return await response.json();
  } catch (error) {
    return { status: 'error', message: error.message };
  }
}

async function executeAction(type, params) {
  const apiUrl = document.getElementById('api-url').value;
  try {
    const response = await fetch(`${apiUrl}/action`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ type, params })
    });
    return await response.json();
  } catch (error) {
    return { status: 'error', message: error.message };
  }
}

async function controlWorker(command) {
  const apiUrl = document.getElementById('api-url').value;
  try {
    const response = await fetch(`${apiUrl}/queue/control`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ command })
    });
    return await response.json();
  } catch (error) {
    return { status: 'error', message: error.message };
  }
}

function addToHistory(type, params, result) {
  const historyItem = {
    type,
    params,
    result,
    timestamp: new Date().toLocaleTimeString()
  };

  historyLocal.unshift(historyItem);
  if (historyLocal.length > 20) historyLocal.pop();
  renderHistory();
}

async function renderQueue() {
  const queueList = document.getElementById('queue-list');
  const actions = await fetchQueue();

  if (actions.length === 0) {
    queueList.innerHTML = '<div class="empty-state">Aucune action en file</div>';
    return;
  }

  const limitedActions = actions.slice(0, 30);

  queueList.innerHTML = limitedActions.map((action, index) => {
    const shortId = action.id.substring(0, 8);
    const created = new Date(action.created_at * 1000).toLocaleTimeString();
    const lastUpdate = action.finished_at || action.started_at || action.created_at;
    const lastUpdateTime = new Date(lastUpdate * 1000).toLocaleTimeString();

    return `
      <div class="action-item">
        <div class="action-type">
          #${index + 1} ${action.type}
          <span class="status-badge ${action.status}">${action.status}</span>
        </div>
        <div class="action-params">${JSON.stringify(action.params)}</div>
        <div class="action-meta">
          <span>ID: ${shortId}</span>
          <span>Source: ${action.source || 'unknown'}</span>
          <span>Priority: ${action.priority || 0}</span>
          ${action.label ? `<span>Label: ${action.label}</span>` : ''}
          <span>Créé: ${created}</span>
          <span>Maj: ${lastUpdateTime}</span>
        </div>
        ${action.error ? `<div class="action-result error">Erreur: ${action.error}</div>` : ''}
      </div>
    `;
  }).join('');
}

function renderHistory() {
  const historyList = document.getElementById('history-list');

  if (historyLocal.length === 0) {
    historyList.innerHTML = '<div class="empty-state">Aucun historique</div>';
    return;
  }

  historyList.innerHTML = historyLocal.map((item) => `
    <div class="action-item">
      <div class="action-type">${item.timestamp} - ${item.type}</div>
      <div class="action-params">${JSON.stringify(item.params)}</div>
      <div class="action-result ${item.result.status}">
        ${item.result.status}: ${item.result.message}
      </div>
    </div>
  `).join('');
}

async function updateWorkerStatus() {
  const status = await getWorkerStatus();
  const workerIndicator = document.getElementById('worker-status');

  if (status) {
    workerIndicator.textContent = `Worker: ${status.worker_status} (${status.queue_count} actions)`;
  } else {
    workerIndicator.textContent = 'Worker: inconnu';
  }
}

async function updateConfigStatus() {
  const config = await getConfigStatus();

  if (config) {
    const safeModeEl = document.getElementById('safe-mode-indicator');
    safeModeEl.textContent = config.safe_mode ? 'ON' : 'OFF';
    safeModeEl.style.color = config.safe_mode ? '#86efac' : '#fbbf24';

    document.getElementById('delay-indicator').textContent = `${config.min_delay_seconds}s`;
    document.getElementById('rate-limit-indicator').textContent = config.max_actions_per_minute;
  }
}

async function renderZones() {
  const zones = await fetchZones();
  const zonesList = document.getElementById('zones-list');

  if (zones.length === 0) {
    zonesList.innerHTML = '<div class="empty-state">Aucune zone définie</div>';
    return;
  }

  zonesList.innerHTML = zones.map(zone => `
    <div style="display: flex; justify-content: space-between; align-items: center; padding: 6px 8px; background: var(--bg-secondary); border-radius: 3px;">
      <div>
        <strong>${zone.name}</strong>: (${zone.x}, ${zone.y})${zone.width ? ` ${zone.width}x${zone.height}` : ''}
      </div>
      <button class="btn" style="padding: 2px 6px; font-size: 11px;" data-delete-zone="${zone.name}">×</button>
    </div>
  `).join('');

  document.querySelectorAll('[data-delete-zone]').forEach(btn => {
    btn.addEventListener('click', async () => {
      const zoneName = btn.getAttribute('data-delete-zone');
      await deleteZone(zoneName);
      await renderZones();
    });
  });
}

function updateModeIndicator() {
  const mode = document.querySelector('input[name="exec-mode"]:checked').value;
  const indicator = document.getElementById('mode-indicator');
  indicator.textContent = `Mode: ${mode}`;
}

document.querySelectorAll('input[name="exec-mode"]').forEach(radio => {
  radio.addEventListener('change', updateModeIndicator);
});

document.getElementById('action-form').addEventListener('submit', async (e) => {
  e.preventDefault();

  const type = document.getElementById('action-type').value;
  const paramsText = document.getElementById('action-params').value;
  const mode = document.querySelector('input[name="exec-mode"]:checked').value;

  let params;
  try {
    params = JSON.parse(paramsText);
  } catch (error) {
    alert('Erreur JSON dans les paramètres');
    return;
  }

  if (mode === 'direct') {
    const result = await executeAction(type, params);
    addToHistory(type, params, result);
  } else {
    const result = await addToQueue(type, params, 'web', 0, null);
    if (result.status === 'ok') {
      addToHistory(type, params, { status: 'ok', message: `Enfilé: ${result.action_id}` });
      await renderQueue();
    } else {
      addToHistory(type, params, result);
    }
  }
});

document.getElementById('btn-start').addEventListener('click', async () => {
  await controlWorker('start');
  await updateWorkerStatus();
});

document.getElementById('btn-pause').addEventListener('click', async () => {
  await controlWorker('pause');
  await updateWorkerStatus();
});

document.getElementById('btn-resume').addEventListener('click', async () => {
  await controlWorker('resume');
  await updateWorkerStatus();
});

document.getElementById('btn-stop').addEventListener('click', async () => {
  await controlWorker('stop');
  await updateWorkerStatus();
  await renderQueue();
});

const presets = {
  'copy-zone': {
    type: 'clipboard_copy',
    params: { text: 'Texte zone automatique' },
    label: 'preset_copy_zone'
  },
  'double-click': {
    type: 'mouse_click',
    params: { x: 500, y: 500, button: 'left' },
    label: 'preset_double_click'
  },
  'paste-sequence': {
    type: 'clipboard_paste',
    params: {},
    label: 'preset_paste_sequence'
  }
};

document.querySelectorAll('[data-preset]').forEach(btn => {
  btn.addEventListener('click', async () => {
    const presetName = btn.getAttribute('data-preset');
    const preset = presets[presetName];

    if (preset) {
      document.querySelector('input[name="exec-mode"][value="queue"]').checked = true;
      updateModeIndicator();

      document.getElementById('action-type').value = preset.type;
      document.getElementById('action-params').value = JSON.stringify(preset.params, null, 2);

      const result = await addToQueue(preset.type, preset.params, 'preset', 0, preset.label);
      if (result.status === 'ok') {
        addToHistory(preset.type, preset.params, { status: 'ok', message: `Preset enfilé: ${result.action_id}` });
        await renderQueue();
      }
    }
  });
});

document.getElementById('btn-add-zone').addEventListener('click', () => {
  document.getElementById('zone-form').style.display = 'block';
  document.getElementById('zone-name').value = '';
  document.getElementById('zone-x').value = '';
  document.getElementById('zone-y').value = '';
  document.getElementById('zone-width').value = '';
  document.getElementById('zone-height').value = '';
});

document.getElementById('btn-cancel-zone').addEventListener('click', () => {
  document.getElementById('zone-form').style.display = 'none';
});

document.getElementById('btn-save-zone').addEventListener('click', async () => {
  const name = document.getElementById('zone-name').value;
  const x = parseInt(document.getElementById('zone-x').value);
  const y = parseInt(document.getElementById('zone-y').value);
  const width = document.getElementById('zone-width').value ? parseInt(document.getElementById('zone-width').value) : null;
  const height = document.getElementById('zone-height').value ? parseInt(document.getElementById('zone-height').value) : null;

  if (!name || isNaN(x) || isNaN(y)) {
    alert('Nom, X et Y sont requis');
    return;
  }

  const result = await createZone(name, x, y, width, height);
  if (result.status === 'ok') {
    document.getElementById('zone-form').style.display = 'none';
    await renderZones();
  } else {
    alert(`Erreur: ${result.message}`);
  }
});

async function fetchTutorialStatus() {
  const apiUrl = document.getElementById('api-url').value;
  try {
    const response = await fetch(`${apiUrl}/tutorial/status`);
    const data = await response.json();
    return data;
  } catch (error) {
    return null;
  }
}

async function startTutorial() {
  const apiUrl = document.getElementById('api-url').value;
  try {
    const response = await fetch(`${apiUrl}/tutorial/start`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' }
    });
    return await response.json();
  } catch (error) {
    return { status: 'error', message: error.message };
  }
}

async function stopTutorial() {
  const apiUrl = document.getElementById('api-url').value;
  try {
    const response = await fetch(`${apiUrl}/tutorial/stop`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' }
    });
    return await response.json();
  } catch (error) {
    return { status: 'error', message: error.message };
  }
}

async function updateTutorialUI() {
  const tutorialStatus = await fetchTutorialStatus();
  const overlay = document.getElementById('tutorial-overlay');
  const btnPrefill = document.getElementById('btn-prefill-tutorial');

  if (!tutorialStatus || tutorialStatus.status === 'no_tutorial') {
    overlay.style.display = 'none';
    return;
  }

  const tutorial = tutorialStatus.tutorial;

  if (tutorial.active) {
    overlay.style.display = 'flex';
    document.getElementById('tutorial-title').textContent = tutorial.title;

    const currentStep = tutorial.steps[tutorial.current_index];
    const totalSteps = tutorial.steps.length;
    const progress = ((tutorial.current_index) / totalSteps) * 100;

    document.getElementById('tutorial-progress-fill').style.width = `${progress}%`;
    document.getElementById('tutorial-progress-text').textContent = `${tutorial.current_index} / ${totalSteps}`;

    if (currentStep) {
      document.getElementById('tutorial-message').textContent = currentStep.message;
      document.getElementById('tutorial-hint').textContent = currentStep.hint || '';
      document.getElementById('btn-start-tutorial').style.display = 'none';
      btnPrefill.style.display = 'block';
      btnPrefill.dataset.zone = currentStep.zone;
    } else {
      document.getElementById('tutorial-message').textContent = 'Tutoriel terminé ! Félicitations !';
      document.getElementById('tutorial-hint').textContent = '';
      document.getElementById('btn-start-tutorial').style.display = 'none';
      btnPrefill.style.display = 'none';
    }
  } else {
    overlay.style.display = 'flex';
    document.getElementById('tutorial-title').textContent = tutorial.title;
    document.getElementById('tutorial-message').textContent = tutorial.description;
    document.getElementById('tutorial-hint').textContent = '';
    document.getElementById('tutorial-progress-fill').style.width = '0%';
    document.getElementById('tutorial-progress-text').textContent = `0 / ${tutorial.steps.length}`;
    document.getElementById('btn-start-tutorial').style.display = 'block';
    btnPrefill.style.display = 'none';
  }
}

document.getElementById('btn-start-tutorial').addEventListener('click', async () => {
  await startTutorial();
  await updateTutorialUI();
});

document.getElementById('btn-close-tutorial').addEventListener('click', async () => {
  await stopTutorial();
  document.getElementById('tutorial-overlay').style.display = 'none';
});

document.getElementById('btn-prefill-tutorial').addEventListener('click', () => {
  const zoneName = document.getElementById('btn-prefill-tutorial').dataset.zone;

  document.getElementById('action-type').value = 'click_zone';
  document.getElementById('action-params').value = JSON.stringify({
    zone: zoneName,
    button: 'left'
  }, null, 2);

  document.querySelector('input[name="exec-mode"][value="direct"]').checked = true;
  updateModeIndicator();

  document.getElementById('action-type').scrollIntoView({ behavior: 'smooth', block: 'center' });
});

checkHealth();
updateWorkerStatus();
updateConfigStatus();
renderQueue();
renderHistory();
renderZones();
updateTutorialUI();

setInterval(checkHealth, 5000);
setInterval(updateWorkerStatus, 3000);
setInterval(renderQueue, 3000);
setInterval(updateTutorialUI, 1000);
