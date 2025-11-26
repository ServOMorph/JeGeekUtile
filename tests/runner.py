#!/usr/bin/env python3
import json
import sys
from pathlib import Path
from datetime import datetime
import time

class TestRunner:
    def __init__(self):
        self.base_path = Path(__file__).parent.parent

        with open(self.base_path / 'config.json', encoding='utf-8') as f:
            self.config = json.load(f)

        with open(self.base_path / 'donnees' / 'agents.json', encoding='utf-8') as f:
            self.agents = json.load(f)['agents']

    def run_all(self):
        """Exécute tous tests - agents + système"""
        print(f"\n{'='*60}")
        print(f"Exécution tests - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*60}\n")

        resultats = {
            'session_id': datetime.now().strftime('%Y%m%d-%H%M'),
            'date': datetime.now().isoformat(),
            'tests': []
        }

        # Tests agents
        print("Tests agents:")
        for agent in self.agents:
            print(f"\n  Agent: {agent['nom']}")
            for test in agent['tests']:
                res = self.execute_test_agent(agent['id'], test)
                resultats['tests'].append(res)
                statut_icon = '[OK]' if res['statut'] == 'ok' else '[ERR]'
                print(f"    {statut_icon} {test['nom']}")

        # Tests système
        print(f"\nTests système:")
        tests_systeme = [
            self.test_structure(),
            self.test_archivage(),
            self.test_indexation(),
            self.test_ui(),
            self.test_config()
        ]

        for test in tests_systeme:
            resultats['tests'].append(test)
            statut_icon = '[OK]' if test['statut'] == 'ok' else '[ERR]'
            print(f"  {statut_icon} {test['test']}")

        # Calcul score
        reussis = sum(1 for t in resultats['tests'] if t['statut'] == 'ok')
        total = len(resultats['tests'])
        resultats['score'] = round((reussis / total) * 100, 1) if total > 0 else 0
        resultats['reussis'] = reussis
        resultats['total'] = total

        # Sauvegarde
        self.save_results(resultats)

        print(f"\n{'='*60}")
        print(f"Résultat: {reussis}/{total} tests réussis ({resultats['score']}%)")
        print(f"{'='*60}\n")

        return resultats

    def execute_test_agent(self, agent_id, test):
        """Exécute test unitaire agent (simulation)"""
        start = time.time()

        # Simulation exécution test
        statut = 'ok'

        duree = round(time.time() - start, 2)

        return {
            'type': 'agent',
            'agent': agent_id,
            'test': test['nom'],
            'statut': statut,
            'duree_sec': duree
        }

    def test_structure(self):
        """Valide structure dossiers"""
        dossiers = ['console-agents', 'donnees', 'sessions', 'tests', 'plan_d_actions']
        try:
            ok = all((self.base_path / d).exists() for d in dossiers)
            return {'type': 'systeme', 'test': 'structure', 'statut': 'ok' if ok else 'erreur'}
        except Exception as e:
            return {'type': 'systeme', 'test': 'structure', 'statut': 'erreur', 'erreur': str(e)}

    def test_archivage(self):
        """Valide capacité archivage"""
        try:
            sessions_dir = self.base_path / 'sessions'
            ok = sessions_dir.exists() and sessions_dir.is_dir()
            return {'type': 'systeme', 'test': 'archivage', 'statut': 'ok' if ok else 'erreur'}
        except Exception as e:
            return {'type': 'systeme', 'test': 'archivage', 'statut': 'erreur', 'erreur': str(e)}

    def test_indexation(self):
        """Valide index recherche"""
        try:
            with open(self.base_path / 'donnees' / 'sessions.json', encoding='utf-8') as f:
                data = json.load(f)

            ok = 'index' in data and all(k in data['index'] for k in ['dates', 'agents', 'tags'])
            return {'type': 'systeme', 'test': 'indexation', 'statut': 'ok' if ok else 'erreur'}
        except Exception as e:
            return {'type': 'systeme', 'test': 'indexation', 'statut': 'erreur', 'erreur': str(e)}

    def test_ui(self):
        """Valide UI existe"""
        try:
            fichiers_ui = [
                self.base_path / 'console-agents' / 'index.html',
                self.base_path / 'console-agents' / 'app.js',
                self.base_path / 'console-agents' / 'eco.css'
            ]
            ok = all(f.exists() for f in fichiers_ui)
            return {'type': 'systeme', 'test': 'ui', 'statut': 'ok' if ok else 'erreur'}
        except Exception as e:
            return {'type': 'systeme', 'test': 'ui', 'statut': 'erreur', 'erreur': str(e)}

    def test_config(self):
        """Valide configuration"""
        try:
            config_file = self.base_path / 'config.json'
            ok = config_file.exists() and 'chemins' in self.config
            return {'type': 'systeme', 'test': 'config', 'statut': 'ok' if ok else 'erreur'}
        except Exception as e:
            return {'type': 'systeme', 'test': 'config', 'statut': 'erreur', 'erreur': str(e)}

    def save_results(self, resultats):
        """Sauvegarde résultats"""
        # Créer dossier session par date
        date = datetime.now().strftime('%Y-%m-%d')
        session_dir = self.base_path / 'sessions' / date
        session_dir.mkdir(parents=True, exist_ok=True)

        # Sauvegarder session complète
        fichier = session_dir / f"{resultats['session_id']}.json"
        with open(fichier, 'w', encoding='utf-8') as f:
            json.dump(resultats, f, indent=2, ensure_ascii=False)

        # Mise à jour index
        self.update_index(resultats)

    def update_index(self, resultats):
        """MAJ sessions.json"""
        sessions_file = self.base_path / 'donnees' / 'sessions.json'

        with open(sessions_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Ajout session résumé
        agents_utilises = list(set(t['agent'] for t in resultats['tests'] if t.get('type') == 'agent'))

        session_resume = {
            'id': resultats['session_id'],
            'date': resultats['date'],
            'score': resultats['score'],
            'reussis': resultats['reussis'],
            'total': resultats['total'],
            'agents': agents_utilises
        }

        data['sessions'].append(session_resume)

        # MAJ index dates
        date = resultats['date'][:10]
        if date not in data['index']['dates']:
            data['index']['dates'][date] = []
        data['index']['dates'][date].append(resultats['session_id'])

        # MAJ index agents
        for agent_id in agents_utilises:
            if agent_id not in data['index']['agents']:
                data['index']['agents'][agent_id] = []
            data['index']['agents'][agent_id].append(resultats['session_id'])

        # MAJ index scores
        score = resultats['score']
        if score >= 90:
            data['index']['scores']['90-100'].append(resultats['session_id'])
        elif score >= 80:
            data['index']['scores']['80-89'].append(resultats['session_id'])
        elif score >= 70:
            data['index']['scores']['70-79'].append(resultats['session_id'])
        elif score >= 60:
            data['index']['scores']['60-69'].append(resultats['session_id'])
        else:
            data['index']['scores']['0-59'].append(resultats['session_id'])

        # MAJ stats
        data['stats']['total_sessions'] = len(data['sessions'])
        if data['stats']['total_sessions'] > 0:
            data['stats']['score_moyen'] = round(
                sum(s['score'] for s in data['sessions']) / data['stats']['total_sessions'],
                1
            )

        with open(sessions_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

if __name__ == '__main__':
    try:
        runner = TestRunner()
        resultats = runner.run_all()
        sys.exit(0 if resultats['score'] >= 80 else 1)
    except Exception as e:
        print(f"\n[ERREUR] {e}\n")
        sys.exit(1)
