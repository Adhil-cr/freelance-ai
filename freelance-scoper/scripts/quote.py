#!/usr/bin/env python3
"""Deterministic quote calculator for the freelance-scoper skill.

The language model never invents prices or hours. It maps the brief onto names in
data/pricing.json, writes a small spec file, and runs this script.

Usage:
    python scripts/quote.py spec.json                       # full markdown
    python scripts/quote.py spec.json --mode brief          # 4-line summary
    python scripts/quote.py spec.json --mode expert         # phases, drivers, sensitivity
    python scripts/quote.py spec.json --budget 80000        # drop low-priority scope to fit a budget (before GST)
    python scripts/quote.py spec.json --json > state/v2.json
    python scripts/quote.py spec.json --compare state/v1.json   # what changed since the last run
    python scripts/quote.py spec.json --rate 900 --exp 1.1 --min-rate 600
    python scripts/quote.py spec.json --options             # six pricing models + lean/recommended/premium packages
    python scripts/quote.py spec.json --proposal            # client-ready proposal draft (markdown)
    python scripts/quote.py spec.json --save project-state  # save as v1, v2, ... and auto-compare with the last version
    python scripts/quote.py --history project-state/<project>   # list saved versions

Spec (JSON). Only category, usage and tech are required:
{
  "client": "optional", "project": "optional",
  "usage": "Personal use (one user)",     # see usage_profiles in pricing.json
  "confidence": "Draft",                   # Draft | Firm | Quote-ready
  "category": "Health / fitness / nutrition app",
  "tier": "Intermediate",                  # Beginner | Intermediate | Advanced
  "features": [                            # strings (priority "must") or objects
    "Login (email/password)",
    {"name": "Meal planner", "priority": "later"},
    {"name": "Progress charts & trends", "priority": "should", "hours": 10}   # hours = your own override
  ],
  "custom_features": [{"name": "Starter Kerala food list", "hours": 30, "priority": "must"}],
  "tech": "Django (Python)",
  "urgency": "Standard",
  "risk": "Medium",                        # adds buffer hours, not a price multiplier
  "extra_revision_rounds": 0,
  "hosting": "Free tier / hobby (personal use)",
  "extras": ["Domain (.com/.in, per year)"],
  "advance_pct": 40,
  "client_type": "Small business",         # Individual / personal client | Small business | Startup | Agency (white-label) | Enterprise / corporate
  "client_region": "India",                # India | UAE / Gulf | UK | EU | US / Canada | Australia / NZ | Southeast Asia | Other (international)
  "retainer_hours": 40,                    # optional, for --options
  "client_value_yearly": 0,                # optional, yearly Rs value to the client, for value-based pricing in --options
  "base_hourly": 700, "experience_multiplier": 1.0, "min_hourly": 500   # optional overrides
}
"""
import argparse
import copy
import json
import sys
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data" / "pricing.json"
TIER_KEY = {"Beginner": "b", "Intermediate": "i", "Advanced": "a"}
PRIORITY_ORDER = {"must": 0, "should": 1, "later": 2}


def inr(n):
    n = int(round(n))
    s = str(abs(n))
    if len(s) > 3:
        head, tail = s[:-3], s[-3:]
        groups = []
        while len(head) > 2:
            groups.insert(0, head[-2:])
            head = head[:-2]
        if head:
            groups.insert(0, head)
        s = ",".join(groups + [tail])
    return ("-" if n < 0 else "") + "Rs " + s


def lookup(table, key, label):
    if key not in table:
        sys.exit("Unknown {}: '{}'. Valid names: {}".format(label, key, "; ".join(sorted(table))))
    return table[key]


def norm_features(spec, data, tier):
    tk = TIER_KEY[tier]
    rows = []
    for item in spec.get("features", []):
        if isinstance(item, str):
            item = {"name": item}
        lib = lookup(data["features"], item["name"], "feature")
        rows.append({"name": item["name"], "hours": item.get("hours", lib[tk]),
                     "priority": item.get("priority", "must"), "custom": False,
                     "overridden": "hours" in item})
    for cf in spec.get("custom_features", []):
        rows.append({"name": cf["name"], "hours": cf["hours"],
                     "priority": cf.get("priority", "must"), "custom": True, "overridden": False})
    return rows


