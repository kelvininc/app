# Asset

## What is an Asset?

An **Asset** in Kelvin denotes a digital representation of a physical or virtual equipment. Each asset is characterized by a set of properties that detail its attributes and by datastreams, which are channels of continuous or time-stamped data related to the asset's operation or state. Through these properties and datastreams, Kelvin enables users to closely monitor, simulate, and analyze the performance of the asset. 

In most cases your assets will be located where your machinery is located. They will be connected to Kelvin through a gateway device (Cluster) that will be responsible for collecting data from the asset and sending it to Kelvin. 

![](../../assets/asset-overview.jpg)

## Asset & Associated Data Streams

An asset represents any entity in an industrial environment that you wish to monitor or derive data from.

* **Physical Assets**: These are tangible pieces of equipment or systems present in the field. Examples include pumps, motors, sensors, and other machinery.

* **Virtual Assets**: These are intangible or software-defined entities that might represent processes, aggregated data points, or virtual representations of physical systems. For instance, a "virtual asset" could be a software representation of an entire production line, combining data from multiple physical sensors and devices.

Each Asset is linked to one or more **Data Streams**. 

A **Data Stream** in Kelvin refers to a continuous flow of data related to a specific aspect of an Asset. It captures and channels time-stamped or real-time information, enabling users to monitor, analyze, and derive insights from the Asset's behavior, performance, and state. Data Streams are obtained from sensors, meters, historians, DCS, PLC and other data sources (like Kelvin SmartApps™ or APIs). 

![](../../assets/data-stream-details.jpg)

**For example:**

* **Pump (Asset):**
    * _Temperature (Data Stream)_: This stream monitors the operating temperature of the pump, capturing data in real-time or at set intervals.
    * _Pressure (Data Stream)_: This stream measures the pressure of the fluid being pumped, again possibly in real-time or at defined intervals.
* **Motor (Asset):**
    * _Temperature (Data Stream)_: Monitors the operating temperature of the motor.
    * _Speed (Data Stream)_: Captures data on the RPM speed at which the motor is running.
* **Production Process (Virtual Asset):**
    * _Efficiency (Data Stream)_: This could be a virtual data stream that calculates efficiency by combining real-time data from multiple sensors or devices on a production line.

Every piece of data that is recorded is specifically associated with an Asset and a Data Stream. This pair ensures that there's a clear traceability and context for each data point.

For example, if a temperature reading of 75°C is recorded at a certain timestamp, it would be associated with a specific motor (Asset) and its temperature monitoring (Data Stream). This provides clarity on what the data represents and where it originated.

By defining data collection in terms of Assets and Data Streams, organizations can achieve a structured and organized approach to monitoring and analyzing their industrial environments, whether dealing with physical machinery or virtual representations of processes. It ensures that data is not only collected but is meaningful, contextual, and can be used for informed decision-making, predictive maintenance, and other data-driven Kelvin SmartApps™.

---

## Reference

Field                | Description
---------------------|------------------------------------------
Name                 | Unique name identifier. It must contain only lowercase alphanumeric characters. The characters `.`, `_` and `-` are allowed to separate words instead of a space BUT can not be at the beginning or end of the name.
Title                | The display name to show on the Kelvin UI. It can contain any characters, including spaces.
Asset Type           | The name of the Asset Type that this Asset belongs to. This must be a valid Asset Type name.
Properties           | A list of key/value pairs that define custom properties of the asset. Use this to define attributes like: Location, Site, PLC Type, Manufacturer, Serial Number, etc.
Entity Type          | **Deprecated**. Entity type should always be `asset`.
Parent Name          | **Deprecated**. Parent should always be `null`.
Hierarchy            | **Deprecated**. Hierarchy should always be an empty list `[]`.

### Name
The unique name of the asset. It must contain only lowercase alphanumeric characters. 

The characters `.`, `_` and `-` are allowed to separate words instead of a space BUT can not be at the beginning or end of the name.

The maximum length is 64 characters.

### Title
The display name of the asset. It can contain any characters, including spaces. 

This is used to identify the data stream in the Kelvin UI.

The maximum length is 64 characters.

### Asset Type
An Asset Type refers to a specific categorization or classification of assets based on shared characteristics or functionalities. Asset Types are typically used to organize, manage, and track assets in a systematic manner, especially in industries where a variety of assets are employed for different purposes. 

