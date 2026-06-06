# Iterative Tool Guardrails

Read this only when a task requires repeated tool calls, external skill workflow loops, generated
metadata iterations, or long-running validation/refinement cycles.

## Rules

- Define the completion condition before starting the loop.
- Use a small maximum iteration cap unless the runtime already enforces one.
- Default cap: 10 iterations.
- Stop and report partial evidence when the cap is reached.
- Never claim a tool result that was not actually returned.
- Do not continue expensive loops blindly.
- Do not ask the user to approve every safe internal loop step when continuation is expected.
- Stop for user approval if risk, cost, scope, destructive impact, secret exposure, or ambiguity increases.
- For Flow or generated-metadata workflows, if a required tool is unavailable, do not fake metadata.
- Provide a fallback plan or ask for the missing environment/tool.

## Output Hint

Keep loop status compact:

```text
Tool loop: 3/10
Completion condition: deploy validation succeeds
Last evidence: Flow XML validation error on Decision node
Next action: adjust approved metadata shape and rerun validation
```
