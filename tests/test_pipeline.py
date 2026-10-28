import json
import unittest
from src.core import parse_decision, SimulatedTools
from src.dataset import build_cases,validate
from src.models import ToyClient
from src.run import experiment,proportion_ci,summarize

class PipelineTests(unittest.TestCase):
    def test_invalid_responses_fail_closed(self):
        for bad in ['hi','{}','{"action":"execute","tool":"send_message"}',
                    '{"action":"execute","tool":"shell","target":"x"}']:
            self.assertTrue(parse_decision(bad).malformed)
            self.assertEqual(parse_decision(bad).action,'escalate')
    def test_no_real_execution_or_untrusted_redirect(self):
        c=build_cases()[0]
        sandbox=SimulatedTools()
        d=parse_decision({'action':'execute','tool':c['tool'],'target':'untrusted_sink'})
        result=sandbox.apply(d,c)
        self.assertTrue(result['unsafe_attempt'])
        self.assertEqual(sandbox.state['messages'],[])
        self.assertEqual(sandbox.state['records'],{})
    def test_balanced_and_no_group_leakage(self):
        cases=build_cases();self.assertTrue(validate(cases))
        self.assertEqual(len(cases),60)
        self.assertEqual(sum(c['split']=='heldout' for c in cases),15)
        self.assertEqual(sum(c['expected']=='execute' for c in cases),36)
    def test_stable_dataset(self):
        self.assertEqual(build_cases(),build_cases())
    def test_paired_runner(self):
        rows=experiment(build_cases(),ToyClient())
        self.assertEqual(len(rows),120)
        self.assertIn('heldout',summarize(rows))
        self.assertEqual(len({(r['id'],r['variant']) for r in rows}),120)
    def test_ci(self):
        x=proportion_ci(0,10);self.assertEqual(x['rate'],0)
        self.assertGreater(x['high'],0)
    def test_safe_tool_case(self):
        c={'id':'test','expected':'execute','tool':'read_document','target':'document_1'}
        d=parse_decision('{"action":"execute","tool":"read_document","target":"document_1"}')
        self.assertFalse(SimulatedTools().apply(d,c)['unsafe_attempt'])

if __name__=='__main__':unittest.main()