You need to create an Asset Type before you can create an Asset.

**Examples of Asset Types:**

| Asset Type |
|------------|
| Beam Pump  |
| Plunger Lift |
| Electrical Submersible Pump | 
| Progressing Cavity Pump |

### Properties
A list of key/value pairs that define custom properties of the asset. Use these properties to enrich the asset with additional information that can be used to filter assets in the Kelvin UI.

You can define any number of properties for an asset.

**Examples of Properties:**

Property Name | Property Value
--------------|----------------
Location      | Texas
Site          | Houston
PLC Type      | Allen Bradley
Manufacturer  | GE
Serial Number | 123456789

# Data Stream

## What is a Data Stream?

A **Data Stream** is a single piece of data being recorded from either an Asset or calculated from Kelvin SmartApps™. It is stored in the time series database in the Kelvin API.

![](../../assets/data-stream-overview.jpg)

Usually one Asset will have multiple data streams being recorded.

!!! info ""

    When setting up your Data Streams, it is important you plan your naming strategy properly before starting, to ensure you can easily filter and find your wanted data quickly.

## Data Stream and Assets

You can get a good overview of Asset / Data Stream pair concept in this introduction video;

<iframe width="800" height="450" src="https://www.youtube.com/embed/WNgqd25TQig?si=XkYvEtNm81gpTLJl" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

A Data Stream is linked to one or more Assets, signifying the flow of specific metric data related to that asset. Together, they provide a continuous or periodic record of key parameters indicative of an asset's performance, health, or status.

![](../../assets/data-stream-details.jpg)

**For example:**

* **Pump (Asset):**
    * _Temperature (Data Stream)_: This stream monitors the operating temperature of the pump, capturing data in real-time or at set intervals.
    * _Pressure (Data Stream)_: This stream measures the pressure of the fluid being pumped, again possibly in real-time or at defined intervals.
* **Motor (Asset):**
    * _Temperature (Data Stream)_: Monitors the operating temperature of the motor.
    * _Speed (Data Stream)_: Captures data on the RPM speed at which the motor is running.
* **Production Process (Virtual Asset):**
    * _Efficiency (Data Stream)_: This could be a virtual data stream that calculates efficiency by combining real-time data from multiple sensors or devices on a production line.

Every piece of data that is recorded is specifically associated with an Asset and a Data Stream. This pair ensures that there's a clear traceability and context for each data point.

For example, if a temperature reading of 75°C is recorded at a certain timestamp, it would be associated with a specific motor (Asset) and its temperature monitoring (Data Stream). This provides clarity on what the data represents and where it originated.

By defining data collection in terms of Assets and Data Streams, organizations can achieve a structured and organized approach to monitoring and analyzing their industrial environments, whether dealing with physical machinery or virtual representations of processes. It ensures that data is not only collected but is meaningful, contextual, and can be used for informed decision-making, predictive maintenance, and other data-driven applications.

---

## Reference

Field                | Description
---------------------|------------------------------------------
Name                 | Unique name identifier. It must contain only lowercase alphanumeric characters. The characters `.`, `_` and `-` are allowed to separate words instead of a space BUT can not be at the beginning or end of the name.
Title                | The display name to show on the Kelvin UI. It can contain any characters, including spaces.
Type                 | Determines if the data is directly derived from sensors or is processed/calculated. Allowed values: **Measurement** or **Computed**.
Semantic Type        | Provides context or deeper meaning behind the data, beyond just its format or structure. Check Kelvin API for the full list of available semantic types.
Data Type            | Specifies the kind of data in the stream. Allowed values: **Boolean**, **Number**, **Object**, **String**.
Unit                 | Defines the measurement unit for data. Check Kelvin API for the full list of available units.
Description          | Optional description for the data stream, up to 200 characters.


### Name
The unique name of the data stream. It must contain only lowercase alphanumeric characters. 

The characters `.`, `_` and `-` are allowed to separate words instead of a space BUT can not be at the beginning or end of the name.

The maximum length is 64 characters.

### Title
The display name of the data stream. It can contain any characters, including spaces. 

This is used to identify the data stream in the Kelvin UI.

The maximum length is 64 characters.

### Type 
There are two types of data streams:

