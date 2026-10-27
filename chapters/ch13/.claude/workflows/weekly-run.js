export const meta = {
  name: 'weekly-run',
  description: "Dana's Monday run in order: profile the drop, review it with dq-reviewer, then to-parquet, build-marts and kpi-report. Stops at the first failure.",
  phases: ['Review the drop', 'Build the report'],
}

phase('Review the drop')
const profile = await agent(
  'Run `uv run python .claude/skills/profile-data/scripts/dq_profile.py` from the project root as one command. Reply with the last line it prints, or with FAILED and its error message.',
  { label: 'dq profile' },
)
if (!profile || profile.startsWith('FAILED')) return { stoppedAt: 'dq profile', detail: profile }

const review = await agent(
  "Review last night's drop against Luis's five promises.",
  { label: 'dq-reviewer', agentType: 'dq-reviewer' },
)
if (!review) return { stoppedAt: 'dq-reviewer' }

phase('Build the report')
const steps = [
  ['to-parquet', 'Run the to-parquet skill with the argument data/raw.'],
  ['build-marts', 'Run the build-marts skill.'],
  ['kpi-report', 'Run the kpi-report skill for the latest week.'],
]
const outputs = {}
for (const [name, task] of steps) {
  const out = await agent(
    `${task} Reply with the script's output unchanged, or with FAILED and its message.`,
    { label: name },
  )
  if (!out || out.startsWith('FAILED')) return { stoppedAt: name, review, detail: out }
  outputs[name] = out
}
return { review, outputs }
