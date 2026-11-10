"""Run with: python -m unittest discover -s tests -v   (no dependencies)"""
import copy
import json
import sys
import unittest
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent / "freelance-scoper"
sys.path.insert(0, str(SKILL / "scripts"))
import quote  # noqa: E402

DATA = json.loads((SKILL / "data" / "pricing.json").read_text())
DATA["_regions"] = json.loads((SKILL / "data" / "regions.json").read_text())["regions"]


def spec(name="fitness-personal"):
    return json.loads((SKILL / "examples" / (name + ".spec.json")).read_text())


class Pricing(unittest.TestCase):
    def test_examples_compute(self):
        for f in (SKILL / "examples").glob("*.spec.json"):
            res = quote.compute(json.loads(f.read_text()), DATA)
            self.assertGreater(res["price"]["fair_ex_gst"], 0, f.name)
            self.assertLess(res["price"]["floor_ex_gst"], res["price"]["fair_ex_gst"], f.name)

    def test_usage_orders_price(self):
        prices = []
        for u in ("Personal use (one user)", "Small business / local customers",
                  "Scalable startup product", "Company internal system (ERP/CRM)"):
            s = spec(); s["usage"] = u
            prices.append(quote.compute(s, DATA)["price"]["fair_ex_gst"])
        self.assertEqual(prices, sorted(prices))

    def test_defaults_do_not_change_price(self):
        a = quote.compute(spec(), DATA)["price"]["fair_ex_gst"]
        s = spec(); s.update(client_type="Small business", client_region="India")
        self.assertEqual(a, quote.compute(s, DATA)["price"]["fair_ex_gst"])

    def test_region_and_client_type_raise_price(self):
        base = quote.compute(spec(), DATA)["price"]["fair_ex_gst"]
        s = spec(); s["client_region"] = "UK"
        self.assertGreater(quote.compute(s, DATA)["price"]["fair_ex_gst"], base)
        s = spec(); s["client_type"] = "Agency (white-label)"
        self.assertLess(quote.compute(s, DATA)["price"]["fair_ex_gst"], base)

    def test_budget_fit_never_cuts_must(self):
        res = quote.budget_fit(spec("fitness-startup"), DATA, 1)
        for d in res["budget_fit"]["dropped"]:
            self.assertIn(d["priority"], ("should", "later"))
        self.assertFalse(res["budget_fit"]["fits"])

    def test_unknown_name_exits(self):
        s = spec(); s["tech"] = "Nonexistent"
        with self.assertRaises(SystemExit):
            quote.compute(s, DATA)


class Options(unittest.TestCase):
    def test_packages_are_ordered(self):
        res = quote.compute(spec("fitness-startup"), DATA)
        p = [x["price"] for x in quote.pricing_options(spec("fitness-startup"), DATA, res)["packages"]]
        self.assertEqual(p, sorted(p))
        self.assertEqual(p[-1], res["price"]["fair_ex_gst"])

    def test_milestones_sum_to_price(self):
        s = spec("fitness-startup"); res = quote.compute(s, DATA)
        total = sum(v for _, v in quote.pricing_options(s, DATA, res)["milestones"])
        self.assertAlmostEqual(total, res["price"]["fair_ex_gst"], delta=5)

    def test_value_option_only_with_value(self):
        s = spec(); res = quote.compute(s, DATA)
        self.assertNotIn("value", quote.pricing_options(s, DATA, res))
        s["client_value_yearly"] = 1000000
        self.assertIn("value", quote.pricing_options(s, DATA, quote.compute(s, DATA)))

    def test_proposal_renders(self):
        s = spec("fitness-uk-client"); s2 = quote._scoped(s, ("must", "should"))
        r = quote.compute(s2, DATA)
        text = quote.md_proposal(s, DATA, r, quote.pricing_options(s2, DATA, r),
                                 quote.pricing_options(s, DATA, quote.compute(s, DATA))["packages"])
        self.assertIn("GBP", text)
        self.assertIn("Payment schedule", text)


class Data(unittest.TestCase):
    def test_regions_complete(self):
        for name, r in DATA["_regions"].items():
            for k in ("currency", "symbol", "fx_inr", "rate_mult", "pack"):
                self.assertIn(k, r, name)
            self.assertTrue((SKILL / "references" / r["pack"]).exists(), r["pack"])

    def test_skill_files_referenced_exist(self):
        text = (SKILL / "SKILL.md").read_text()
        for line in text.splitlines():
            for tok in line.replace("`", " ").split():
                if tok.startswith(("references/", "templates/")) and tok.endswith(".md"):
                    self.assertTrue((SKILL / tok).exists(), tok)


if __name__ == "__main__":
    unittest.main()