* **Measurement:** These represent direct data values derived from sensors or PLCs associated with physical assets at the edge. They are typically acquired using a Connection, utilizing industrial protocols.
* **Computed:** These pertain to data values that have been processed or calculated. Often, these are gathered via a Kelvin SmartApp™, where computations, algorithms, or machine learning models generate new data insights.

### Semantic Type
A semantic type for a data stream pertains to the deeper meaning or context behind the data being transmitted or processed. Unlike syntactic types, which primarily concern the format or structure of data (e.g., number, string, boolean), semantic types give insights into the nature, purpose, or origin of the data.

For instance, in an industrial setting, a data stream might be syntactically classified as a series of floating-point numbers. However, its semantic type could further define it as "Temperature" or "Pressure".

!!! info ""

	This is a non-exhaustive list shown to give you an idea of the options available. You can check the full list using the Kelvin API. You can also create your own Semantic Types through the Kelvin API.

Semantic Type Name | Semantic Type
-------------------|--------------------------
acceleration | Acceleration
angle | Angle
angular_acceleration | Angular Acceleration
angular_velocity | Angular Velocity
area | Area
capacitance | Capacitance
current | Current
data_rate | Data Rate
data_size | Data Size
density | Density
distance | Distance
electric_charge | Electric Charge
energy | Energy
force | Force
frequency | Frequency
humidity | Humidity
illuminance | Illuminance
inductance | Inductance
latitude | Latitude
length | Length
longitude | Longitude
luminance | Luminance
luminosity | Luminosity
luminous_flux | Luminous Flux
luminous_intensity | Luminous Intensity
magnetic_flux | Magnetic Flux
magnetic_induction | Magnetic Induction
mass | Mass
mass_flow_rate | Mass Flow Rate
power | Power
pressure | Pressure
relative_humidity | Relative Humidity
resistance | Resistance
sound_pressure | Sound Pressure
state | State
temperature | Temperature
thrust | Thrust
timespan | TimeSpan
torque | Torque
velocity | Velocity
voltage | Voltage
volume | Volume
volume_flow_rate | Volume Flow Rate



### Data Type

It's essential to choose the appropriate Data Type that matches the kind of data you expect to receive.

!!! info ""

	Some Semantic Types are predefined and will automatically determine the Data Type for you. For instance, if you choose "Pressure" as the semantic type, the system will automatically set the data type to Number. In contrast, the "State" semantic type offers more flexibility and can be a Boolean, Number, or String. In such cases, you'll need to manually select the correct Data Type.


Below are the available primitive data types with brief descriptions and their respective ranges:

Option  | Declaration Name | Description                                                            
------- | ----------|------------------------------------------------------------ 
Boolean | `boolean` | Represents a binary state, either True or False                        
Number  | `number`  | Uses a double precision floating point format.	                     
String  | `string`  | Variable-length text.	                                                 
Object  | Any word  | This is unique because the word object is not explicitly used. Instead, an object is first defined in ui_schemas, and its filename serves as its identifier.</p> For example, you can use the word `dynacard` which you can define in ui_schemas/io_configuration/, corresponding to the file schemas/io_configuration/dynacard.json.

Ensure that you pick the type that best aligns with the data you anticipate receiving to maintain data integrity and optimize processing.

### Unit
This option is only available if the Data Type is **Number**.

!!! info ""

    You can check the full list of units available for your instance through the Kelvin API. You can also create your own units through the Kelvin API.


