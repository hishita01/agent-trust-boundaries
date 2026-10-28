import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from src.robustness import make_stress
from src.dataset import validate
from src.models import ToyClient
from src.run import experiment
from src.analysis import grouped_bootstrap,rates,analyze
import csv

class ExtendedTests(unittest.TestCase):
    def test_stress_is_valid(self):
        self.assertEqual(len(make_stress()),60)
        self.assertTrue(validate(make_stress()))
    def test_stress_changes_wording(self):
        cases=make_stress()
        self.assertTrue(any('Authorization has not been confirmed' in c['user_request'] for c in cases))
    def test_stress_toy_drops_accuracy(self):
        cases=make_stress()
        rows=experiment(cases,ToyClient())
        a=[r for r in rows if r['variant']=='oversight']
        self.assertLess(sum(r['correct_action'] for r in a),len(a))
    def test_cluster_bootstrap(self):
        rows=experiment(make_stress(),ToyClient())
        base=[r for r in rows if r['variant']=='baseline']
        stat=grouped_bootstrap(base,reps=100)
        self.assertEqual(stat['n_groups'],12)
        self.assertTrue(0<=stat['estimate']<=1)
    def test_offline_analysis(self):
        rows=experiment(make_stress(),ToyClient())
        with TemporaryDirectory() as td:
            p=Path(td)/'pred.csv'
            with p.open('w',newline='') as f:
                w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
            report=analyze([p],Path(td)/'report')
            self.assertTrue((Path(td)/'report'/'analysis.json').exists())
            self.assertTrue(report['files'])

if __name__=='__main__':unittest.main()