def compute(spec, data, rate=None, exp=None, min_rate=None):
    r = data["rates"]
    base_rate = rate if rate is not None else spec.get("base_hourly", r["base_hourly"])
    exp_mult = exp if exp is not None else spec.get("experience_multiplier", r["experience_multiplier"])
    floor_rate = min_rate if min_rate is not None else spec.get("min_hourly", r["min_hourly"])

    usage_name = spec.get("usage", "Not sure yet")
    prof = lookup(data["usage_profiles"], usage_name, "usage")
    cat = lookup(data["categories"], spec["category"], "category")
    tech = lookup(data["tech"], spec["tech"], "tech")
    urg = lookup(data["urgency"], spec.get("urgency", "Standard"), "urgency")
    risk = lookup(data["risk"], spec.get("risk", "Low"), "risk")
    ct_name = spec.get("client_type", "Small business")
    ct = lookup(data.get("client_types", {ct_name: {"rate_mult": 1.0, "min_advance_pct": 40, "note": ""}}), ct_name, "client_type")
    regions = data.get("_regions", {"India": {"currency": "INR", "symbol": "Rs", "fx_inr": 1, "rate_mult": 1.0, "pack": "regions/india-kerala.md", "cross_border": False}})
    region_name = spec.get("client_region", "India")
    region = lookup(regions, region_name, "client_region")
    conf_name = spec.get("confidence", "Draft")
    conf = lookup(data["confidence"], conf_name, "confidence")
    tier = spec.get("tier", "Intermediate")
    if tier not in TIER_KEY:
        sys.exit("tier must be Beginner, Intermediate or Advanced")

    feats = norm_features(spec, data, tier)
    feature_hours = sum(f["hours"] for f in feats)
    foundation = cat["base_hours"] * prof["base_scale"]
    raw = foundation + feature_hours
    tech_scaled = raw * tech["hours_mult"]
    extra_rev = spec.get("extra_revision_rounds", 0) * r["hours_per_extra_revision_round"]
    pre = tech_scaled + extra_rev
    buffer_rate = r["buffer"] + risk["extra_buffer"]
    buffer = pre * buffer_rate
    meetings = pre * r["meetings_share"]
    total = pre + buffer + meetings

    eff_rate = base_rate * exp_mult * tech["rate_mult"] * urg["rate_mult"] * ct["rate_mult"] * region["rate_mult"]
    dev_cost = total * eff_rate * prof["client_mult"]
    margin = dev_cost * r["profit_margin"]
    fair = dev_cost + margin
    realised = fair / total if total else 0

    band = r["rate_band"]
    # the band moves with the freelancer's own rate (an expert charging Rs 900 base has a higher band)
    band_scale = exp_mult * (base_rate / r["base_hourly"])
    band_hi = band["high"] * band_scale * max(1.0, prof["client_mult"] * ct["rate_mult"]) * region["rate_mult"]
    band_lo = band["low"] * band_scale
    if realised > band_hi * 1.05:
        band_status = "ABOVE your rate band"
    elif realised < band_lo:
        band_status = "BELOW your rate band (underpriced)"
    else:
        band_status = "within your rate band"

    band_cap_price = total * band_hi
    floor = min(total * floor_rate, fair * r["floor_vs_fair_max"])
    anchor = fair * (1 + prof["anchor_uplift"])
    gst = fair * r["gst"]
    low = fair * conf["low"]
    high = fair * conf["high"]

    days = total / urg["hours_per_day"]

    phases = [(n, round(pre * s, 1)) for n, s in data["phase_shares"].items()]
    drivers = sorted(feats, key=lambda f: -f["hours"])[:3]

    hosting_name = spec.get("hosting") or prof["default_hosting"]
    hosting = lookup(data["hosting_yearly"], hosting_name, "hosting")
    extras = [(e, lookup(data["other_recurring"], e, "extra")) for e in spec.get("extras", [])]

    adv_default = 50 if fair < 60000 else ct["min_advance_pct"]
    adv_pct = spec.get("advance_pct", adv_default)
    adv = fair * adv_pct / 100
    rest = fair - adv
    if fair < 60000:
        schedule = [("Advance (before any work)", adv), ("Final (on acceptance)", rest)]
    else:
        schedule = [("Advance (before design work)", adv), ("Midpoint (core features on staging)", rest / 2),
                    ("Final (on acceptance)", rest / 2)]

    return {
        "inputs": {"client": spec.get("client"), "project": spec.get("project"), "usage": usage_name,
                   "confidence": conf_name, "category": spec["category"], "tier": tier,
                   "tech": spec["tech"], "urgency": spec.get("urgency", "Standard"),
                   "risk": spec.get("risk", "Low"), "base_rate": base_rate,
                   "experience_multiplier": exp_mult, "min_hourly": floor_rate,
                   "client_type": ct_name, "client_region": region_name},
        "currency": {"code": region["currency"], "symbol": region["symbol"], "fx_inr": region["fx_inr"],
                     "cross_border": region.get("cross_border", False), "pack": region.get("pack")},
        "features": feats,
        "hours": {"foundation": round(foundation, 1), "features": feature_hours,
                  "tech_scaled": round(tech_scaled, 1), "extra_revision": extra_rev,
                  "buffer": round(buffer, 1), "buffer_rate": buffer_rate,
                  "meetings": round(meetings, 1), "total": round(total, 1),
                  "calendar_days": round(days, 1), "hours_per_day": urg["hours_per_day"]},
        "rate": {"effective_hourly": round(eff_rate), "client_mult": prof["client_mult"],
                 "client_type_mult": ct["rate_mult"], "region_mult": region["rate_mult"],
                 "tech_rate_mult": tech["rate_mult"], "urgency_rate_mult": urg["rate_mult"],
                 "realised_hourly": round(realised), "band_status": band_status,
                 "band": [round(band_lo), round(band_hi)],
                 "price_if_capped_at_band_top": round(band_cap_price)},
        "price": {"dev_cost": round(dev_cost), "margin": round(margin),
                  "fair_ex_gst": round(fair), "range_low": round(low), "range_high": round(high),
                  "gst_if_registered": round(gst), "anchor_ex_gst": round(anchor),
                  "floor_ex_gst": round(floor)},
        "phases": phases,
        "drivers": [{"name": d["name"], "hours": d["hours"]} for d in drivers],
        "payments": [[n, round(v)] for n, v in schedule],
        "recurring": {"hosting": [hosting_name, hosting], "extras": [[n, v] for n, v in extras],
                      "year1_total": hosting + sum(v for _, v in extras)},
        "notes": {"profile_note": prof["note"], "confidence_note": conf["note"], "client_type_note": ct["note"]},
    }


