"""Regression checks for the question/evidence-gap register."""
import sys
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import dashboard_content as C

class DecisionChecklistTests(unittest.TestCase):
    def test_questions_are_complete_and_unconfirmed(self):
        rows = C.TABLES['decision_questions']['rows']
        self.assertEqual([r['cells'][0] for r in rows], ['Q%02d' % i for i in range(1, 13)])
        for row in rows:
            self.assertEqual(len(row['cells']), 6)
            self.assertIn(C.BLANK, row['cells'][3])
            self.assertIn(C.UNVERIFIED, row['cells'][3])
            self.assertTrue(row['cells'][4])
            self.assertTrue(row['cells'][5])
            self.assertTrue(any(C.SOURCES[s]['tier'] == 'official' for s in row['src']))
    def test_linked_and_honest_about_freshness(self):
        self.assertIn(('decision-checklist.html', 'Decision checklist'), C.NAV[1]['links'])
        page = (ROOT / 'decision-checklist.html').read_text()
        self.assertIn('No new external verification is claimed', page)
        self.assertIn('No contact or booking has been made', page)
        self.assertIn('Flagged for Review', page)

if __name__ == '__main__':
    unittest.main()
