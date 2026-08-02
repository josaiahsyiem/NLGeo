"""
Audit + gate ALL deterministic analysis-path branches for SKIP_DETERMINISTIC.

Finds every `print("[Analysis] ... path")`-style line in analysis_agent.py,
walks up to the nearest `if`, reports whether it is gated, and gates any
that are not (except the LLM fallback itself).

Run from E:\\GOAI\\PHASE2:
    python eval\\patch_skip_all_paths.py
"""
from pathlib import Path
import shutil
import sys

TARGET = Path(__file__).resolve().parents[1] / "app" / "agents" / "analysis_agent.py"

# branches that must NOT be gated (the LLM fallback and error paths)
NEVER_GATE = ("LLM", "llm", "fallback", "code generation", "generated")


def main():
    src = TARGET.read_text(encoding="utf-8")
    lines = src.splitlines(keepends=True)
    report, changed = [], 0

    for i, line in enumerate(lines):
        if "print(" not in line or "[Analysis]" not in line:
            continue
        low = line.lower()
        if "path" not in low:
            continue
        label = line.strip()[:70]
        if any(k.lower() in low for k in NEVER_GATE):
            report.append(f"  line {i+1}: {label}  -> LLM/fallback, left ungated")
            continue
        # walk up to nearest `if `
        gated_here = False
        for j in range(i - 1, max(i - 10, -1), -1):
            stripped = lines[j].lstrip()
            if stripped.startswith("if ") and lines[j].rstrip().endswith(":"):
                if "SKIP_DETERMINISTIC" in lines[j]:
                    report.append(f"  line {i+1}: {label}  -> already gated")
                else:
                    indent = lines[j][: len(lines[j]) - len(stripped)]
                    cond = stripped[3:].rstrip().rstrip(":")
                    lines[j] = (f"{indent}if not SKIP_DETERMINISTIC "
                                f"and ({cond}):\n")
                    report.append(f"  line {i+1}: {label}  -> GATED NOW (if at line {j+1})")
                    changed += 1
                gated_here = True
                break
        if not gated_here:
            report.append(f"  line {i+1}: {label}  -> NO `if` FOUND ABOVE — check manually")

    print("Audit of [Analysis] path branches:")
    print("\n".join(report) if report else "  none found")

    if changed:
        new_src = "".join(lines)
        import ast
        try:
            ast.parse(new_src)
        except SyntaxError as e:
            print(f"\nSyntax check FAILED, nothing written: {e}")
            sys.exit(2)
        shutil.copy(TARGET, str(TARGET) + ".bak2")
        TARGET.write_text(new_src, encoding="utf-8", newline="")
        print(f"\n{changed} branch(es) newly gated. Backup: analysis_agent.py.bak2. Syntax OK.")
    else:
        print("\nNo changes needed.")


if __name__ == "__main__":
    main()
