"""
NLGeo benchmark runner.

Reads eval/benchmark.jsonl, submits each query to the running NLGeo API
(http://localhost:8000), polls until completion, scores the result against
the expected values, and writes:

  - eval/results_<timestamp>.csv   (raw per-query rows)
  - eval/RESULTS.md                (summary table, overwritten each run)

Usage (from E:/GOAI/PHASE2):
    python eval/run_benchmark.py                 # run all queries once
    python eval/run_benchmark.py --only mumbai   # run only ids containing "mumbai"
    python eval/run_benchmark.py --repeat 3      # run each query 3 times (for variance later)

Requires: pip install requests
"""

import argparse
import csv
import json
import statistics
import sys
import time
from datetime import datetime
from pathlib import Path

import requests

API = "http://localhost:8000"
EVAL_DIR = Path(__file__).parent
BENCHMARK = EVAL_DIR / "benchmark.jsonl"
POLL_INTERVAL_S = 3
TIMEOUT_S = 900  # worst observed live-fetch (Berlin pharmacies) was 625s


def load_benchmark():
    items = []
    with open(BENCHMARK, encoding="utf-8") as f:
        for line_no, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                items.append(json.loads(line))
            except json.JSONDecodeError as e:
                print(f"[WARN] benchmark.jsonl line {line_no} is not valid JSON: {e}")
    return items


def submit(item):
    body = {"task": item["query"], "city": item["city"]}
    if item.get("hint"):
        body["domain_hint"] = item["hint"]
    r = requests.post(f"{API}/query", json=body, timeout=30)
    r.raise_for_status()
    data = r.json()
    # API may return task_id under different keys; handle both
    return data.get("task_id") or data.get("id")


def poll(task_id):
    start = time.time()
    while time.time() - start < TIMEOUT_S:
        r = requests.get(f"{API}/query/{task_id}", timeout=30)
        r.raise_for_status()
        data = r.json()
        status = data.get("status")
        if status in ("complete", "failed"):
            return data, time.time() - start
        time.sleep(POLL_INTERVAL_S)
    return {"status": "timeout"}, time.time() - start


def parse_result(response):
    """API returns result as a JSON string — parse it."""
    res = response.get("result") or {}
    if isinstance(res, str):
        try:
            res = json.loads(res)
        except (json.JSONDecodeError, TypeError):
            res = {}
    return res if isinstance(res, dict) else {}


TOP_LINE = __import__("re").compile(r"#\d+\s+(.+?):\s")


def extract_top_names(result_dict, k=3):
    """Ranked names live in the output text as lines like '#1 Kurla: 41.0%'."""
    output = result_dict.get("output", "") or ""
    names = [m.group(1).strip() for m in TOP_LINE.finditer(output)]
    return names[:k]


def name_match(expected, actual):
    """Lenient match: case-insensitive substring either direction."""
    if expected is None or actual is None:
        return None
    e, a = expected.lower().strip(), actual.lower().strip()
    return e in a or a in e


