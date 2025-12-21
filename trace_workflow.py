import json
from datetime import datetime
from pathlib import Path

class WorkflowTracer:
    def __init__(self):
        self.sessions_file = Path('console-agents/donnees/sessions.json')
        self.trace = {
            'id': self._generate_id(),
            'date': datetime.now().isoformat(),
            'agents': ['robert', 'halu', 'promptparfait'],
            'etapes': [],
            'score': 0,
            'reussis': 0,
            'total': 0
        }

    def _generate_id(self):
        return datetime.now().strftime('%Y%m%d-%H%M')

    def log_etape(self, agent, type_etape, contenu, resultat=None):
        etape = {
            'timestamp': datetime.now().isoformat(),
            'agent': agent,
            'type': type_etape,
            'contenu': contenu,
            'resultat': resultat
        }
        self.trace['etapes'].append(etape)
        print(f"\n[{agent.upper()}] {type_etape}")
        print(f"Contenu: {contenu}")
        if resultat:
            print(f"Résultat: {resultat}")
        print("-" * 80)

    def calculer_score(self):
        validations = [e for e in self.trace['etapes'] if e['type'] == 'validation']
        if not validations:
            return 0

        reussis = sum(1 for v in validations if v['resultat'] and 'valid' in v['resultat'].lower())
        total = len(validations)

        self.trace['reussis'] = reussis
        self.trace['total'] = total
        self.trace['score'] = round((reussis / total * 100), 1) if total > 0 else 0

        return self.trace['score']

    def sauvegarder(self):
        try:
            with open(self.sessions_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except FileNotFoundError:
            data = {
                'sessions': [],
                'index': {'dates': {}, 'agents': {}, 'tags': {}, 'scores': {}},
                'stats': {'total_sessions': 0, 'score_moyen': 0}
            }

        session = {
            'id': self.trace['id'],
            'date': self.trace['date'],
            'score': self.trace['score'],
            'reussis': self.trace['reussis'],
            'total': self.trace['total'],
            'agents': self.trace['agents'],
            'trace_complete': self.trace['etapes']
        }

        data['sessions'].append(session)

        date_key = datetime.now().strftime('%Y-%m-%d')
        if date_key not in data['index']['dates']:
            data['index']['dates'][date_key] = []
        data['index']['dates'][date_key].append(self.trace['id'])

        for agent in self.trace['agents']:
            if agent not in data['index']['agents']:
                data['index']['agents'][agent] = []
            data['index']['agents'][agent].append(self.trace['id'])

        if self.trace['score'] >= 90:
            score_range = '90-100'
        elif self.trace['score'] >= 80:
            score_range = '80-89'
        elif self.trace['score'] >= 70:
            score_range = '70-79'
        elif self.trace['score'] >= 60:
            score_range = '60-69'
        else:
            score_range = '0-59'

        if score_range not in data['index']['scores']:
            data['index']['scores'][score_range] = []
        data['index']['scores'][score_range].append(self.trace['id'])

        data['stats']['total_sessions'] = len(data['sessions'])
        data['stats']['score_moyen'] = round(sum(s['score'] for s in data['sessions']) / len(data['sessions']), 1)

        with open(self.sessions_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        print(f"\n[OK] Session {self.trace['id']} sauvegardee")
        print(f"Score: {self.trace['score']}% ({self.trace['reussis']}/{self.trace['total']})")

    def afficher_trace_complete(self):
        print("\n" + "=" * 80)
        print(f"TRACE WORKFLOW COMPLÈTE - Session {self.trace['id']}")
        print("=" * 80)

        for i, etape in enumerate(self.trace['etapes'], 1):
            print(f"\nÉTAPE {i}: [{etape['agent'].upper()}] {etape['type']}")
            print(f"Timestamp: {etape['timestamp']}")
            print(f"Contenu: {etape['contenu']}")
            if etape['resultat']:
                print(f"Résultat: {etape['resultat']}")
            print("-" * 80)

        print(f"\nSCORE FINAL: {self.trace['score']}% ({self.trace['reussis']}/{self.trace['total']})")
        print("=" * 80)


def demo_workflow():
    tracer = WorkflowTracer()

    prompt_initial = "crée une fonction python qui additionne deux nombres"

    tracer.log_etape(
        agent='robert',
        type_etape='reception_prompt',
        contenu=prompt_initial,
        resultat='Workflow démarré'
    )

    tracer.log_etape(
        agent='halu',
        type_etape='validation',
        contenu=prompt_initial,
        resultat='STATUS: valid - Prompt simple, clair, sans ambiguïté'
    )

    prompt_optimise = "Créer fonction Python add(a, b) retournant a+b"

    tracer.log_etape(
        agent='promptparfait',
        type_etape='optimisation',
        contenu=prompt_initial,
        resultat=prompt_optimise
    )

    tracer.log_etape(
        agent='halu',
        type_etape='validation',
        contenu=prompt_optimise,
        resultat='STATUS: valid - Prompt optimisé cohérent, exécutable'
    )

    tracer.log_etape(
        agent='robert',
        type_etape='confirmation_user',
        contenu=f"Prompt optimisé: {prompt_optimise}",
        resultat='En attente'
    )

    tracer.calculer_score()

    tracer.afficher_trace_complete()

    tracer.sauvegarder()


if __name__ == '__main__':
    demo_workflow()