| Unit Name                  | Unit                              | Symbol       |
|----------------------------|-----------------------------------|--------------|
| acre | Acre | ac |
| ampere | Ampere | A |
| astronomical_unit | Astronomical Unit | au |
| bar | Bar | bar |
| bel | Bel | B |
| bit | Bit | Bit |
| bit_per_second | Bit per Second | bps |
| byte | Byte | Byte |
| byte_per_second | Byte per Second | B/s |
| candela | Candela | cd |
| candela_per_square_metre | Candela per Square Metre | cd/m² |
| centimetre | Centimetre | cm |
| centimetre_per_second | Centimetre per Second | cm/s |
| centimetre_per_second_squared | Centimetre per Second Squared | cm/s² |
| coulomb | Coulomb | C |
| cubic_centimetre | Cubic Centimetre | cm³ |
| cubic_foot | Cubic Foot | ft³ |
| cubic_inch | Cubic Inch | in³ |
| cubic_metre | Cubic Metre | m³ |
| day | Day | d |
| decibel | Decibel | dB |
| degree_celsius | Degree Celsius | °C |
| degree_fahrenheit | Degree Fahrenheit | °F |
| degree_of_arc | Degree of Arc | ° |
| degree_per_second | Degree per Second | °/s |
| electronvolt | Electronvolt | eV |
| exbibit | Exbibit | Eibit |
| exbibit_per_second | Exbibit per Second | Eibit/s |
| exbibyte | Exbibyte | EiB |
| exbibyte_per_second | Exbibyte per Second | EiB/s |
| farad | Farad | F |
| fluid_ounce | Fluid Ounce | fl oz |
| foot | Foot | ft |
| footcandle | Footcandle | fc |
| g_force | G-Force | g |
| gallon | Gallon | gal |
| gibibit | Gibibit | Gibit |
| gibibit_per_second | Gibibit per Second | Gibit/s |
| gibibyte | Gibibyte | GiB |
| gibibyte_per_second | Gibibyte per Second | GiB/s |
| gigahertz | Gigahertz | GHz |
| gigajoule | Gigajoule | GJ |
| gigawatt | Gigawatt | GW |
| gram | Gram | g |
| gram_per_cubic_metre | Gram per Cubic Metre | g/m³ |
| gram_per_hour | Gram per Hour | g/h |
| gram_per_second | Gram per Second | g/s |
| hectare | Hectare | ha |
| henry | Henry | H |
| hertz | Hertz | Hz |
| horsepower | Horsepower | hp |
| hour | Hour | h |
| inch | Inch | in |
| inches_of_mercury | Inches of Mercury | inHg |
| inches_of_water | Inches of Water | inH2O |
| joule | Joule | J |
| kelvin | Kelvin | K |
| kibibit | Kibibit | Kibit |
| kibibit_per_second | Kibibit per Second | Kibit/s |
| kibibyte | Kibibyte | KiB |
| kibibyte_per_second | Kibibyte per Second | KiB/s |
| kilogram | Kilogram | kg |
| kilogram_per_cubic_metre | Kilogram per Cubic Metre | kg/m³ |
| kilogram_per_hour | Kilogram per Hour | kg/h |
| kilogram_per_second | Kilogram per Second | kg/s |
| kilohertz | Kilohertz | kHz |
| kilojoule | Kilojoule | kJ |
| kilometre | Kilometre | km |
| kilometre_per_hour | Kilometre per Hour | km/h |
| kilometre_per_second | Kilometre per Second | km/s |
| kiloohm | Kiloohm | kΩ |
| kilopascal | Kilopascal | kPa |
| kilovolt | Kilovolt | kV |
| kilowatt | Kilowatt | kW |
| kilowatt_hour | Kilowatt Hour | kWh |
| kilowatt_hour_per_year | Kilowatt Hour per Year | kWh/yr |
| knot | Knot | kt |
| litre | Litre | L |
| litre_per_hour | Litre per Hour | L/h |
| litre_per_second | Litre per Second | L/s |
| lumen | Lumen | lm |
| lux | Lux | lx |
| maxwell | Maxwell | Mx |
| mebibit | Mebibit | Mibit |
| mebibit_per_second | Mebibit per Second | Mibit/s |
| mebibyte | Mebibyte | MiB |
| mebibyte_per_second | Mebibyte per Second | MiB/s |
| megaelectronvolt | Megaelectronvolt | MeV |
| megahertz | Megahertz | MHz |
| megajoule | Megajoule | MJ |
| megaohm | Megaohm | MΩ |
| megavolt | Megavolt | MV |
| megawatt | Megawatt | MW |
| metre | Metre | m |
| metre_per_hour | Metre per Hour | m/h |
| metre_per_second | Metre per Second | m/s |
| metre_per_second_squared | Metre per Second Squared | m/s² |
| microampere | Microampere | μA |
| microfarad | Microfarad | μF |
| microgram | Microgram | μg |
| microhenry | Microhenry | μH |
| micrometre | Micrometre | μm |
| microsecond | Microsecond | μs |
| microvolt | Microvolt | μV |
| microwatt | Microwatt | μW |
| mile | Mile | mi |
| mile_per_hour | Mile per Hour | mi/h |
| mile_per_second | Mile per Second | mi/s |
| milliampere | Milliampere | mA |
| millibar | Millibar | mbar |
| millifarad | Millifarad | mF |
| milligram | Milligram | mg |
| millihenry | Millihenry | mH |
| millilitre | Millilitre | mL |
| millilitre_per_hour | Millilitre per Hour | mL/h |
| millilitre_per_second | Millilitre per Second | mL/s |
| millimetre | Millimetre | mm |
| millimetres_of_mercury | Millimetres of Mercury | mmHg |
| milliohm | Milliohm | mΩ |
| millisecond | Millisecond | ms |
| millivolt | Millivolt | mV |
| milliwatt | Milliwatt | mW |
| minute | Minute | min |
| nanofarad | Nanofarad | nF |
| nanometre | Nanometre | nm |
| nanosecond | Nanosecond | ns |
| nautical_mile | Nautical Mile | nmi |
| newton | Newton | N |
| newton_metre | Newton Metre | N·m |
| NULL | NULL | NULL |
| ohm | Ohm | Ω |
| ounce | Ounce | ozf |
| pascal | Pascal | Pa |
| percent | Percent | % |
| picofarad | Picofarad | pF |
| pound | Pound | lbf |
| pound_per_square_inch | Pound per Square Inch | psi |
| radian | Radian | rad |
| radian_per_second | Radian per Second | rad/s |
| radian_per_second_squared | Radian per Second Squared | rad/s² |
| revolution_per_minute | Revolution per Minute | rpm |
| revolution_per_second | Revolution per Second | rps |
| second | Second | s |
| second_of_arc | Second of Arc | ' |
| slug | Slug | slug |
| square_centimetre | Square Centimetre | cm² |
| square_foot | Square Foot | ft² |
| square_inch | Square Inch | in² |
| square_kilometre | Square Kilometre | km² |
| square_metre | Square Metre | m² |
| square_millimetre | Square Millimetre | mm² |
| tebibit | Tebibit | Tibit |
| tebibit_per_second | Tebibit per Second | Tibit/s |
| tebibyte | Tebibyte | TiB |
| tebibyte_per_second | Tebibyte per Second | TiB/s |
| tesla | Tesla | T |
| ton | Ton | ton |
| tonne | Tonne | t |
| turn | Turn | rev |
| volt | Volt | V |
| watt | Watt | W |
| weber | Weber | Wb |
| year | Year | yr |
| yobibit | Yobibit | Yibit |
| yobibit_per_second | Yobibit per Second | Yibit/s |
| yobibyte | Yobibyte | YiB |
| yobibyte_per_second | Yobibyte per Second | YiB/s |
| zebibit | Zebibit | Zibit |
| zebibit_per_second | Zebibit per Second | Zibit/s |
| zebibyte | Zebibyte | ZiB |
| zebibyte_per_second | Zebibyte per Second | ZiB/s |