def score_item(item, response):
    """Return a dict of per-query scores."""
    out = {
        "status": response.get("status", "unknown"),
        "eval_score": None,
        "gt_correlation": None,
        "top1_actual": None,
        "top1_correct": None,
        "top3_hit": None,
    }
    if out["status"] != "complete":
        return out

    res = parse_result(response)
    out["eval_score"] = res.get("eval_score")
    out["gt_correlation"] = res.get("ground_truth_correlation")

    tops = extract_top_names(res, k=3)
    if tops:
        out["top1_actual"] = tops[0]
        if item.get("expected_top1"):
            out["top1_correct"] = name_match(item["expected_top1"], tops[0])
        if item.get("expected_top3"):
            hits = sum(
                1 for exp in item["expected_top3"]
                if any(name_match(exp, t) for t in tops)
            )
            out["top3_hit"] = hits / max(len(item["expected_top3"]), 1)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default=None,
                    help="only run benchmark ids containing this substring")
    ap.add_argument("--repeat", type=int, default=1,
                    help="run each query N times")
    args = ap.parse_args()

    items = load_benchmark()
    if args.only:
        items = [i for i in items if args.only.lower() in i["id"].lower()]
    if not items:
        print("No benchmark items matched.")
        sys.exit(1)

    # sanity: API up?
    try:
        requests.get(f"{API}/health", timeout=10)
    except requests.RequestException:
        print(f"ERROR: cannot reach {API}. Is docker compose up?")
        sys.exit(1)

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_path = EVAL_DIR / f"results_{stamp}.csv"
    rows = []

    total = len(items) * args.repeat
    n = 0
    for item in items:
        for rep in range(1, args.repeat + 1):
            n += 1
            label = f"[{n}/{total}] {item['id']}" + (
                f" (rep {rep})" if args.repeat > 1 else "")
            print(f"{label}: submitting…", flush=True)
            t0 = time.time()
            try:
                task_id = submit(item)
                response, wait_s = poll(task_id)
            except requests.RequestException as e:
                print(f"{label}: REQUEST ERROR {e}")
                rows.append({**item_row(item, rep),
                             "status": "request_error",
                             "latency_s": round(time.time() - t0, 2)})
                continue

            scores = score_item(item, response)
            latency = round(wait_s, 2)
            rows.append({**item_row(item, rep), **scores,
                         "latency_s": latency})
            print(f"{label}: {scores['status']} in {latency}s "
                  f"| eval={scores['eval_score']} "
                  f"| top1={scores['top1_actual']} "
                  f"correct={scores['top1_correct']}")

    write_csv(csv_path, rows)
    write_summary(rows, csv_path)
    print(f"\nDone. Raw rows: {csv_path}")
    print(f"Summary: {EVAL_DIR / 'RESULTS.md'}")


def item_row(item, rep):
    return {
        "id": item["id"],
        "rep": rep,
        "query": item["query"],
        "city": item["city"],
        "type": item["type"],
        "has_gt": item.get("has_gt", False),
    }


def write_csv(path, rows):
    if not rows:
        return
    keys = ["id", "rep", "query", "city", "type", "has_gt", "status",
            "eval_score", "gt_correlation", "top1_actual", "top1_correct",
            "top3_hit", "latency_s"]
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=keys, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def pct(x):
    return f"{100*x:.0f}%" if x is not None else "—"


def write_summary(rows, csv_path):
    done = [r for r in rows if r.get("status") == "complete"]
    evals = [r["eval_score"] for r in done
             if isinstance(r.get("eval_score"), (int, float))]
    lats = [r["latency_s"] for r in done
            if isinstance(r.get("latency_s"), (int, float))]
    top1_judged = [r for r in done if r.get("top1_correct") is not None]
    top1_ok = [r for r in top1_judged if r["top1_correct"]]

    def p(series, q):
        if not series:
            return None
        s = sorted(series)
        idx = min(int(q * len(s)), len(s) - 1)
        return s[idx]

    lines = [
        "# NLGeo Benchmark Results",
        "",
        f"Run: {datetime.now().isoformat(timespec='seconds')}  ",
        f"Raw data: `{csv_path.name}`",
        "",
        "## Summary",
        "",
        f"- Queries run: **{len(rows)}**",
        f"- Success rate: **{pct(len(done)/len(rows)) if rows else '—'}** "
        f"({len(done)}/{len(rows)})",
        f"- Mean eval score: **"
        f"{statistics.mean(evals):.3f}"
        f"{' ± ' + format(statistics.stdev(evals), '.3f') if len(evals) > 1 else ''}"
        f"**" if evals else "- Mean eval score: —",
        f"- Top-1 accuracy (where expected known): **"
        f"{pct(len(top1_ok)/len(top1_judged)) if top1_judged else '—'}** "
        f"({len(top1_ok)}/{len(top1_judged)})",
        f"- Latency p50: **{p(lats, 0.50)}s**, p95: **{p(lats, 0.95)}s**"
        if lats else "- Latency: —",
        "",
        "## Per-query",
        "",
        "| id | city | type | status | eval | top1 | correct | latency (s) |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for r in rows:
        lines.append(
            f"| {r['id']} | {r['city']} | {r['type']} | {r.get('status')} "
            f"| {r.get('eval_score') if r.get('eval_score') is not None else '—'} "
            f"| {r.get('top1_actual') or '—'} "
            f"| {'' if r.get('top1_correct') is None else ('✓' if r['top1_correct'] else '✗')} "
            f"| {r.get('latency_s', '—')} |")
    (EVAL_DIR / "RESULTS.md").write_text(
        "\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    main()
