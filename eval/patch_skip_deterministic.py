"""
Gate the remaining deterministic paths behind SKIP_DETERMINISTIC so the
ablation's LLM-only arm is valid.

Adds `not SKIP_DETERMINISTIC` to:
  1. the memory-reuse branch          (else cached deterministic code leaks in)
  2. the Mumbai flood benchmark path  (else flood queries stay deterministic)
  3. the generic-engine early path    (else most counts stay deterministic)
  4. the per-capita branch, if found  (deterministic raster code)

Makes analysis_agent.py.bak first. Prints a report; writes only if the two
critical anchors (1, 2) are found.

Run from E:\\GOAI\\PHASE2:
    python eval\\patch_skip_deterministic.py
"""
from pathlib import Path
import shutil
import sys

TARGET = Path(__file__).resolve().parents[1] / "app" / "agents" / "analysis_agent.py"


def main():
    src = TARGET.read_text(encoding="utf-8")
    original = src
    report = []

    # ── 1. memory reuse ──────────────────────────────────────────────
    anchor1 = ("if (not _generic_handles and not _is_satellite_q "
               "and similar and stored_code and")
    if "not SKIP_DETERMINISTIC and not _generic_handles" in src:
        report.append("1. memory reuse: already gated — skipped")
    elif anchor1 in src:
        src = src.replace(
            anchor1,
            "if (not SKIP_DETERMINISTIC and not _generic_handles "
            "and not _is_satellite_q and similar and stored_code and",
            1,
        )
        report.append("1. memory reuse: GATED")
    else:
        report.append("1. memory reuse: ANCHOR NOT FOUND — aborting")

    # ── 2. Mumbai flood benchmark ────────────────────────────────────
    anchor2 = ("if is_mumbai_flood_query(task, plan) and not is_per_capita "
               "and not is_vulnerability and not _hint_has_buffer:")
    if ("is_mumbai_flood_query(task, plan)" in src
            and "not _hint_has_buffer and not SKIP_DETERMINISTIC:" in src):
        report.append("2. mumbai benchmark: already gated — skipped")
    elif anchor2 in src:
        src = src.replace(
            anchor2,
            "if is_mumbai_flood_query(task, plan) and not is_per_capita "
            "and not is_vulnerability and not _hint_has_buffer "
            "and not SKIP_DETERMINISTIC:",
            1,
        )
        report.append("2. mumbai benchmark: GATED")
    else:
        report.append("2. mumbai benchmark: ANCHOR NOT FOUND — aborting")

    # ── 3. generic engine early path (walk up from its print) ────────
    lines = src.splitlines(keepends=True)
    idx = next((i for i, l in enumerate(lines)
                if "Generic engine early path" in l), None)
    if idx is None:
        report.append("3. generic early path: print line not found — MANUAL")
    else:
        gated = False
        for j in range(idx - 1, max(idx - 8, -1), -1):
            stripped = lines[j].lstrip()
            if stripped.startswith("if ") and lines[j].rstrip().endswith(":"):
                if "SKIP_DETERMINISTIC" in lines[j]:
                    report.append("3. generic early path: already gated — skipped")
                else:
                    indent = lines[j][: len(lines[j]) - len(stripped)]
                    cond = stripped[3:].rstrip().rstrip(":")
                    lines[j] = (f"{indent}if not SKIP_DETERMINISTIC "
                                f"and ({cond}):\n")
                    report.append(
                        f"3. generic early path: GATED (line {j + 1})")
                gated = True
                break
        if not gated:
            report.append("3. generic early path: no `if` within 8 lines "
                          "above print — MANUAL")
        src = "".join(lines)

    # ── 4. per-capita branch (best effort) ───────────────────────────
    lines = src.splitlines(keepends=True)
    pc_idx = next((i for i, l in enumerate(lines)
                   if "Per-capita" in l and "print" in l), None)
    if pc_idx is None:
        report.append("4. per-capita: print line not found — left as is "
                      "(acceptable: raster path is arguably data, not shortcut)")
    else:
        done = False
        for j in range(pc_idx - 1, max(pc_idx - 8, -1), -1):
            stripped = lines[j].lstrip()
            if stripped.startswith("if ") and lines[j].rstrip().endswith(":"):
                if "SKIP_DETERMINISTIC" in lines[j]:
                    report.append("4. per-capita: already gated — skipped")
                else:
                    indent = lines[j][: len(lines[j]) - len(stripped)]
                    cond = stripped[3:].rstrip().rstrip(":")
                    lines[j] = (f"{indent}if not SKIP_DETERMINISTIC "
                                f"and ({cond}):\n")
                    report.append(f"4. per-capita: GATED (line {j + 1})")
                done = True
                break
        if not done:
            report.append("4. per-capita: no `if` found above print — MANUAL")
        src = "".join(lines)

    print("\n".join(report))

    critical_fail = any("ANCHOR NOT FOUND" in r for r in report)
    if critical_fail:
        print("\nNo changes written (critical anchor missing).")
        sys.exit(1)

    if src != original:
        shutil.copy(TARGET, TARGET.with_suffix(".py.bak"))
        TARGET.write_text(src, encoding="utf-8", newline="")
        print(f"\nWritten. Backup at {TARGET.with_suffix('.py.bak').name}")
        import ast
        try:
            ast.parse(src)
            print("Syntax check: OK")
        except SyntaxError as e:
            print(f"Syntax check FAILED: {e} — restore the .bak!")
            sys.exit(2)
    else:
        print("\nNothing to change.")


if __name__ == "__main__":
    main()