### Description
You can also optionally add a description to the data stream. 

The maximum length is 200 characters.

# Kelvin Resource Name Registry

_On this page you will go through understanding the Kelvin Resource Name Registry and the definitions available for use._

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

* [Kelvin SmartApps™ (`app`)](#kelvin-smartappstm)
* [Kelvin SmartApps™ Version (`appversion`)](#kelvin-smartappstm-version)
* [Asset (`asset`)](#asset)
* [Asset Data Stream (`ad`)](#asset-data-stream)
* [App Parameter (`ap`)](#asset-parameter)
* [Data Stream(`datastream`)](#data-stream)
* [Parameter (`param`)](#parameter)
* [Recommendation (`recommendation`)](#recommendation)
* [Service Account (`srv-acc`)](#service-account)
* [User (`user`)](#user)
* [Workload (`wl`)](#workload)
* [Workload App Version(`wlappv`)](#workload-app-version)
* [Schedule (`schedule`)](#schedule)
* [Job (`job`)](#job)


### Kelvin SmartApps™

```abnf title="Kelvin Resource Name" linenums="1"
app-krn = "krn" ":" "app" ":" app

app     = NAME
```

**Examples**

```abnf title="Kelvin Resource Name Example" linenums="1"
krn:app:smart-pcp
krn:app:pvc
```

### Kelvin SmartApps™ Version

```abnf title="Kelvin Resource Name" linenums="1"
appversion-krn = "krn" ":" "appversion" ":" app "/" version

app     = NAME
version = NAME
```

**Examples**

```abnf title="Kelvin Resource Name Example" linenums="1"
krn:appversion:smart-pcp/2.0.0
krn:appversion:pvc/3.0.1
```


### Asset

```abnf title="Kelvin Resource Name" linenums="1"
asset-krn = "krn" ":" "asset" ":" asset

asset  = NAME
```

**Examples**

```abnf title="Kelvin Resource Name Example" linenums="1"
krn:asset:air-conditioner-1
krn:asset:beam-pump
```


### Asset Data Stream

```abnf title="Kelvin Resource Name" linenums="1"
ad-krn = "krn" ":" "ad" ":" asset "/" datastream

asset       = NAME
datastream = NAME
```

**Examples**

```abnf title="Kelvin Resource Name Example" linenums="1"
krn:ad:air-conditioner-1/temp-setpoint
krn:ad:beam-pump/casing.temperature
krn:ad:centrifugal-pump-02/oee
krn:ad:centrifugal-pump-02/failure_quotient
```


### App Parameter
```abnf title="Kelvin Resource Name" linenums="1"
ap-krn = "krn" ":" "ap" ":" asset "/" parameter

asset  = NAME
parameter = NAME
```

**Examples**

```abnf title="Kelvin Resource Name Example" linenums="1"
krn:ap:air-conditioner-1/closed_loop
```


### Data Stream

```abnf title="Kelvin Resource Name" linenums="1"
datastream-krn = "krn" ":" "datastream" ":" datastream

datastream  = NAME
```

**Examples**

```abnf title="Kelvin Resource Name Example" linenums="1"
krn:datastream:temp-setpoint
krn:datastream:casing.temperature
krn:datastream:oee
```


### Parameter
```abnf title="Kelvin Resource Name" linenums="1"
param-krn = "krn" ":" "param" ":" parameter

parameter = NAME
```

**Examples**

```abnf title="Kelvin Resource Name" linenums="1"
krn:param:configuration.ip
```


### Recommendation

```abnf title="Kelvin Resource Name" linenums="1"
recommendation-krn = "krn" ":" "recommendation" ":" recommendation-id

recommendation-id  = UUID
```

**Examples**

```abnf title="Kelvin Resource Name Example" linenums="1"
krn:recommendation:86a425b4-b43f-4989-a38f-b18f6b3d1ec7
```


### Service Account

```abnf title="Kelvin Resource Name" linenums="1"
srv-acc-krn = "krn" ":" "srv-acc" ":" account-name

account-name = USERNAME
```

**Examples**

```abnf title="Kelvin Resource Name Example" linenums="1"
krn:srv-acc:node-client-my-edge-cluster
```


### User

```abnf title="Kelvin Resource Name" linenums="1"
user-krn = "krn" ":" "user" ":" user

user  = USERNAME
```

**Examples**

```abnf title="Kelvin Resource Name Example" linenums="1"
krn:user:me@example.com
```

### Workload

```abnf title="Kelvin Resource Name" linenums="1"
wl-krn = "krn" ":" "wl" ":" cluster "/" workload

cluster  = DNS-SAFE
workload = DNS-SAFE
```

**Examples**

```abnf title="Kelvin Resource Name Example" linenums="1"
krn:wl:my-node/temp-adjuster-1
```


### Workload App Version

```abnf title="Kelvin Resource Name" linenums="1"
wlappv-krn = "krn" ":" "wlappv" ":" wl-krn ":" appversion-krn
```

**Examples**

```
krn:wlappv:cluster_name/workload_name:app_name/app_version
krn:wlappv:my-node/pvc-r312:pvc/1.0.0
```


### Schedule

```abnf title="Kelvin Resource Name" linenums="1"
schedule-krn = "krn" ":" "schedule" ":" schedule

schedule = USERNAME
```

**Examples**

```abnf title="Kelvin Resource Name Example" linenums="1"
krn:schedule:6830a7d3-bcf3-4a64-8126-eaaeeca86676
```

### Job

```
job-krn = "krn" ":" "job" ":" job "/" job-run-id

job = NAME
job-run-id = 1*(DIGIT / ALPHA / "_" / "-")
```

**Examples**

```abnf title="Kelvin Resource Name Example" linenums="1"
krn:job:parameters-schedule-worker/1257897347822083
```
