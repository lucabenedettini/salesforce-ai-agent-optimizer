# Least-Privilege Planning

Use this reference during planning for Salesforce changes that create, modify, grant, expose, automate, integrate with, or document user access.

Official basis:

- Salesforce Well-Architected Secure: https://architect.salesforce.com/docs/architect/well-architected/guide/secure
- Configure permissions and access in permission sets: https://help.salesforce.com/s/articleView?id=platform.perm_sets_permissions_access.htm&language=en_US&type=5
- PermissionSetAssignment profile-backed behavior: https://help.salesforce.com/s/articleView?id=000387815&language=en_US&type=1

## Mandatory Rule

Always apply Salesforce least privilege in every plan. Grant only the minimum object, field, app, tab, Apex, Flow, setup, API, package, sharing, and integration permissions required for the approved business task.

Before recommending or changing permissions, inspect current access in the target org for affected users/personas. Ask the user for the org alias and the target users, personas, groups, or user filter. If the user wants offline planning only, state that least-privilege validation is limited until org access is inspected.

If the correct permission scope is unclear, do not guess. Ask the user which persona should receive access, or present scoped options with tradeoffs and wait for a choice.

## Planning Checklist

- Identify personas and business tasks, not just individual users.
- Inspect current profile, permission set assignments, permission set group assignments, permission set licenses, and relevant object/field permissions.
- Prefer Minimum Access style profiles plus modular permission sets and permission set groups for new access.
- Avoid broad profile changes when permission sets or permission set groups solve the requirement.
- Use permission set groups, muting permission sets, and assignment expiration when they reduce over-permissioning.
- Avoid elevated permissions such as Modify All Data, View All Data, Customize Application, Author Apex, Manage Users, API Enabled, Modify Metadata, and package admin permissions unless the requirement explicitly needs them and the user approves the risk.
- Plan data visibility separately from metadata permissions: OWD, role hierarchy, sharing rules, teams, territories, restriction rules, scoping rules, queues, groups, and report/dashboard folders can all affect access.
- Validate access with real users, login-as, user-mode Apex, Flow tests, UI checks, or targeted SOQL evidence when the project supports it.

## Token-Efficient Org Inspection

Use the facade before planning access changes:

```bash
python scripts/sf_agent_cli.py access-inspect --target-org <alias> --username user@example.com --sobject Account --sobject Opportunity --select users.records,permission_set_assignments.records,object_permissions.records,field_permissions.records
```

For persona/user filters:

```bash
python scripts/sf_agent_cli.py access-inspect --target-org <alias> --where "IsActive = true AND Profile.Name = 'Sales User'" --sobject Account --limit 10 --select users.records,permission_set_assignments.records
```

For package or admin access, combine `access-inspect` with narrow `data-query` calls only for the affected metadata or objects. Do not dump all profiles, permission sets, or field permissions unless the user explicitly approves a broad audit.

## Plan Output

Every plan must include:

- Personas/users inspected or the reason inspection was deferred.
- Current access evidence summarized in one compact paragraph or table.
- Proposed permission delta with exact metadata names when known.
- Why the delta is least-privileged.
- Any unclear permission decision as a user question or selectable scenario.