def money(n, res):
    """INR amount, with an approximate client-currency amount for cross-border clients."""
    c = res["currency"]
    if not c["cross_border"]:
        return inr(n)
    return "{}{:,} ({})".format(c["symbol"], int(round(n / c["fx_inr"])), inr(n))


def _scoped(spec, keep):
    s = copy.deepcopy(spec)
    s["features"] = [f for f in s.get("features", []) if (f.get("priority", "must") if isinstance(f, dict) else "must") in keep]
    s["custom_features"] = [f for f in s.get("custom_features", []) if f.get("priority", "must") in keep]
    return s


def pricing_options(spec, data, res, **kw):
    """Six ways to price the same project. All numbers are derived from the main result."""
    ms = data["model_settings"]
    p, h, rt = res["price"], res["hours"], res["rate"]
    fair = p["fair_ex_gst"]
    out = {}
    packs = []
    for label, keep in zip(ms["package_labels"], (("must",), ("must", "should"), ("must", "should", "later"))):
        r2 = compute(_scoped(spec, keep), data, **kw)
        packs.append({"label": label, "price": r2["price"]["fair_ex_gst"], "hours": r2["hours"]["total"]})
    out["packages"] = packs
    out["fixed"] = {"price": fair, "range": [p["range_low"], p["range_high"]]}
    out["hourly"] = {"rate": round(rt["realised_hourly"] / 10) * 10, "est_hours": h["total"],
                     "est_hours_range": [round(h["total"] * 0.9), round(h["total"] * 1.25)],
                     "weekly_cap_hours": h["hours_per_day"] * 5}
    phase_hours = dict(res["phases"])
    total_ph = sum(phase_hours.values()) or 1
    adv_pct = spec.get("advance_pct", 50 if fair < 60000 else 40)
    advance = fair * adv_pct / 100
    rest = fair - advance
    stones = [["Advance (before any work)", round(advance)]]
    for name, members in ms["milestones"]:
        share = sum(phase_hours.get(m, 0) for m in members) / total_ph
        stones.append([name, round(rest * share)])
    out["milestones"] = stones
    rh = spec.get("retainer_hours", ms["retainer_hours_default"])
    rrate = rt["realised_hourly"] * (1 - ms["retainer_discount"])
    out["retainer"] = {"hours_per_month": rh, "rate": round(rrate), "monthly": round(rh * rrate),
                       "min_months": ms["retainer_min_months"]}
    val = spec.get("client_value_yearly", 0)
    if val:
        lo, hi = val * ms["value_share_low"], val * ms["value_share_high"]
        out["value"] = {"yearly_value": val, "band": [round(lo), round(hi)], "suggested": round(min(max(fair, lo), hi)),
                        "below_cost": lo < fair}
    return out


