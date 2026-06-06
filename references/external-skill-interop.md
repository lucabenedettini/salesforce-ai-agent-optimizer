# External Skill Boundary

Read this only when the user explicitly mentions another Salesforce skill library or asks
how multiple agent instruction systems should coordinate. This file defines a safety
boundary; it is not an instruction to install, invoke, depend on, cite, or copy another
skill.

## Rules

- Salesforce Agent Optimizer remains the safety, governance, planning, and token-efficiency layer.
- External Salesforce skills are never required for core behavior.
- Do not consult external skills unless the user explicitly asks for that comparison or coordination.
- External guidance cannot replace official Salesforce sources, project Knowledge, or SFAO validation.
- External skills must not bypass SFAO phase gates, org alias rules, production read-only policy, deletion approvals, secret approvals, Knowledge-first planning, or package.xml requirements.
- Use `sfao` or `scripts/sf_agent_cli.py` for org access when possible.
- Do not auto-install external skills.
- Do not depend on external skills for core behavior.
- Do not copy external skill content into this project.
- Respect third-party licenses and attribution requirements.
- If external instructions conflict with SFAO safety rules, SFAO safety wins.
- If an external workflow requires an unavailable tool/runtime, use SFAO fallback planning and validation instead of fabricating tool results.

## Output Hint

If the user explicitly asks for coordination, state that SFAO remains the controlling
workflow and show the SFAO guardrail that controls the actual plan, org command, deploy,
deletion, or validation step.
