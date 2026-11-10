"""Regression checks for the dated, non-destructive verification supplement."""
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import dashboard_content as C


class DeliveryChecks(unittest.TestCase):
    def test_selected_reads_have_official_links_and_blank_price(self):
        rows = C.TABLES['delivery_checks']['rows']
        self.assertEqual(len(rows), 6)
        for row in rows:
            self.assertIn(C.BLANK, row['cells'][3])
            self.assertIn(C.UNVERIFIED, row['cells'][3])
            for sid in row['src']:
                self.assertEqual(C.SOURCES[sid]['checked'], '2026-11-10')
                self.assertTrue(C.SOURCES[sid]['url'].startswith('https://'))

    def test_historical_model_read_dates_preserved(self):
        for sid in ('S11', 'S64', 'S10'):
            self.assertEqual(C.SOURCES[sid]['checked'], '2026-11-08')

    def test_page_is_navigable_and_does_not_claim_booking(self):
        self.assertIn(('delivery.html', 'Latest verification'), C.NAV[-1]['links'])
        text = (ROOT / 'delivery.html').read_text()
        self.assertIn('No provider is confirmed for this job', text)
        self.assertIn('11/9/2026 4:51:45 PM', text)
        d = json.loads((ROOT / 'data/canonical/delivery-2026-11-10.json').read_text())
        self.assertFalse(d['provider_contacted'])
        self.assertFalse(d['booking_confirmed'])
        self.assertIsNone(d['job_specific_verified_price'])