def md_options(opt, res):
    m = lambda n: money(n, res)
    L = ["**Pricing options for this project** (same scope, different shape; before GST)", ""]
    L.append("| Model | When it fits | What to quote |")
    L.append("|---|---|---|")
    f, hr, rt = opt["fixed"], opt["hourly"], opt["retainer"]
    L.append("| Fixed price | Scope is clear and signed off | {} (range {} to {}) |".format(m(f["price"]), m(f["range"][0]), m(f["range"][1])))
    L.append("| Hourly (time and materials) | Scope is unclear or will keep changing | {}/h, about {} to {} h, weekly cap {} h |".format(
        m(hr["rate"]), hr["est_hours_range"][0], hr["est_hours_range"][1], hr["weekly_cap_hours"]))
    L.append("| Milestones | Mid-size project, cash-flow protection | " + "; ".join("{} {}".format(n, m(v)) for n, v in opt["milestones"]) + " |")
    L.append("| Retainer | Ongoing work after launch | {} h/month at {}/h = {}/month, minimum {} months |".format(
        rt["hours_per_month"], m(rt["rate"]), m(rt["monthly"]), rt["min_months"]))
    if "value" in opt:
        v = opt["value"]
        L.append("| Value-based | The product earns or saves the client money | {} to {} (10 to 20 percent of yearly value {}); suggested {}{} |".format(
            m(v["band"][0]), m(v["band"][1]), m(v["yearly_value"]), m(v["suggested"]),
            "; below your cost price, do not use" if v["below_cost"] and v["suggested"] < f["price"] else ""))
    L.append("")
    L.append("**Packages to offer the client (let them choose):**")
    L.append("")
    L.append("| Package | Price | Hours |")
    L.append("|---|---|---|")
    for pk in opt["packages"]:
        L.append("| {} | {} | {} |".format(pk["label"], m(pk["price"]), pk["hours"]))
    if len({pk["price"] for pk in opt["packages"]}) == 1:
        L.append("")
        L.append("All features are tagged must-have, so the packages are identical. Tag some features should or later to get real choices.")
    return "\n".join(L)


