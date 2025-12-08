# Kelvin Resource Name Registry

## Overview

The Kelvin Resource Name (KRN) Registry serves as the centralized system for uniquely identifying various types of resources within the Kelvin Platform. It is conceptually similar to Uniform Resource Names (URN) or Amazon Resource Names (ARN), tailored for Kelvin's use.

## Specification

A KRN must conform to the following criteria:

* **Format**: A KRN should adhere to a specific URN-based format that starts with `krn:` followed by a Namespace Identifier (NID) and a Namespace-Specific String (NSS), separated by colons.
  * **Example for Data Streams**: `krn:ad:air-conditioner/temperature`
  * **Example for Workloads**: `krn:wl:my-node/modbus-bridge-1`
* **Validity**: It must be a valid URN scheme URI, which means it has to contain at least a NID and an NSS.
*   **Syntax**: The KRN should follow a subset of the URN's ABNF syntax rules, as outlined below:

    ```makefile
    makefileCopy codekrn           = "krn" ":" NID ":" NSS
    NID           = (alphanum) 0*30(ldh) (alphanum)
    NSS           = pchar *(pchar / "/")
    ```
* **Documentation**: All NIDs used in KRN must be documented, along with the NSS specification.

## Definitions

* [Asset Custom Action (`aca`)](#asset-custom-action)
* [Action (`action`)](#action)
* [Asset Data Stream (`ad`)](#asset-data-stream)
* [Asset Parameter (`ap`)](#asset-parameter)
* [App (`app`)](#app)
* [App Parameter (`app-parameter`)](#app-parameter)
* [App Version (`appversion`)](#app-version)
* [Asset (`asset`)](#asset)
* [Asset Type (`asset-type`)](#asset-type)
- [Control Change (`control-change`)](#control-change)
* [Data Stream(`datastream`)](#data-stream)
* [Data Quality - Asset Data Stream (`dqad`)](#data-quality-asset-data-stream)
* [Data Quality - Asset (`dqasset`)](#data-quality-asset)
* [Job (`job`)](#job)
* [Recommendation (`recommendation`)](#recommendation)
* [Schedule (`schedule`)](#schedule)
* [Service Account (`srv-acc`)](#service-account)
* [System (`system`)](#system)
* [User (`user`)](#user)
* [Workload (`wl`)](#workload)
* [Workload App Version(`wlappv`)](#workload-app-version)

## Asset Custom Action

```abnf
aca-krn = "krn" ":" "aca" ":" asset "/" action

asset = NAME
action = NAME-V2
```

**Examples**

```
krn:aca:air-conditioner-1/email
krn:aca:beam-pump/Webhook
```


## Action

```abnf
action-krn = "krn" ":" "action" ":" email

action     = NAME-V2
```

**Examples**

```
krn:action:email
krn:action:Webhook
```


## Asset Data Stream

```abnf
ad-krn = "krn" ":" "ad" ":" asset "/" datastream

asset       = NAME
datastream = NAME
```

**SDK Example**

```python linenums="1"
from kelvin.krn import KRNAssetDataStream

KRNAssetDataStream(asset="air-conditioner-1", data_stream="temp-setpoint")
```

**Examples**

```
krn:ad:air-conditioner-1/temp-setpoint
krn:ad:beam-pump/casing.temperature
krn:ad:centrifugal-pump-02/oee
krn:ad:centrifugal-pump-02/failure_quotient
```


## Asset Parameter
```abnf
ap-krn = "krn" ":" "ap" ":" asset "/" parameter

asset  = NAME
parameter = NAME
```

**SDK Example**

```python linenums="1"
from kelvin.krn import KRNAssetParameter

KRNAssetParameter(asset="air-conditioner-1",parameter="closed_loop")
```

**Examples**

```
krn:ap:air-conditioner-1/closed_loop
```


## App

```abnf
app-krn = "krn" ":" "app" ":" app

app     = NAME
```

**SDK Example**

```python linenums="1"
from kelvin.krn import KRNApp

KRNApp(app="smart-pcp")
```

**Examples**

```
krn:app:smart-pcp
krn:app:pvc
```


## App Parameter

```abnf
app-parameter-krn = "krn" ":" "app-paramter" ":" app ":" parameter

app       = NAME
parameter = NAME
```

**Examples**

```
krn:app-parameter:my-app:my-param
krn:app-parameter:smart-pcp:closed_loop
```


## App Version

```abnf
appversion-krn = "krn" ":" "appversion" ":" app "/" version

app     = NAME
version = NAME
```

**SDK Example**

```python linenums="1"
from kelvin.krn import KRNAppVersion

KRNAppVersion(app="smart-pcp",version="2.0.0")
```

**Examples**

```
krn:appversion:smart-pcp/2.0.0
krn:appversion:pvc/3.0.1
```


## Asset

```abnf
asset-krn = "krn" ":" "asset" ":" asset

asset  = NAME
```

**SDK Example**

```python linenums="1"
from kelvin.krn import KRNAsset

KRNAsset(asset="air-conditioner-1")
```

**Examples**

```
krn:asset:air-conditioner-1
krn:asset:beam-pump
```


## Asset Type

```abnf
asset-type-krn = "krn" ":" "asset-type" "/" asset-type

asset-type  = NAME
```

**Examples**

```
krn:asset-type/beam-pump
```

## Control Change

```abnf
control-change-krn = "krn" ":" "control-change" ":" control-change-id

control-change-id  = UUID
```

**Examples**

```
krn:control-change:86a425b4-b43f-4989-a38f-b18f6b3d1ec7
```

## Data Stream

```abnf
datastream-krn = "krn" ":" "datastream" ":" datastream

datastream  = NAME
```

**SDK Example**

```python linenums="1"
from kelvin.krn import KRNDatastream

KRNDatastream(datastream="temp-setpoint")
```

**Examples**

```
krn:datastream:temp-setpoint
krn:datastream:casing.temperature
krn:datastream:oee
```


## Data Quality - Asset Data Stream

```abnf
dqad-krn = "krn" ":" "dqad" ":" data-quality ":" asset "/" datastream

asset        = NAME
datastream   = NAME
data-quality = NAME
```

**SDK Example**

```python linenums="1"
from kelvin.krn import KRNAssetDataStreamDataQuality

KRNAssetDataStreamDataQuality(asset="pcp_01",data_stream="gas_flow",data_quality="kelvin_timestamp_anomaly")
```

**Examples**

```
krn:dqad:kelvin_timestamp_anomaly:pcp_01/gas_flow 
krn:dqad:kelvin_out_of_range_detection:pcp_01/gas_flow
```


## Data Quality - Asset

```abnf
dqasset-krn = "krn" ":" "dqasset" ":" data-quality ":" asset

asset        = NAME
data-quality = NAME
```

**SDK Example**

```python linenums="1"
from kelvin.krn import KRNAssetDataQuality

KRNAssetDataQuality(asset="pcp01",data_quality="asset_score")
```

**Examples**

```
krn:dqasset:asset_score:pcp01
```


## Job

```abnf
job-krn = "krn" ":" "job" ":" job "/" job-run-id

job = NAME
job-run-id = 1*(DIGIT / ALPHA / "_" / "-")
```

**Examples**

**SDK Example**

```python linenums="1"
from kelvin.krn import KRNJob

KRNJob(job="parameters-schedule-worker",job_run_id="1257897347822083")
```

```
krn:job:parameters-schedule-worker/1257897347822083
```


## Recommendation

```abnf
recommendation-krn = "krn" ":" "recommendation" ":" recommendation-id

recommendation-id  = UUID
```

**SDK Example**

```python linenums="1"
from kelvin.krn import KRNRecommendation

KRNRecommendation(recommendation_id="86a425b4-b43f-4989-a38f-b18f6b3d1ec7")
```

**Examples**

```
krn:recommendation:86a425b4-b43f-4989-a38f-b18f6b3d1ec7
```


## Schedule

```abnf
schedule-krn = "krn" ":" "schedule" ":" schedule

schedule = USERNAME
```

**SDK Example**

```python linenums="1"
from kelvin.krn import KRNSchedule

KRNSchedule(schedule="6830a7d3-bcf3-4a64-8126-eaaeeca86676")
```

**Examples**

```
krn:schedule:6830a7d3-bcf3-4a64-8126-eaaeeca86676
```


## Service Account

```abnf
srv-acc-krn = "krn" ":" "srv-acc" ":" account-name

account-name = USERNAME
```

**SDK Example**

```python linenums="1"
from kelvin.krn import KRNServiceAccount

KRNServiceAccount(service_account="node-client-my-edge-cluster")
```

**Examples**

```
krn:srv-acc:node-client-my-edge-cluster
```


## System

```abnf
system-krn = "krn" ":" "system" ":" system_name

system_name = NAME-V2
```

**Examples**

```
krn:system:kelvin
```


## User

```abnf
user-krn = "krn" ":" "user" ":" user

user  = USERNAME
```

**SDK Example**

```python linenums="1"
from kelvin.krn import KRNUser

KRNUser(user="me@example.com")
```

**Examples**

```
krn:user:me@example.com
```

## Workload

```abnf
wl-krn = "krn" ":" "wl" ":" cluster "/" workload

cluster  = DNS-SAFE
workload = DNS-SAFE
```

**SDK Example**

```python linenums="1"
from kelvin.krn import KRNWorkload

KRNWorkload(node="my-node",workload="temp-adjuster-1")
```

**Examples**

```
krn:wl:my-node/temp-adjuster-1
```


## Workload App Version

```abnf
wlappv-krn = "krn" ":" "wlappv" ":" wl-krn ":" appversion-krn
```

**SDK Example**

```python linenums="1"
from kelvin.krn import KRNWorkloadAppVersion

KRNWorkloadAppVersion(node="my-node",workload="pvc-r312",app="pvc",version="1.0.0")
```

**Examples**

```
krn:wlappv:cluster_name/workload_name:app_name/app_version
krn:wlappv:my-node/pvc-r312:pvc/1.0.0
```


# Common Components

See [Kelvin Platform
Regex](https://docs.google.com/spreadsheets/d/1kOG7G6oz8PirKhCsljeHQe2xX96gV2kdUogmGxlnRG4/edit#gid=0)
for the complete and authoritative document.

| Component     | Regex
|---            | ---
| DNS-SAFE-NAME | `^[a-z]([-a-z0-9]*[a-z0-9])?$`
| NAME          | `^[a-z0-9]([-_.a-z0-9]*[a-z0-9])?$`
| NAME-V2       | `^[a-zA-Z0-9]([-_ .a-zA-Z0-9]*[a-zA-Z0-9])?$`
| SEMVER        | See [Semantic Versioning](https://semver.org/)
| USERNAME      | Probably limited by the URN spec, so `([-a-zA-Z0-9()+,.:=@;$_!*'&~\/]|%[0-9a-f]{2})+`
| UUID          | `^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$`