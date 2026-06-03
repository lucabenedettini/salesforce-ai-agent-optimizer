# Nome del prodotto/pacchetto: User Access and Permissions Assistant

## Breve descrizione sintetica
Salesforce package for analyzing, reporting and managing user permissions and assignments.

## Oggetti principali
- User, PermissionSet, PermissionSetGroup, PermissionSetAssignment.
- Profile, PermissionSetLicenseAssign, ObjectPermissions, FieldPermissions.
- Package report/configuration objects where installed.

## Funzionalita principali
- Permission analysis and reporting.
- Visibility into assignments and access.
- Admin support for permission cleanup.

## Configurazioni principali
- Package permission sets and app access.
- Reports/dashboards and result visibility.
- Access to setup/security metadata.

## Best practice
- Use findings to plan least-privilege permission changes.
- Check permission set groups and muting permission sets together.
- Validate object and field access with a real user or login-as test.
- Avoid broad profile changes when permission sets solve the requirement.