def md_proposal(spec, data, res, opt, packs):
    """Client-facing proposal draft. res/opt describe the first release (must + should); packs are the full package options."""
    i, p, h, rt, c = res["inputs"], res["price"], res["hours"], res["rate"], res["currency"]
    m = lambda n: money(n, res)
    title = i["project"] or "Project"
    must = [f["name"] for f in res["features"] if f["priority"] in ("must", "should")]
    should = []
    later = [f["name"] for f in norm_features(spec, data, spec.get("tier", "Intermediate")) if f["priority"] == "later"]
    L = ["# Proposal: {}".format(title), "",
         "Prepared for: {}  |  Prepared by: [Your name]  |  Date: [date]  |  Valid for 14 days".format(i["client"] or "[Client name]"), "",
         "## What I understood", "", "[2 to 3 lines in the client's words: the problem, who will use it, what success looks like.]", "",
         "## What is included (first version)", ""]
    L += ["- " + n for n in must] or ["- [list]"]
    if should:
        L += ["", "**Included if budget allows:**"] + ["- " + n for n in should]
    if later:
        L += ["", "**Planned for a later phase (not in this price):**"] + ["- " + n for n in later]
    outs = spec.get("out_of_scope", [])
    L += ["", "**Not included:**"] + (["- " + n for n in outs] if outs else ["- Anything not listed above. Extra requests are quoted separately before work starts."])
    L += ["", "## Timeline", "",
          "About {} working days of effort, roughly {} weeks including your feedback time. The start date depends on the advance payment.".format(
              round(h["calendar_days"]), max(1, round(h["calendar_days"] / 5 + 1))), "",
          "## Investment (before tax)", ""]
    if i["confidence"] == "Quote-ready":
        L.append("**Total: {}**".format(m(p["fair_ex_gst"])))
    else:
        L.append("**Estimated: {} to {}** (final price confirmed after the scope sheet is approved)".format(m(p["range_low"]), m(p["range_high"])))
    if spec.get("gst_registered"):
        L.append("")
        L.append("GST at 18 percent is added on top: {}.".format(inr(p["gst_if_registered"])))
    elif c["cross_border"]:
        L.append("")
        L.append("Export of services to a client outside India: no Indian GST is charged on the invoice (subject to the freelancer's registration status).")
    L += ["", "**Payment schedule:**", ""]
    for n, v in opt["milestones"]:
        L.append("- {}: {}".format(n, m(v)))
    pk = packs
    if len({x["price"] for x in pk}) > 1:
        L += ["", "**Scope options you can choose between:**", ""] + ["- {}: {}".format(x["label"], m(x["price"])) for x in pk]
    rc = res["recurring"]
    L += ["", "## Running costs (paid by you directly, in your name)", "",
          "- {}: about {} per year".format(rc["hosting"][0], inr(rc["hosting"][1]))] + ["- {}: about {} per year".format(n, inr(v)) for n, v in rc["extras"]]
    L += ["", "## How we will work", "",
          "1. You approve the scope sheet and pay the advance; I start design.",
          "2. I show the design prototype; you reply \"approved\" in writing before I build.",
          "3. Weekly short updates; I send a working version on staging at the midpoint.",
          "4. You test against the agreed criteria; final payment before handover of code and accounts.",
          "", "Included: 2 rounds of design changes and a free-fix period of 30 days after acceptance. Changes outside the scope are quoted before I start.",
          "", "## Next step", "", "Reply \"approved\" to this proposal and I will send the scope sheet and the first invoice.", "",
          "_Draft generated by freelance-scoper. Review every number and line before sending._"]
    return "\n".join(L)


def _slug(spec, fallback):
    name = spec.get("project") or spec.get("client") or fallback
    out = "".join(ch.lower() if ch.isalnum() else "-" for ch in name).strip("-")
    return "-".join(p for p in out.split("-") if p) or "project"


def save_state(spec, res, root, fallback="project"):
    """Save spec and result as the next version. Returns (folder, version, previous_result_or_None)."""
    folder = Path(root) / _slug(spec, fallback)
    folder.mkdir(parents=True, exist_ok=True)
    versions = sorted(int(p.stem.split("-v")[1]) for p in folder.glob("result-v*.json"))
    prev = json.loads((folder / "result-v{}.json".format(versions[-1])).read_text()) if versions else None
    n = (versions[-1] + 1) if versions else 1
    (folder / "spec-v{}.json".format(n)).write_text(json.dumps(spec, indent=2))
    (folder / "result-v{}.json".format(n)).write_text(json.dumps(res, indent=2))
    return folder, n, prev


