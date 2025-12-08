# Best Practices for Kelvin App Developers

When starting to develop applications for the Kelvin platform, it is important even in the pilot project stage to structure your program and environment correctly.

By following these best practices, you will be able to easily scale your applications while maintaining cost-effective infrastructure and maintenance routines.

# Software Design

## Asynchronous Code

Programs can leverage concurrency in many ways, the easiest of which may be utilizing [coroutines](https://docs.python.org/3/library/asyncio-task.html) and [asyncio](https://docs.python.org/3/library/asyncio.html). These allow portions of code to be written as asynchronous routines which Python will execute through a form of cooperative multitasking. This allows code, especially that which typically waits such as I/O-bound operations, to effectively execute in parallel thereby making the most efficient use of processor time.

Here is an example of an asynchronous program demonstrating three routines which are run in parallel, each for 1 second, but with total execution time of only 1 second:

```python title="Asynchronous Code" linenums="1"
import asyncio
import time

async def dwell(duration=1.0):
    await asyncio.sleep(duration)
    return duration

async def main():
    return await asyncio.gather(*[dwell() for _ in range(3)])


start_time = time.time()
times = asyncio.run(main())

print(f"Tasks total time: {sum(times):.1f}")
print(f"Wall time: {time.time() - start_time:.1f}")
```

> Combined time: 3.0
> Wall time: 1.0

## Subscription vs Polling

Some protocols such as OPC-UA can be configured for subscription-based readings which are much more efficient than polling mechanisms. With a subscription, a one-time request for values from the endpoint will result in values being published to the application only when they change. This reduces loan on both systems and facilitates an event-driven design where an application can respond to only those changes.

Some Kelvin Connectors such as OPC-UA and MQTT offer subscription-based readings whereas some like Modbus only support polling.

## Event-Driven Design

Rather than running a process or function at a regular interval which might waste processing on unchanged readings, for instance, applications should use features such as queues or `socket.select()` to execute code when new data is available.

An example of this is an application watching for new datastream readings and performing processing upon receipt of a new metric value.

## Logging

Implementing logging within an application can greatly improve the application testing process as well as facilitate troubleshooting when there is an issue. Especially when implemented using available severity levels (DEBUG, INFO, WARNING, ERROR, CRITICAL), thorough log messages can help a developer or engineer find and focus on the information that is pertinent.

Logging verbosity can be adjusted, even at run-time, using a Kelvin Asset Parameter. An application designer can include a custom Asset Parameter with, say, multiple log levels pre-defined. When a user changes the parameter in the UI, it is synchronized to the application which can respond and adjust the log level accordingly.

## Open vs Closed Loop Control

Kelvin Recommendations are used by an application to suggest control changes and other outputs which are applied to a system. Recommendations can be open-loop where a user is required to accept the changes in the UI, or they can be closed-loop with the changes being automatically applied. When combined with a Kelvin Asset Parameter to control the mode of operation, applications can afford the user the ability to selectively decide when to have recommendations applied automatically based on e.g. operating conditions or trust in the application’s performance.

# Deployments

## [Workload Resources](https://docs.kelvin.ai/latest/developer-tools/how-to/deploy/set-cpu-and-memory-limits/)

Workloads are run within a container with separate compute resources, CPU and memory, allocated to each container. How much of each resource is reserved or restricted for a given application is determined by the Requests and Limits respectively, which can be defined for each application.

Proper adjustment of these settings can provide safeguards for application operation while optimizing the number of workloads deployed to a machine. [Cluster Telemetry](https://docs.kelvin.ai/latest/platform-administration/how-to/cluster/#cluster-telemetry) and [Workload Telemetry](https://docs.kelvin.ai/latest/developer-tools/how-to/monitor/#telemetry) can be used to profile the resource performance of the cluster and application, respectively, in order to apply the optimal settings.

### Requests

A resource request is a reservation of that resource within the cluster and is used by the system for allocating workloads to available cluster nodes. When a resource for a node has been fully reserved, no additional workloads can be allocated to that node. 

### Limits

A resource limit is a restriction on how much of a node’s resource is available to a workload. A resource for a node is allowed to be over-allocated with respect to the total limits from all workloads but, in the case that actual available resources are exhausted, workloads will be subject to repercussions which depend on the resource type.

### Memory

Memory is a finite resource available on the machine that runs containers. When it is exhausted for an application, the application is likely to experience unrecoverable errors unless it was purposefully built to handle that scenario through optimistic allocation.

### CPU

CPU, or processor, is a “compressible” resource in that it can never truly be exhausted. The multitasking performed by the OS will always yield some time for an application to execute with a potential penalty in performance if the processor is fully utilized.

## [Asset to Workload Assignment](https://docs.kelvin.ai/latest/developer-tools/how-to/deploy/planner-application/)

It is very easy to write a program that handles data from an asset and then deploy this as a workload. But, because compute resources are associated to each workload, scaling an application to many assets can dramatically increase the processor and memory requirements of the solution.

Kelvin allows multiple assets to be deployed to a single workload which reduces resource requirements by allowing one application to handle data and processing for many assets without the overhead of individual workloads. The application is made aware of the assets that it are assigned to it, and it is free to determine how best to handle them. This can allow an application to process assets in sequence or in parallel, or to avoid processing an asset altogether if it is not in an appropriate state.

## [Secrets](https://docs.kelvin.ai/latest/developer-tools/how-to/develop/secrets/)

While not a performance consideration, the usage of Kelvin’s secret management system can facilitate a more secure deployment for an application. Examples of secrets are an API authentication key for AWS or a password used to connect to an MQTT server. Once created, a secret can only be replaced or deleted but cannot be viewed by any users.

Secrets are defined globally in the cloud environment and then embedded into an application’s configuration using tokens. When deployed, the token is replaced by the system with the actual value where an application can utilize it at run-time.







