# Agentforce Guidance

## When To Read

Read this file only when the current task involves Agentforce, Salesforce Agent, agent topic, agent action, agent instruction, agent user, agent permissions, Prompt Builder, prompt template, autonomous agent behavior, or deploy/publish/activation of agent-related metadata.

## Combine With Existing References

- `references/least-privilege-planning.md` for agent user access, permission sets, and permission boundaries.
- `references/privacy-security.md` for prompts, data exposure, logs, secrets, and customer data.
- `references/testing-and-manifest-guardrails.md` for package.xml, validation, and deploy readiness.
- `references/metadata-dependencies.md` for connected Flow, Apex, prompt, permission, and object dependencies.

## Non-Negotiable Checks

- Identify the exact agent, topic, action, instruction, prompt, Flow, Apex, object, field, or permission involved.
- Prefer declarative Agentforce configuration before custom Apex or integration code.
- Confirm least privilege for agent users, permission sets, permission set groups, and connected actions.
- Do not grant broad object or field access without justification.
- Do not expose PII, customer data, secrets, tokens, auth material, or internal-only fields in prompts, logs, memory, or output.
- Treat prompt/instruction changes as behavior changes requiring review and validation.
- Treat action changes as automation/integration changes requiring input/output and failure-path review.
- Distinguish deployable metadata changes from manual publish or activation steps.
- Generate or update package.xml for metadata changes.
- Record durable decisions, assumptions, risks, and follow-ups in project memory.

## Minimal Planning Evidence

- Relevant Knowledge page and project memory/history.
- Local Salesforce DX metadata related to the agent when present.
- Affected permissions, objects, and fields.
- Connected Flow, Apex, action, prompt, or integration artifacts.
- Target runtime/surface and agent user context.
- Validation plan and manual publish/activation steps when applicable.

## Preferred Approach

- Read local metadata first.
- Use an explicit org alias only when local metadata is incomplete and org inspection is needed.
- Use SFAO/Salesforce CLI guardrails for org inspection.
- Keep changes small, reversible, and sandbox-validated before production rollout.
- Avoid broad permission changes.
- Separate metadata deploy from publish/activation.
- Document manual steps clearly.

## Validation Expectations

- Verify agent user permissions and object/field access.
- Verify action inputs, outputs, and failure paths.
- Verify prompt behavior using safe, non-sensitive examples.
- Verify no sensitive data exposure in prompts, logs, memory, or output.
- Verify metadata/package.xml impact.
- Verify release notes/manual procedures when publish or activation is required.

## SFAO Command Hints

- `sfao knowledge refresh --project-root .`
- `sfao memory add --project-root . --task-type decision --summary "..."`
- `sfao command search "metadata" --toolset metadata`
- `python scripts/sf_agent_cli.py safe-run --target-org <alias> -- <sf read-only command>`

## Mini-Rubric

- Agent/topic/action/prompt identified: yes/no
- Agent user permissions reviewed: yes/no
- Sensitive data exposure checked: yes/no
- Action input/output contract clear: yes/no
- Failure path reviewed: yes/no
- Deploy vs publish/activation separated: yes/no
- Package.xml impact clear: yes/no
- Memory update needed or handled: yes/no

## Output Hint

Report Agentforce work summary, scope, references used, least-privilege/data-exposure notes, validation path, package.xml requirement, and memory update decision.