def md_history(folder):
    rows = ["| Version | Confidence | Fair price | Hours | Features | Client type / country |", "|---|---|---|---|---|---|"]
    for p in sorted(Path(folder).glob("result-v*.json"), key=lambda x: int(x.stem.split("-v")[1])):
        r = json.loads(p.read_text())
        i = r["inputs"]
        rows.append("| v{} | {} | {} | {} | {} | {} / {} |".format(
            p.stem.split("-v")[1], i["confidence"], inr(r["price"]["fair_ex_gst"]), r["hours"]["total"],
            len(r["features"]), i.get("client_type", "-"), i.get("client_region", "-")))
    return "\n".join(rows) if len(rows) > 2 else "No saved versions in {}".format(folder)


def budget_fit(spec, data, budget, **kw):
    """Drop 'later' then 'should' features (largest hours first) until fair price <= budget."""
    work = copy.deepcopy(spec)
    res = compute(work, data, **kw)
    dropped = []
    tier = work.get("tier", "Intermediate")
    while res["price"]["fair_ex_gst"] > budget:
        feats = norm_features(work, data, tier)
        cands = [f for f in feats if f["priority"] in ("later", "should")]
        if not cands:
            break
        cands.sort(key=lambda f: (-PRIORITY_ORDER[f["priority"]], -f["hours"]))
        victim = cands[0]
        dropped.append({"name": victim["name"], "priority": victim["priority"], "hours": victim["hours"]})
        work["features"] = [x for x in work.get("features", [])
                            if (x if isinstance(x, str) else x["name"]) != victim["name"]]
        work["custom_features"] = [x for x in work.get("custom_features", []) if x["name"] != victim["name"]]
        res = compute(work, data, **kw)
    res["budget_fit"] = {"budget": budget, "fits": res["price"]["fair_ex_gst"] <= budget,
                         "dropped": dropped, "gap": max(0, res["price"]["fair_ex_gst"] - budget)}
    return res


def diff(old, new):
    lines = []
    oh, nh = old["hours"]["total"], new["hours"]["total"]
    if oh != nh:
        lines.append("Hours: {} -> {} ({:+.1f})".format(oh, nh, nh - oh))
    op, np_ = old["price"]["fair_ex_gst"], new["price"]["fair_ex_gst"]
    if op != np_:
        lines.append("Fair price: {} -> {} ({}{})".format(inr(op), inr(np_), "+" if np_ >= op else "-", inr(abs(np_ - op))[3:]))
    ol, nl = old["price"]["floor_ex_gst"], new["price"]["floor_ex_gst"]
    if ol != nl:
        lines.append("Walk-away floor: {} -> {}".format(inr(ol), inr(nl)))
    orr, nr = old["rate"]["realised_hourly"], new["rate"]["realised_hourly"]
    if orr != nr:
        lines.append("Realised hourly rate: Rs {} -> Rs {}".format(orr, nr))
    of = {f["name"] for f in old["features"]}
    nf = {f["name"] for f in new["features"]}
    if nf - of:
        lines.append("Added: " + "; ".join(sorted(nf - of)))
    if of - nf:
        lines.append("Removed: " + "; ".join(sorted(of - nf)))
    for k in ("usage", "confidence", "tech", "urgency", "risk", "category", "tier", "client_type", "client_region"):
        if old["inputs"].get(k) != new["inputs"].get(k):
            lines.append("{}: {} -> {}".format(k.replace("_", " ").capitalize(), old["inputs"].get(k), new["inputs"].get(k)))
    return lines or ["No change in scope or price."]


def md_brief(res):
    i, p, h, rt = res["inputs"], res["price"], res["hours"], res["rate"]
    out = []
    title = " - ".join(x for x in [i["client"], i["project"]] if x) or "Quote"
    out.append("**{}** | {} | confidence: {}".format(title, i["usage"], i["confidence"]))
    if i["confidence"] == "Quote-ready":
        out.append("**Price:** {} before GST (range {} to {})".format(inr(p["fair_ex_gst"]), inr(p["range_low"]), inr(p["range_high"])))
    else:
        out.append("**Price range:** {} to {} before GST (midpoint {}). Do not send a single number yet.".format(
            inr(p["range_low"]), inr(p["range_high"]), inr(p["fair_ex_gst"])))
    out.append("**Hours:** {} (~{} working days at {} h/day) | **Realised rate:** Rs {}/h, {}".format(
        h["total"], h["calendar_days"], h["hours_per_day"], rt["realised_hourly"], rt["band_status"]))
    out.append("**Anchor:** {} | **Walk-away floor:** {}".format(inr(p["anchor_ex_gst"]), inr(p["floor_ex_gst"])))
    if res["currency"]["cross_border"]:
        out.append("**In client currency:** about {} (fair price; approximate rate, check before quoting)".format(money(p["fair_ex_gst"], res)))
    return "\n".join(out)


