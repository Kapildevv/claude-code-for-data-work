"""Write Dana's weekly KPI report from the marts in warehouse.duckdb.

Run it from the project root, with a week's Monday or with no argument for the latest week:

    uv run python .claude/skills/kpi-report/scripts/kpi_report.py 2026-09-21

It writes reports/kpi-<week>.md and two PNG charts beside it, and prints their paths and one
headline line. The numbers in the markdown come straight from the marts.
"""

import argparse
import sys
from datetime import date, timedelta
from pathlib import Path

import duckdb
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

INK, MUTED, GRID, BAR, MARK = "#1f2933", "#52606d", "#e4e7eb", "#9aa5b1", "#1c5d99"

parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
parser.add_argument("week", nargs="?", help="Monday of the report week, such as 2026-09-21; default: the latest week")
args = parser.parse_args()

if not Path("warehouse.duckdb").exists():
    sys.exit("warehouse.duckdb not found: run the build-marts skill first")
con = duckdb.connect("warehouse.duckdb", read_only=True)
weeks = con.sql("select * from weekly_sales order by week_start").fetchall()
cols = [d[0] for d in con.sql("select * from weekly_sales").description]
weeks = [dict(zip(cols, row)) for row in weeks]
by_start = {str(w["week_start"]): w for w in weeks}
start = args.week or str(weeks[-1]["week_start"])
if start not in by_start:
    sys.exit(f"{start} is not a week in weekly_sales; the weeks run {weeks[0]['week_start']} to {weeks[-1]['week_start']}")
week = by_start[start]
end = week["week_start"] + timedelta(days=6)

stores = con.sql("""
    select store_id, store_name, net_sales from store_weekly
    where week_start = ? order by net_sales desc, store_id limit 3""", params=[start]).fetchall()
products = con.sql("""
    select product_id, product_name, units, net_sales from product_weekly
    where week_start = ? order by net_sales desc, product_id limit 5""", params=[start]).fetchall()


def money(value) -> str:
    return f"${value:,.2f}"


def style(ax):
    ax.spines[["top", "right"]].set_visible(False)
    ax.spines[["left", "bottom"]].set_color(GRID)
    ax.tick_params(colors=MUTED, labelsize=8)
    ax.grid(axis="y", color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)


Path("reports").mkdir(exist_ok=True)
labels = [w["week_start"].strftime("%m-%d") for w in weeks]
positions = range(len(weeks))
highlight = [str(w["week_start"]) == start for w in weeks]

fig, ax = plt.subplots(figsize=(7, 3.2))
ax.bar(positions, [float(w["net_sales"]) for w in weeks], color=[MARK if h else BAR for h in highlight], width=0.65)
ax.set_xticks(list(positions), labels)
ax.yaxis.set_major_formatter(lambda v, _: f"${v / 1000:.0f}k")
ax.set_title("Net sales by week", loc="left", color=INK, fontsize=11)
ax.set_xlabel("Week starting (2026)", color=MUTED, fontsize=8)
style(ax)
net_chart = f"kpi-{start}-net-sales.png"
fig.tight_layout()
fig.savefig(f"reports/{net_chart}", dpi=150)
plt.close(fig)

fig, ax = plt.subplots(figsize=(7, 3.2))
ax.plot(list(positions), [float(w["returns_rate"]) * 100 for w in weeks], color=BAR, linewidth=2, marker="o", markersize=5)
index = [str(w["week_start"]) for w in weeks].index(start)
ax.plot([index], [float(week["returns_rate"]) * 100], marker="o", markersize=8, color=MARK)
ax.set_xticks(list(positions), labels)
ax.yaxis.set_major_formatter(lambda v, _: f"{v:.0f}%")
ax.set_ylim(bottom=0)
ax.set_title("Returns rate by week", loc="left", color=INK, fontsize=11)
ax.set_xlabel("Week starting (2026)", color=MUTED, fontsize=8)
style(ax)
rate_chart = f"kpi-{start}-returns-rate.png"
fig.tight_layout()
fig.savefig(f"reports/{rate_chart}", dpi=150)
plt.close(fig)

lines = [
    "# Juniper Lane Goods: weekly KPI report",
    "",
    f"Week of {week['week_start']} to {end}",
    "",
    "| Measure | Value |",
    "|---|---:|",
    f"| Net sales | {money(week['net_sales'])} |",
    f"| Gross sales | {money(week['gross_sales'])} |",
    f"| Returns value | {money(week['returns_value'])} |",
    f"| Returns rate | {float(week['returns_rate']):.2%} |",
    f"| Orders | {week['orders']:,} |",
    f"| Returns | {week['returns']} ({week['late_returns']} late) |",
    "",
    "## Top stores by net sales",
    "",
    "| Store | Net sales |",
    "|---|---:|",
    *[f"| {sid} {name} | {money(net)} |" for sid, name, net in stores],
    "",
    "## Top products by net sales",
    "",
    "| Product | Units | Net sales |",
    "|---|---:|---:|",
    *[f"| {pid} {name} | {units} | {money(net)} |" for pid, name, units, net in products],
    "",
    "## Charts",
    "",
    f"![Net sales by week]({net_chart})",
    "",
    f"![Returns rate by week]({rate_chart})",
    "",
]
report = Path(f"reports/kpi-{start}.md")
report.write_text("\n".join(lines), encoding="utf-8")

print(report.as_posix())
print(f"reports/{net_chart}")
print(f"reports/{rate_chart}")
top = stores[0]
print(f"net sales {money(week['net_sales'])}, returns rate {float(week['returns_rate']):.2%}, "
      f"top store {top[0]} {top[1]} {money(top[2])}")
