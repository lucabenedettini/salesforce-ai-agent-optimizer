# Official Salesforce CLI Command Catalog

Generated: `2026-06-02T18:35:20+00:00`

This catalog is generated from the installed `sf commands --json` output. Use `scripts/sf_agent_cli.py safe-run` for commands not exposed as first-class facade commands.

Safety values are heuristic and intentionally conservative. `write` and `execute` commands are blocked on production by the agent facade.

| Command | Safety | Target Org | JSON | Project | Summary |
|---|---:|---:|---:|---:|---|
| `agent:activate` | `write` | yes | yes | no | Activate an agent in an org. |
| `agent:create` | `write` | yes | yes | yes | Create an agent in your org using a local agent spec file. |
| `agent:deactivate` | `write` | yes | yes | no | Deactivate an agent in an org. |
| `agent:generate:agent-spec` | `execute` | yes | yes | yes | Generate an agent spec, which is a YAML file that captures what an agent can do. |
| `agent:generate:authoring-bundle` | `execute` | yes | yes | yes | Generate an authoring bundle from an existing agent spec YAML file. |
| `agent:generate:template` | `local` | no | yes | yes | Generate an agent template from an existing agent in your DX project so you can then package the template in a second-generation managed package. |
| `agent:generate:test-spec` | `local` | no | no | no | Generate an agent test spec, which is a YAML file that lists the test cases for testing a specific agent. |
| `agent:preview` | `read` | yes | no | yes | Interact with an agent to preview how it responds to your statements, questions, and commands (utterances). |
| `agent:preview:end` | `read` | yes | yes | yes | End an existing programmatic agent preview session and get trace location. |
| `agent:preview:send` | `read` | yes | yes | yes | Send a message to an existing agent preview session. |
| `agent:preview:sessions` | `read` | no | yes | yes | List all known programmatic agent preview sessions. |
| `agent:preview:start` | `read` | yes | yes | yes | Start a programmatic agent preview session. |
| `agent:publish:authoring-bundle` | `write` | yes | yes | yes | Publish an authoring bundle to your org, which results in a new agent or a new version of an existing agent. |
| `agent:test:create` | `write` | yes | yes | no | Create an agent test in your org using a local test spec YAML file. |
| `agent:test:list` | `read` | yes | yes | no | List the available agent tests in your org. |
| `agent:test:results` | `execute` | yes | yes | no | Get the results of a completed agent test run. |
| `agent:test:resume` | `read` | yes | yes | no | Resume an agent test that you previously started in your org so you can view the test results. |
| `agent:test:run` | `execute` | yes | yes | no | Start an agent test in your org. |
| `agent:test:run-eval` | `execute` | yes | yes | no | Run rich evaluation tests against an Agentforce agent. |
| `agent:trace:delete` | `write` | no | yes | yes | Delete trace files from an agent preview session. |
| `agent:trace:list` | `read` | no | yes | yes | List the available trace files that were recorded during all agent preview sessions. |
| `agent:trace:read` | `read` | no | yes | yes | Read trace files from an agent preview session. |
| `agent:validate:authoring-bundle` | `execute` | yes | yes | yes | Validate an authoring bundle to ensure its Agent Script file compiles successfully and can be used to publish an agent. |
| `alias:list` | `read` | no | no | no | List all aliases currently set on your local computer. |
| `alias:set` | `read` | no | no | no | Set one or more aliases on your local computer. |
| `alias:unset` | `read` | no | no | no | Unset one or more aliases that are currently set on your local computer. |
| `apex:get:log` | `read` | yes | yes | no | Fetch the specified log or given number of most recent logs from the org. |
| `apex:get:test` | `read` | yes | yes | no | Display test results for a specific asynchronous test run. |
| `apex:list:log` | `read` | yes | yes | no | Display a list of IDs and general information about debug logs. |
| `apex:run` | `execute` | yes | yes | no | Execute anonymous Apex code entered on the command line or from a local file. |
| `apex:run:test` | `execute` | yes | yes | no | Invoke Apex tests in an org. |
| `apex:tail:log` | `read` | yes | no | no | Activate debug logging and display logs in the terminal. |
| `api:request:graphql` | `read` | yes | yes | no | Execute a GraphQL statement. |
| `api:request:rest` | `read` | yes | no | no | Make an authenticated HTTP request using the Salesforce REST API. |
| `autocomplete` | `local` | no | no | no |  |
| `cmdt:generate:field` | `local` | no | yes | yes | Generate a field for a custom metadata type based on the provided field type. |
| `cmdt:generate:fromorg` | `execute` | yes | yes | yes | Generate a custom metadata type and all its records from a Salesforce object. |
| `cmdt:generate:object` | `local` | no | yes | yes | Generate a new custom metadata type in the current project. |
| `cmdt:generate:record` | `local` | no | yes | yes | Generate a new record for a given custom metadata type in the current project. |
| `cmdt:generate:records` | `local` | no | yes | yes | Generate new custom metadata type records from a CSV file. |
| `code-analyzer:config` | `read` | no | no | no | Output the current state of configuration for Code Analyzer. |
| `code-analyzer:rules` | `read` | no | no | no | List the rules that are available to analyze your code. |
| `code-analyzer:run` | `execute` | no | no | no | Analyze your code with a selection of rules to ensure good coding practices. |
| `commands` | `local` | no | yes | no |  |
| `community:create` | `write` | yes | yes | no | Create an Experience Cloud site using a template. |
| `community:list:template` | `read` | yes | yes | no | Retrieve the list of templates available in your org. |
| `community:publish` | `write` | yes | yes | no | Publish an Experience Builder site to make it live. |
| `config:get` | `local` | no | yes | no | Get the value of a configuration variable. |
| `config:list` | `local` | no | yes | no | List the configuration variables that you've previously set. |
| `config:set` | `local` | no | yes | no | Set one or more configuration variables, such as your default org. |
| `config:unset` | `local` | no | yes | no | Unset local or global configuration variables. |
| `data:bulk:results` | `read` | yes | yes | no | Get the results of a bulk ingest job that you previously ran. |
| `data:create:file` | `write` | yes | yes | no | Upload a local file to an org. |
| `data:create:record` | `write` | yes | yes | no | Create and insert a record into a Salesforce or Tooling API object. |
| `data:delete:bulk` | `write` | yes | yes | no | Bulk delete records from an org using a CSV file. Uses Bulk API 2.0. |
| `data:delete:record` | `write` | yes | yes | no | Deletes a single record from a Salesforce or Tooling API object. |
| `data:delete:resume` | `read` | yes | yes | no | Resume a bulk delete job that you previously started. Uses Bulk API 2.0. |
| `data:export:bulk` | `read` | yes | yes | no | Bulk export records from an org into a file using a SOQL query. Uses Bulk API 2.0. |
| `data:export:resume` | `read` | no | yes | no | Resume a bulk export job that you previously started. Uses Bulk API 2.0. |
| `data:export:tree` | `read` | yes | yes | no | Export data from an org into one or more JSON files. |
| `data:get:record` | `read` | yes | yes | no | Retrieve and display a single record of a Salesforce or Tooling API object. |
| `data:import:bulk` | `read` | yes | yes | no | Bulk import records into a Salesforce object from a CSV file. Uses Bulk API 2.0. |
| `data:import:resume` | `read` | no | yes | no | Resume a bulk import job that you previously started. Uses Bulk API 2.0. |
| `data:import:tree` | `read` | yes | yes | no | Import data from one or more JSON files into an org. |
| `data:query` | `read` | yes | yes | no | Execute a SOQL query. |
| `data:resume` | `read` | yes | yes | no | View the status of a bulk data load job or batch. |
| `data:search` | `read` | yes | yes | no | Execute a SOSL text-based search query. |
| `data:update:bulk` | `write` | yes | yes | no | Bulk update records to an org from a CSV file. Uses Bulk API 2.0. |
| `data:update:record` | `write` | yes | yes | no | Updates a single record of a Salesforce or Tooling API object. |
| `data:update:resume` | `read` | no | yes | no | Resume a bulk update job that you previously started. Uses Bulk API 2.0. |
| `data:upsert:bulk` | `write` | yes | yes | no | Bulk upsert records to an org from a CSV file. Uses Bulk API 2.0. |
| `data:upsert:resume` | `read` | yes | yes | no | Resume a bulk upsert job that you previously started. Uses Bulk API 2.0. |
| `dev:audit:messages` | `read` | no | yes | no | Audit messages in a plugin's messages directory to locate unused messages and missing messages that have references in source code. |
| `dev:convert:messages` | `read` | no | yes | no | Convert a .json messages file into Markdown. |
| `dev:convert:script` | `read` | no | yes | no | Convert a script file that contains deprecated sfdx-style commands to use the new sf-style commands instead. |
| `dev:generate:command` | `local` | no | no | no | Generate a new sf command. |
| `dev:generate:flag` | `local` | no | no | no | Generate a flag for an existing command. |
| `dev:generate:plugin` | `local` | no | no | no | Generate a new sf plugin. |
| `doctor` | `read` | no | yes | no | Gather CLI configuration data and run diagnostic tests to discover and report potential problems in your environment. |
| `flow:get:test` | `read` | yes | yes | no | Display test results for a specific asynchronous test run. |
| `flow:run:test` | `execute` | yes | yes | no | Invoke flow tests in an org. |
| `force:data:bulk:delete` | `write` | yes | yes | no | Bulk delete records from an org using a CSV file. Uses Bulk API 1.0. |
| `force:data:bulk:status` | `read` | yes | yes | no | View the status of a bulk data load job or batch. Uses Bulk API 1.0. |
| `force:data:bulk:upsert` | `write` | yes | yes | no | Bulk upsert records to an org from a CSV file. Uses Bulk API 1.0. |
| `force:lightning:lwc:test:create` | `write` | no | no | yes |  |
| `force:lightning:lwc:test:run` | `execute` | no | no | yes |  |
| `force:lightning:lwc:test:setup` | `execute` | no | no | yes |  |
| `force:package:push-upgrade:list` | `read` | no | yes | no | Lists the status of push upgrade requests for a given package. |
| `help` | `read` | no | no | no |  |
| `info:releasenotes:display` | `read` | no | yes | no | Display Salesforce CLI release notes on the command line. |
| `lightning:dev:app` | `read` | yes | no | no | Preview a Lightning Experience app locally and in real-time, without deploying it. |
| `lightning:dev:component` | `read` | yes | yes | no | Preview LWC components in isolation. |
| `lightning:dev:site` | `read` | yes | no | no | Preview an Experience Builder site locally and in real-time, without deploying it. |
| `logic:get:test` | `read` | yes | yes | no | Get the results of a test run. |
| `logic:run:test` | `execute` | yes | yes | no | Invoke tests for Apex and Flows in an org. |
| `org:assign:permset` | `write` | yes | no | no | Assign a permission set to one or more org users. |
| `org:assign:permsetlicense` | `write` | yes | yes | no | Assign a permission set license to one or more org users. |
| `org:auth:show-access-token` | `auth` | yes | yes | no | Show the current access token for an org. |
| `org:auth:show-sfdx-auth-url` | `auth` | yes | yes | no | Show the SFDX Auth URL for an org. |
| `org:auth:show-user-password` | `auth` | yes | yes | no | Show the stored password for an org's user. |
| `org:create:agent-user` | `write` | yes | yes | no | Create the default Salesforce user that is used to run an agent. |
| `org:create:sandbox` | `write` | yes | no | no | Create a sandbox org. |
| `org:create:scratch` | `write` | no | yes | no | Create a scratch org. |
| `org:create:shape` | `write` | yes | yes | no | Create a scratch org configuration (shape) based on the specified source org. |
| `org:create:snapshot` | `write` | no | yes | no | Create a snapshot of a scratch org. |
| `org:create:user` | `write` | yes | yes | no | Create a user for a scratch org. |
| `org:delete:sandbox` | `write` | yes | yes | no | Delete a sandbox. |
| `org:delete:scratch` | `write` | yes | yes | no | Delete a scratch org. |
| `org:delete:shape` | `write` | yes | yes | no | Delete all org shapes for a target org. |
| `org:delete:snapshot` | `write` | no | yes | no | Delete a scratch org snapshot. |
| `org:disable:tracking` | `write` | yes | yes | no | Prevent Salesforce CLI from tracking changes in your source files between your project and an org. |
| `org:display` | `read` | yes | yes | no | Display information about an org. |
| `org:display:user` | `read` | yes | yes | no | Display information about a Salesforce user. |
| `org:enable:tracking` | `write` | yes | yes | no | Allow Salesforce CLI to track changes in your source files between your project and an org. |
| `org:generate:password` | `execute` | yes | no | no | Generate a random password for scratch org users. |
| `org:get:snapshot` | `read` | no | yes | no | Get details about a scratch org snapshot. |
| `org:list` | `read` | no | yes | no | List all orgs you’ve created or authenticated to. |
| `org:list:auth` | `auth` | no | yes | no | List authorization information about the orgs you created or logged into. |
| `org:list:limits` | `read` | yes | yes | no | Display information about limits in your org. |
| `org:list:metadata` | `read` | yes | yes | no | List the metadata components and properties of a specified type. |
| `org:list:metadata-types` | `read` | yes | yes | no | Display details about the metadata types that are enabled for your org. |
| `org:list:shape` | `read` | no | yes | no | List all org shapes you’ve created. |
| `org:list:snapshot` | `read` | no | yes | no | List scratch org snapshots. |
| `org:list:sobject:record-counts` | `read` | yes | yes | no | Display record counts for the specified standard or custom objects. |
| `org:list:users` | `read` | yes | yes | no | List all locally-authenticated users of an org. |
| `org:login:access-token` | `auth` | no | yes | no | Authorize an org using an existing Salesforce access token. |
| `org:login:jwt` | `auth` | no | yes | no | Log in to a Salesforce org using a JSON web token (JWT). |
| `org:login:sfdx-url` | `auth` | no | yes | no | Authorize an org using a Salesforce DX authorization URL stored in a file or through standard input (stdin). |
| `org:login:web` | `auth` | no | yes | no | Log in to a Salesforce org using the web server flow. |
| `org:logout` | `auth` | yes | yes | no | Log out of a Salesforce org. |
| `org:open` | `read` | yes | yes | no | Open your default scratch org, or another specified org, in a browser. |
| `org:open:agent` | `read` | yes | yes | no | Open an agent in your org's Agent Builder UI in a browser. |
| `org:refresh:sandbox` | `read` | yes | no | no | Refresh a sandbox org using the sandbox name. |
| `org:resume:sandbox` | `read` | yes | no | no | Check the status of a sandbox creation, and log in to it if it's ready. |
| `org:resume:scratch` | `read` | no | yes | no | Resume the creation of an incomplete scratch org. |
| `package1:version:create` | `read` | yes | yes | no | Create a first-generation package version in the release org. |
| `package1:version:create:get` | `read` | yes | yes | no | Retrieve the status of a package version creation request. |
| `package1:version:display` | `read` | yes | yes | no | Display details about a first-generation package version. |
| `package1:version:list` | `read` | yes | yes | no | List package versions for the specified first-generation package or for the org. |
| `package:convert` | `read` | no | yes | yes | Convert a managed-released first-generation managed package into a second-generation managed package. |
| `package:create` | `write` | no | yes | yes | Create a package. |
| `package:delete` | `write` | no | yes | no | Delete a package. |
| `package:install` | `write` | yes | yes | no | Install or upgrade a version of a package in the target org. |
| `package:install:report` | `read` | yes | yes | no | Retrieve the status of a package installation request. |
| `package:installed:list` | `read` | yes | yes | no | List the org’s installed packages. |
| `package:list` | `read` | no | yes | no | List all packages in the Dev Hub org. |
| `package:push-upgrade:abort` | `read` | no | yes | no | Abort a package push upgrade that has been scheduled. Only push upgrade requests with a status of Created or Pending can be aborted. |
| `package:push-upgrade:list` | `read` | no | yes | no | Lists the status of push upgrade requests for a given package. |
| `package:push-upgrade:report` | `read` | no | yes | no | Retrieve the status of a package push upgrade. |
| `package:push-upgrade:schedule` | `read` | no | yes | no | Schedule a package push upgrade. |
| `package:uninstall` | `write` | yes | yes | no | Uninstall a second-generation package from the target org. |
| `package:uninstall:report` | `read` | yes | yes | no | Retrieve the status of a package uninstall request. |
| `package:update` | `write` | no | yes | no | Update package details. |
| `package:version:create` | `read` | no | yes | yes | Create a package version in the Dev Hub org. |
| `package:version:create:list` | `read` | no | yes | no | List package version creation requests. |
| `package:version:create:report` | `read` | no | yes | no | Retrieve details about a package version creation request. |
| `package:version:delete` | `read` | no | yes | no | Delete a package version. |
| `package:version:displayancestry` | `read` | no | yes | no | Display the ancestry tree for a 2GP managed package version. |
| `package:version:displaydependencies` | `read` | no | yes | no | Display the dependency graph for an unlocked or 2GP managed package version. |
| `package:version:list` | `read` | no | yes | no | List all package versions in the Dev Hub org. |
| `package:version:promote` | `read` | no | yes | no | Promote a package version to released. |
| `package:version:report` | `read` | no | yes | no | Retrieve details about a package version in the Dev Hub org. |
| `package:version:retrieve` | `read` | no | yes | yes | Retrieve package metadata for a specified package version. Package metadata can be retrieved for only second-generation managed package versions or unlocked packages. |
| `package:version:update` | `read` | no | yes | yes | Update a package version. |
| `plugins` | `local` | no | yes | no |  |
| `plugins:add` | `local` | no | yes | no | Installs a plugin into sf. |
| `plugins:discover` | `local` | no | yes | no | See a list of 3rd-party sf plugins you can install. |
| `plugins:inspect` | `local` | no | yes | no |  |
| `plugins:install` | `local` | no | yes | no | Installs a plugin into sf. |
| `plugins:link` | `local` | no | no | no | Links a plugin into the CLI for development. |
| `plugins:remove` | `local` | no | no | no |  |
| `plugins:reset` | `local` | no | no | no | Remove all user-installed and linked plugins. |
| `plugins:trust:allowlist:add` | `local` | no | yes | no | Add plugins to the plugin allowlist. |
| `plugins:trust:allowlist:list` | `local` | no | yes | no | List the plugins on the plugin allowlist. |
| `plugins:trust:allowlist:remove` | `local` | no | yes | no | Remove plugins from the plugin allowlist. |
| `plugins:trust:verify` | `local` | no | yes | no | Validate a digital signature. |
| `plugins:uninstall` | `local` | no | no | no |  |
| `plugins:unlink` | `local` | no | no | no |  |
| `plugins:update` | `local` | no | no | no |  |
| `project:convert:mdapi` | `read` | no | yes | yes | Convert metadata retrieved via Metadata API into the source format used in Salesforce DX projects. |
| `project:convert:source` | `read` | no | yes | yes | Convert source-formatted files into metadata that you can deploy using Metadata API. |
| `project:convert:source-behavior` | `read` | yes | yes | yes | Enable a behavior of your project source files, and then update your Salesforce DX project to implement the behavior. |
| `project:delete:source` | `write` | yes | yes | yes | Delete source from your project and from a non-source-tracked org. |
| `project:delete:tracking` | `write` | yes | yes | yes | Delete all local source tracking information. |
| `project:deploy:cancel` | `write` | yes | yes | no | Cancel a deploy operation. |
| `project:deploy:pipeline:quick` | `write` | no | yes | no | Quickly deploy a validated deployment to an org. |
| `project:deploy:pipeline:report` | `read` | no | yes | no | Check the status of a pipeline deploy operation. |
| `project:deploy:pipeline:resume` | `read` | no | yes | no | Resume watching a pipeline deploy operation. |
| `project:deploy:pipeline:start` | `write` | no | yes | no | Deploy changes from a branch to the pipeline stage’s org. |
| `project:deploy:pipeline:validate` | `execute` | no | yes | no | Perform a validate-only deployment from a branch to the pipeline stage’s org. |
| `project:deploy:preview` | `read` | yes | yes | yes | Preview a deployment to see what will deploy to the org, the potential conflicts, and the ignored files. |
| `project:deploy:quick` | `write` | yes | yes | no | Quickly deploy a validated deployment to an org. |
| `project:deploy:report` | `read` | yes | yes | no | Check or poll for the status of a deploy operation. |
| `project:deploy:resume` | `read` | no | yes | no | Resume watching a deploy operation and update source tracking when the deploy completes. |
| `project:deploy:start` | `write` | yes | yes | no | Deploy metadata to an org from your local project. |
| `project:deploy:validate` | `execute` | yes | yes | no | Validate a metadata deployment without actually executing it. |
| `project:generate:manifest` | `local` | no | yes | yes | Create a project manifest that lists the metadata components you want to deploy or retrieve. |
| `project:list:ignored` | `read` | no | yes | yes | Check your local project package directories for forceignored files. |
| `project:reset:tracking` | `write` | yes | yes | yes | Reset local and remote source tracking. |
| `project:retrieve:preview` | `read` | yes | yes | yes | Preview a retrieval to see what will be retrieved from the org, the potential conflicts, and the ignored files. |
| `project:retrieve:start` | `read` | yes | yes | no | Retrieve metadata from an org to your local project. |
| `schema:generate:field` | `local` | no | no | yes | Generate metadata source files for a new custom field on a specified object. |
| `schema:generate:platformevent` | `local` | no | no | yes | Generate metadata source files for a new platform event. |
| `schema:generate:sobject` | `local` | no | no | yes | Generate metadata source files for a new custom object. |
| `schema:generate:tab` | `local` | no | yes | yes | Generate the metadata source files for a new custom tab on a custom object. |
| `search` | `read` | no | no | no | Search for a command. |
| `sobject:describe` | `read` | yes | yes | no | Display the metadata for a standard or custom object or a Tooling API object. |
| `sobject:list` | `read` | yes | yes | no | List all Salesforce objects of a specified category. |
| `template:generate:analytics:template` | `local` | no | yes | no | Generate a simple Analytics template. |
| `template:generate:apex:class` | `local` | no | yes | no | Generate an Apex class. |
| `template:generate:apex:trigger` | `local` | no | yes | no | Generate an Apex trigger. |
| `template:generate:digital-experience:site` | `execute` | yes | yes | no | Generate an Experience Cloud site. |
| `template:generate:flexipage` | `local` | no | yes | no | Generate a FlexiPage, also known as a Lightning page. |
| `template:generate:lightning:app` | `local` | no | yes | no | Generate a Lightning App. |
| `template:generate:lightning:component` | `local` | no | yes | no | Generate a bundle for an Aura component or a Lightning web component. |
| `template:generate:lightning:event` | `local` | no | yes | no | Generate a Lightning Event. |
| `template:generate:lightning:interface` | `local` | no | yes | no | Generate a Lightning Interface. |
| `template:generate:lightning:test` | `execute` | no | yes | no | Generate a Lightning test. |
| `template:generate:project` | `local` | no | yes | no | Generate a Salesforce DX project. |
| `template:generate:static-resource` | `local` | no | yes | no | Generate a static resource. |
| `template:generate:ui-bundle` | `local` | no | yes | no | Generate a UI bundle, which contains the code and metadata to build a UI experience that uses non-native Salesforce frameworks, such as React. |
| `template:generate:visualforce:component` | `local` | no | yes | no | Generate a Visualforce Component. |
| `template:generate:visualforce:page` | `local` | no | yes | no | Generate a Visualforce Page. |
| `ui-bundle:dev` | `read` | yes | yes | no | Preview a UI bundle locally and in real-time, without deploying it to your org. |
| `update` | `write` | no | no | no |  |
| `version` | `local` | no | yes | no |  |
| `whatsnew` | `read` | no | yes | no | Display Salesforce CLI release notes on the command line. |
| `which` | `read` | no | yes | no |  |

## Usage

```bash
python scripts/sf_agent_cli.py safe-run --target-org dev-sandbox -- data query --query "SELECT Id, Name FROM Account LIMIT 20" --select result.records
```

Refresh this catalog after upgrading Salesforce CLI:

```bash
python scripts/sf_agent_cli.py catalog-refresh
```