def md_full(res, expert=False, sens=None):
    i, p, h, rt = res["inputs"], res["price"], res["hours"], res["rate"]
    L = [md_brief(res), ""]
    L.append("| Feature | Priority | Hours |")
    L.append("|---|---|---|")
    L.append("| Foundation (setup, design system, deploy pipeline) | must | {} |".format(h["foundation"]))
    for f in res["features"]:
        tag = " (custom)" if f["custom"] else (" (your override)" if f["overridden"] else "")
        L.append("| {}{} | {} | {} |".format(f["name"], tag, f["priority"], f["hours"]))
    L.append("")
    L.append("**Hours build-up:** foundation {} + features {} = {}; x tech hours {} = {}; + buffer {} ({}%) + meetings {} = **{} h**".format(
        h["foundation"], h["features"], round(h["foundation"] + h["features"], 1),
        round(h["tech_scaled"] / (h["foundation"] + h["features"]), 2) if (h["foundation"] + h["features"]) else 1,
        h["tech_scaled"], h["buffer"], int(round(h["buffer_rate"] * 100)), h["meetings"], h["total"]))
    L.append("")
    L.append("**Rate build-up:** Rs {} base x experience {} x tech {} x urgency {} x usage {} x client type {} x region {} = **Rs {}/h**; realised after margin: Rs {}/h".format(
        i["base_rate"], i["experience_multiplier"], rt["tech_rate_mult"], rt["urgency_rate_mult"],
        rt["client_mult"], rt["client_type_mult"], rt["region_mult"], rt["effective_hourly"], rt["realised_hourly"]))
    if rt["band_status"].startswith("ABOVE"):
        L.append("")
        L.append("**Rate check:** realised Rs {}/h is above your band (Rs {} to {}). Either justify it with a specific skill the client needs, or cap the price at about {} (band top) and trim scope to match.".format(
            rt["realised_hourly"], rt["band"][0], rt["band"][1], inr(rt["price_if_capped_at_band_top"])))
    L.append("")
    L.append("| | Amount |")
    L.append("|---|---|")
    L.append("| Development cost | {} |".format(inr(p["dev_cost"])))
    L.append("| + Margin | {} |".format(inr(p["margin"])))
    L.append("| **Fair price (before GST)** | **{}** |".format(inr(p["fair_ex_gst"])))
    L.append("| GST, only if you are registered | {} |".format(inr(p["gst_if_registered"])))
    L.append("| Opening anchor | {} |".format(inr(p["anchor_ex_gst"])))
    L.append("| Walk-away floor (hours x your minimum rate) | {} |".format(inr(p["floor_ex_gst"])))
    L.append("")
    L.append("**Payment schedule (before GST):** " + " | ".join("{} {}".format(n, inr(v)) for n, v in res["payments"]))
    rc = res["recurring"]
    L.append("")
    L.append("**Client's recurring costs (paid separately):** {} {}/yr".format(rc["hosting"][0], inr(rc["hosting"][1])) +
             "".join("; {} {}".format(n, inr(v)) for n, v in rc["extras"]) + "; year-1 total {}".format(inr(rc["year1_total"])))
    if "budget_fit" in res:
        b = res["budget_fit"]
        L.append("")
        L.append("**Budget fit ({}):** {}".format(inr(b["budget"]), "fits" if b["fits"] else "still {} over after cutting everything non-essential".format(inr(b["gap"]))))
        if b["dropped"]:
            L.append("Cut to fit: " + "; ".join("{} ({}, {} h)".format(d["name"], d["priority"], d["hours"]) for d in b["dropped"]))
        if not b["fits"]:
            L.append("Options: phase the project, simplify the stack, use a lighter tier for non-core features, or say plainly that this budget buys less than the client expects.")
    if expert:
        L.append("")
        L.append("**Phase split of work hours (before buffer and meetings):**")
        L.append("")
        L.append("| Phase | Hours |")
        L.append("|---|---|")
        for n, v in res["phases"]:
            L.append("| {} | {} |".format(n, v))
        L.append("")
        L.append("**Top cost drivers:** " + "; ".join("{} ({} h)".format(d["name"], d["hours"]) for d in res["drivers"]))
        if sens:
            L.append("")
            L.append("**Sensitivity (fair price before GST):** " + " | ".join("{}: {}".format(k, inr(v)) for k, v in sens))
        L.append("")
        L.append("Formula: total_h = (foundation + features) x tech_h + extra revisions, then x (1 + buffer + risk buffer + meetings). Price = total_h x base x exp x tech_rate x urgency x client_mult x (1 + margin).")
    return "\n".join(L)


