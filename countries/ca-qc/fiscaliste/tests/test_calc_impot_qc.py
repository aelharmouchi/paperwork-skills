"""Tests du calculateur. Les valeurs attendues ont été calculées à la main,
indépendamment du script (voir commentaires). Lancer : python -m unittest discover -s countries/ca-qc/fiscaliste/tests
"""
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "scripts"))

import calc_impot_qc as c  # noqa: E402

VALUES = c.load_values(HERE.parent / "data")


class TestBareme(unittest.TestCase):
    def test_revenu_zero(self):
        r = c.calcul_impot(0, VALUES)
        self.assertEqual(r["impot_total"], 0.0)

    def test_sous_credits_impot_nul(self):
        # 10 000 $ : impôt brut féd. 1 400 $ < crédit 2 303,28 $ ; QC 1 400 $ < 2 653 $
        r = c.calcul_impot(10000, VALUES)
        self.assertEqual(r["impot_total"], 0.0)

    def test_75000(self):
        # Fédéral : 58 523 x 14 % + 16 477 x 20,5 % = 11 571,005
        #   - 16 452 x 14 % = 9 267,725 ; x (1 - 0,165) = 7 738,55
        # Québec : 54 345 x 14 % + 20 655 x 19 % = 11 532,75 - 2 653 = 8 879,75
        r = c.calcul_impot(75000, VALUES)
        self.assertAlmostEqual(r["federal"]["impot_federal_net"], 7738.55, places=2)
        self.assertAlmostEqual(r["quebec"]["impot_quebec_net"], 8879.75, places=2)
        self.assertAlmostEqual(r["impot_total"], 16618.30, places=2)

    def test_bpa_reduction_progressive(self):
        mx = c.v(VALUES, "federal_bpa_max")
        mn = c.v(VALUES, "federal_bpa_min")
        debut = c.v(VALUES, "federal_bpa_phaseout_start")
        fin = c.v(VALUES, "federal_bpa_phaseout_end")
        self.assertEqual(c.montant_personnel_federal(debut, VALUES), mx)
        self.assertEqual(c.montant_personnel_federal(fin, VALUES), mn)
        milieu = c.montant_personnel_federal((debut + fin) / 2, VALUES)
        self.assertAlmostEqual(milieu, (mx + mn) / 2, places=6)

    def test_haut_revenu_tranche_superieure(self):
        r = c.calcul_impot(300000, VALUES)
        # le taux marginal combiné : 33 % x 0,835 + 25,75 % = 53,305 %
        self.assertAlmostEqual(r["taux_marginal_combine"], 0.33 * 0.835 + 0.2575, places=6)

    def test_marginal_dans_tranche(self):
        # À 54 345 $ pile, on est encore dans la tranche 14 % du Québec
        t = c.tranche_marginale(54345, c.v(VALUES, "quebec_brackets"))
        self.assertEqual(t, 0.14)
        t = c.tranche_marginale(54346, c.v(VALUES, "quebec_brackets"))
        self.assertEqual(t, 0.19)


class TestCotisations(unittest.TestCase):
    def test_80000(self):
        # RRQ : (74 600 - 3 500) x 6,30 % = 4 479,30 ; 2e supp. : (80 000 - 74 600) x 4 % = 216
        # RQAP : 80 000 x 0,43 % = 344,00 ; AE : plafonné à 895,70
        r = c.cotisations_salariales(80000, VALUES)
        self.assertEqual(r["rrq_base_et_premiere_supplementaire"], 4479.30)
        self.assertEqual(r["rrq_deuxieme_supplementaire"], 216.00)
        self.assertEqual(r["rqap"], 344.00)
        self.assertEqual(r["ae"], 895.70)
        self.assertEqual(r["total"], 5935.00)

    def test_salaire_sous_exemption(self):
        r = c.cotisations_salariales(3000, VALUES)
        self.assertEqual(r["rrq_base_et_premiere_supplementaire"], 0.0)

    def test_plafond_rrq_deuxieme(self):
        r = c.cotisations_salariales(200000, VALUES)
        self.assertEqual(r["rrq_deuxieme_supplementaire"], 416.00)
        self.assertEqual(r["rqap"], 442.90)


class TestGainsCapital(unittest.TestCase):
    def test_inclusion(self):
        self.assertEqual(c.gain_en_capital_imposable(10000, VALUES), 5000.0)


class TestDonnees(unittest.TestCase):
    def test_toutes_les_feuilles_ont_une_source(self):
        for k, leaf in VALUES.items():
            self.assertIn("source", leaf, k)
            self.assertIn(leaf["confidence"], {"official", "secondary", "unconfirmed"}, k)

    def test_celi_cumulatif_recoupe(self):
        # 5 000 x4 (2009-2012) + 5 500 x2 (2013-14) + 10 000 (2015) + 5 500 x3 (2016-18)
        # + 6 000 x4 (2019-22) + 6 500 (2023) + 7 000 x3 (2024-26)
        total = 5000*4 + 5500*2 + 10000 + 5500*3 + 6000*4 + 6500 + 7000*3
        self.assertEqual(total, 109000)
        self.assertEqual(c.v(VALUES, "celi_cumulative_since_2009"), total)


if __name__ == "__main__":
    unittest.main()
