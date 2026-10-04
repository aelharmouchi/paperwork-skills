"""Tests du calculateur IR Maroc. Valeurs attendues calculées à la main.
Lancer : python -m unittest discover -s countries/ma/fiscaliste/tests
"""
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "scripts"))

import calc_ir_ma as c  # noqa: E402

VALUES = c.load_values(HERE.parent / "data")
BR = c.v(VALUES, "ir_brackets")


class TestBareme(unittest.TestCase):
    def test_exoneration(self):
        self.assertEqual(c.calcul_ir(40000, 0, VALUES)["ir_net"], 0.0)
        self.assertEqual(c.calcul_ir(0, 0, VALUES)["ir_net"], 0.0)

    def test_continuite_aux_bornes(self):
        # Le barème « taux x revenu - somme à déduire » doit coïncider avec le calcul
        # tranche par tranche à chaque borne et au milieu de chaque tranche.
        bornes = [40000, 60000, 80000, 100000, 180000]
        points = bornes + [50000, 70000, 90000, 140000, 250000, 1_000_000]
        for r in points:
            self.assertAlmostEqual(c.ir_par_tranches(r, BR), c.ir_par_somme_a_deduire(r, BR), places=6, msg=r)

    def test_valeurs_main(self):
        # 100 000 : 20 000 x 10 % + 20 000 x 20 % + 20 000 x 30 % = 2 000 + 4 000 + 6 000 = 12 000
        self.assertAlmostEqual(c.calcul_ir(100000, 0, VALUES)["ir_brut"], 12000.0, places=2)
        # 120 000 : 12 000 + 20 000 x 34 % = 18 800  (méthode : 34 % x 120 000 - 22 000 = 18 800)
        self.assertAlmostEqual(c.calcul_ir(120000, 0, VALUES)["ir_brut"], 18800.0, places=2)
        # 200 000 : 39 200 + 20 000 x 37 % = 46 600  (37 % x 200 000 - 27 400 = 46 600)
        self.assertAlmostEqual(c.calcul_ir(200000, 0, VALUES)["ir_brut"], 46600.0, places=2)

    def test_charges_famille(self):
        # 120 000, 2 personnes : 18 800 - 1 200 = 17 600
        r = c.calcul_ir(120000, 2, VALUES)
        self.assertEqual(r["reduction_charges_famille"], 1200)
        self.assertAlmostEqual(r["ir_net"], 17600.0, places=2)

    def test_charges_famille_plafonnees(self):
        self.assertEqual(c.reduction_charges_famille(10, VALUES), 3600)
        self.assertEqual(c.reduction_charges_famille(6, VALUES), 3600)
        self.assertEqual(c.reduction_charges_famille(0, VALUES), 0)

    def test_ir_jamais_negatif(self):
        # 45 000 : 10 % x 5 000 = 500 ; réduction 3 600 => 0, pas négatif
        r = c.calcul_ir(45000, 6, VALUES)
        self.assertEqual(r["ir_net"], 0.0)

    def test_taux_marginal(self):
        self.assertEqual(c.calcul_ir(40001, 0, VALUES)["taux_marginal"], 0.10)
        self.assertEqual(c.calcul_ir(300000, 0, VALUES)["taux_marginal"], 0.37)


class TestDonnees(unittest.TestCase):
    def test_confiance_frais_pro_non_officielle(self):
        for k in ("frais_pro_rate_low", "frais_pro_rate_high", "frais_pro_cap", "frais_pro_threshold"):
            self.assertEqual(VALUES[k]["confidence"], "unconfirmed")

    def test_frais_pro_estimation(self):
        # 60 000 x 35 % = 21 000 ; 200 000 x 25 % = 50 000 -> plafonné à 35 000
        self.assertAlmostEqual(c.frais_professionnels(60000, VALUES), 21000.0)
        self.assertAlmostEqual(c.frais_professionnels(200000, VALUES), 35000.0)


if __name__ == "__main__":
    unittest.main()
