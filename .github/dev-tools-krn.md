```markdown
# dev-tools-krn — depth-0 extract (Kelvin docs: KRN Reference)

Source: https://docs.kelvin.ai/6.3/developer-tools/how-to/develop/krn/
Fetched: 2025-10-26 (offline extract stored in this repo)

Overview
The Kelvin Resource Name (KRN) Registry is the canonical naming scheme used across the Kelvin platform to uniquely identify resources (assets, data streams, recommendations, schedules, workloads, etc.). It is conceptually similar to URNs or AWS ARNs and follows a consistent, documented format so resources can be referenced unambiguously in `app.yaml`, API calls, and SDK objects.

Specification and format
- A KRN uses a URN-like form that begins with `krn:` followed by a Namespace Identifier (NID) and a Namespace-Specific String (NSS), typically separated by colons and slashes.
- General form examples:
  - `krn:ad:air-conditioner/temperature` (asset data stream)
  - `krn:wl:my-node/modbus-bridge-1` (workload)

KRN components and syntax (high-level)
- `krn` — literal prefix
- `NID` — namespace identifier (short code for type, e.g., `ad`, `asset`, `app`, `datastream`)
- `NSS` — namespace specific string comprising names or hierarchical IDs (may include `/` separators)

Definitions and resource types
Below are the KRN patterns for common resource types (examples included). Use these when you need a stable reference in code, `app.yaml`, or SDK calls.

- Asset Custom Action (aca)
  - Pattern: `krn:aca:<asset>/<action>`
  - Examples: `krn:aca:air-conditioner-1/email`, `krn:aca:beam-pump/Webhook`

- Action (action)
  - Pattern: `krn:action:<action>`
  - Examples: `krn:action:email`, `krn:action:Webhook`

- Asset Data Stream (ad)
  - Pattern: `krn:ad:<asset>/<datastream>`
  - Examples:
    - `krn:ad:air-conditioner-1/temp-setpoint`
    - `krn:ad:beam-pump/casing.temperature`
    - `krn:ad:centrifugal-pump-02/oee`

- Asset Parameter (ap)
  - Pattern: `krn:ap:<asset>/<parameter>`
  - Example: `krn:ap:air-conditioner-1/closed_loop`

- App (app)
  - Pattern: `krn:app:<app>`
  - Examples: `krn:app:smart-pcp`, `krn:app:pvc`

- App Parameter (app-parameter)
  - Pattern: `krn:app-parameter:<app>:<parameter>`
  - Examples: `krn:app-parameter:my-app:my-param`, `krn:app-parameter:smart-pcp:closed_loop`

- App Version (appversion)
  - Pattern: `krn:appversion:<app>/<version>`
  - Examples: `krn:appversion:smart-pcp/2.0.0`, `krn:appversion:pvc/3.0.1`

- Asset (asset)
  - Pattern: `krn:asset:<asset>`
  - Examples: `krn:asset:air-conditioner-1`, `krn:asset:beam-pump`

- Asset Type (asset-type)
  - Pattern: `krn:asset-type/<asset-type>`
  - Example: `krn:asset-type/beam-pump`

- Data Stream (datastream)
  - Pattern: `krn:datastream:<datastream>`
  - Examples: `krn:datastream:temp-setpoint`, `krn:datastream:casing.temperature`, `krn:datastream:oee`

- Data Quality - Asset Data Stream (dqad)
  - Pattern: `krn:dqad:<data-quality>:<asset>/<datastream>`
  - Examples: `krn:dqad:kelvin_timestamp_anomaly:pcp_01/gas_flow`, `krn:dqad:kelvin_out_of_range_detection:pcp_01/gas_flow`

- Data Quality - Asset (dqasset)
  - Pattern: `krn:dqasset:<data-quality>:<asset>`
  - Example: `krn:dqasset:asset_score:pcp01`

- Job (job)
  - Pattern: `krn:job:<job>/<job-run-id>`
  - Example: `krn:job:parameters-schedule-worker/1257897347822083`

- Recommendation (recommendation)
  - Pattern: `krn:recommendation:<uuid>`
  - Example: `krn:recommendation:86a425b4-b43f-4989-a38f-b18f6b3d1ec7`

- Schedule (schedule)
  - Pattern: `krn:schedule:<id>`
  - Example: `krn:schedule:6830a7d3-bcf3-4a64-8126-eaaeeca86676`

- Service Account (srv-acc)
  - Pattern: `krn:srv-acc:<account-name>`
  - Example: `krn:srv-acc:node-client-my-edge-cluster`

- System (system)
  - Pattern: `krn:system:<system_name>`
  - Example: `krn:system:kelvin`

- User (user)
  - Pattern: `krn:user:<username>`
  - Example: `krn:user:me@example.com`

- Workload (wl)
  - Pattern: `krn:wl:<cluster>/<workload>`
  - Example: `krn:wl:my-node/temp-adjuster-1`

- Workload App Version (wlappv)
  - Pattern: `krn:wlappv:<cluster/workload>:<app_name>/<app_version>`
  - Example: `krn:wlappv:my-node/pvc-r312:pvc/1.0.0`

Common components and regex
The docs provide the canonical regex for common components used in KRNs:

- DNS-SAFE-NAME: ^[a-z]([-a-z0-9]*[a-z0-9])?$
- NAME: ^[a-z0-9]([-_.a-z0-9]*[a-z0-9])?$
- NAME-V2: ^[a-zA-Z0-9]([-_ .a-zA-Z0-9]*[a-zA-Z0-9])?$
- SEMVER: Semantic Versioning (see semver spec)
- USERNAME: ([-a-zA-Z0-9()+,.:=@;$_!*'&~\/]|%[0-9a-f]{2})+
- UUID: ^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$

Notes and usage guidance
- Use the KRN patterns above whenever you need to reference platform resources in `app.yaml`, SDK calls, or published messages.
- Document any custom NIDs your SmartApp introduces and ensure they follow the documented syntactic rules.

Authoritative link
- Live docs: https://docs.kelvin.ai/6.3/developer-tools/how-to/develop/krn/

Keep this file in sync with any changes to KRN usage in the repo (for example, if the app starts producing recommendations or using new custom actions, include example KRNs in this file for reviewers).

``` 