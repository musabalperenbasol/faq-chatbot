"""Compare which mutants each test-suite variant killed. Writes suite_comparison.md."""

import re
from pathlib import Path

DIR = Path("docs/ai_evidence/mutation")
SUITES = ["ours", "ai", "combined", "all"]
SURVIVED = re.compile(r"^\s*(\S+):\s*survived")
PROGRESS = re.compile(r"(\d+)/(\d+)")


def survivors(name):
    lines = (DIR / f"suite_{name}_survivors.txt").read_text(encoding="utf-8").splitlines()
    return {m.group(1) for line in lines if (m := SURVIVED.match(line))}


def total_mutants(name):
    text = (DIR / f"suite_{name}_run.txt").read_text(encoding="utf-8")
    return int(PROGRESS.findall(text)[-1][1])


surv = {name: survivors(name) for name in SUITES}
total = total_mutants("ours")

out = ["# Suite comparison (mutation testing)", "", "| Suite | Killed | Survived | Score |", "|---|---|---|---|"]
for name in SUITES:
    survived = len(surv[name])
    killed = total - survived
    out.append(f"| {name} | {killed} | {survived} | {killed / total:.1%} |")


def listing(title, mutants):
    out.extend(["", f"## {title} ({len(mutants)})", ""])
    if mutants:
        out.extend(f"- {m}" for m in sorted(mutants))
    else:
        out.append("(none)")


listing("Killed by the AI suite but survived our suite", surv["ours"] - surv["ai"])
listing("Killed by our suite but survived the AI suite", surv["ai"] - surv["ours"])
listing("Survived BOTH suites", surv["ours"] & surv["ai"])
listing("Survived even the final suite (all)", surv["all"])

text = "\n".join(out) + "\n"
(DIR / "suite_comparison.md").write_text(text, encoding="utf-8")
print(text)