def sensitivity(spec, data, **kw):
    out = []
    base = compute(spec, data, **kw)["price"]["fair_ex_gst"]
    for t in ("Beginner", "Intermediate", "Advanced"):
        s = copy.deepcopy(spec)
        s["tier"] = t
        out.append(("tier " + t, compute(s, data, **kw)["price"]["fair_ex_gst"]))
    out.append(("hours -20%", base * 0.8))
    out.append(("hours +20%", base * 1.2))
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("spec", nargs="?")
    ap.add_argument("--mode", choices=["brief", "full", "expert"], default="full")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--budget", type=float, help="client budget before GST; drops low-priority scope to fit")
    ap.add_argument("--compare", help="path to a previous --json result; prints what changed")
    ap.add_argument("--rate", type=float)
    ap.add_argument("--exp", type=float)
    ap.add_argument("--min-rate", type=float)
    ap.add_argument("--data", default=str(DATA))
    ap.add_argument("--save", metavar="DIR", help="save spec and result as the next version under DIR/<project>; prints what changed since the last version")
    ap.add_argument("--history", metavar="FOLDER", help="list saved versions in FOLDER (a DIR/<project> folder) and exit")
    ap.add_argument("--options", action="store_true", help="show six pricing models and lean/recommended/premium packages")
    ap.add_argument("--proposal", action="store_true", help="print a client-ready proposal draft (markdown)")
    a = ap.parse_args()

    if a.history:
        print(md_history(a.history))
        return
    if not a.spec:
        ap.error("spec is required unless --history is used")
    spec = json.loads(Path(a.spec).read_text())
    data = json.loads(Path(a.data).read_text())
    reg_path = Path(a.data).with_name("regions.json")
    if reg_path.exists():
        data["_regions"] = json.loads(reg_path.read_text())["regions"]
    kw = {"rate": a.rate, "exp": a.exp, "min_rate": a.min_rate}
    res = budget_fit(spec, data, a.budget, **kw) if a.budget else compute(spec, data, **kw)

    opt = pricing_options(spec, data, res, **kw) if (a.options or a.proposal or a.json) else None
    if a.proposal:
        spec1 = _scoped(spec, ("must", "should"))
        res1 = compute(spec1, data, **kw)
        print(md_proposal(spec, data, res1, pricing_options(spec1, data, res1, **kw), opt["packages"]))
        return
    if a.json:
        res["options"] = opt
        print(json.dumps(res, indent=2))
        return
    if a.mode == "brief":
        print(md_brief(res))
    else:
        sens = sensitivity(spec, data, **kw) if a.mode == "expert" else None
        print(md_full(res, expert=(a.mode == "expert"), sens=sens))
    if a.options:
        print("\n" + md_options(opt, res))
    if a.save:
        folder, n, prev = save_state(spec, res, a.save, Path(a.spec).stem.replace(".spec", ""))
        print("\nSaved as v{} in {}".format(n, folder))
        if prev is not None and not a.compare:
            print("\n**Changed since v{}:**".format(n - 1))
            for line in diff(prev, res):
                print("- " + line)
    if a.compare:
        old = json.loads(Path(a.compare).read_text())
        print("\n**Changed since last run:**")
        for line in diff(old, res):
            print("- " + line)


if __name__ == "__main__":
    main()
