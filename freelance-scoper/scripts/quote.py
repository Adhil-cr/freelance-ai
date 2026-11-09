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

    eff_rate = base_rate * exp_mult * tech["rate_mult"] * urg["rate_mult"]
    dev_cost = total * eff_rate * prof["client_mult"]
    margin = dev_cost * r["profit_margin"]
    fair = dev_cost + margin
    realised = fair / total if total else 0

    band = r["rate_band"]
    # the band moves with the freelancer's own rate (an expert charging Rs 900 base has a higher band)
    band_scale = exp_mult * (base_rate / r["base_hourly"])
    band_hi = band["high"] * band_scale * max(1.0, prof["client_mult"])
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

    adv_default = 50 if fair < 60000 else 40
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
                   "experience_multiplier": exp_mult, "min_hourly": floor_rate},
        "features": feats,
        "hours": {"foundation": round(foundation, 1), "features": feature_hours,
                  "tech_scaled": round(tech_scaled, 1), "extra_revision": extra_rev,
                  "buffer": round(buffer, 1), "buffer_rate": buffer_rate,
                  "meetings": round(meetings, 1), "total": round(total, 1),
                  "calendar_days": round(days, 1), "hours_per_day": urg["hours_per_day"]},
        "rate": {"effective_hourly": round(eff_rate), "client_mult": prof["client_mult"],
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
        "notes": {"profile_note": prof["note"], "confidence_note": conf["note"]},
    }


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
    for k in ("usage", "confidence", "tech", "urgency", "risk", "category", "tier"):
        if old["inputs"][k] != new["inputs"][k]:
            lines.append("{}: {} -> {}".format(k.capitalize(), old["inputs"][k], new["inputs"][k]))
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
    L.append("**Rate build-up:** Rs {} base x experience {} x tech {} x urgency {} x client type {} = **Rs {}/h**; realised after margin: Rs {}/h".format(
        i["base_rate"], i["experience_multiplier"], rt["tech_rate_mult"], rt["urgency_rate_mult"],
        rt["client_mult"], rt["effective_hourly"], rt["realised_hourly"]))
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
    ap.add_argument("spec")
    ap.add_argument("--mode", choices=["brief", "full", "expert"], default="full")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--budget", type=float, help="client budget before GST; drops low-priority scope to fit")
    ap.add_argument("--compare", help="path to a previous --json result; prints what changed")
    ap.add_argument("--rate", type=float)
    ap.add_argument("--exp", type=float)
    ap.add_argument("--min-rate", type=float)
    ap.add_argument("--data", default=str(DATA))
    a = ap.parse_args()

    spec = json.loads(Path(a.spec).read_text())
    data = json.loads(Path(a.data).read_text())
    kw = {"rate": a.rate, "exp": a.exp, "min_rate": a.min_rate}
    res = budget_fit(spec, data, a.budget, **kw) if a.budget else compute(spec, data, **kw)

    if a.json:
        print(json.dumps(res, indent=2))
        return
    if a.mode == "brief":
        print(md_brief(res))
    else:
        sens = sensitivity(spec, data, **kw) if a.mode == "expert" else None
        print(md_full(res, expert=(a.mode == "expert"), sens=sens))
    if a.compare:
        old = json.loads(Path(a.compare).read_text())
        print("\n**Changed since last run:**")
        for line in diff(old, res):
            print("- " + line)


if __name__ == "__main__":
    main()
