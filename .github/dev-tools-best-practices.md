Title: Best Practices for Kelvin App Developers
Source: https://docs.kelvin.ai/6.3/developer-tools/how-to/develop/best-practices/
Fetched: 2025-10-27

Detailed Summary :
This page outlines recommended design, deployment and operational practices for developing Kelvin SmartApps. The guidance spans software design (asynchronous programming and event-driven patterns), logging, deployment sizing, secrets management, and resource considerations for workloads. The recommendations emphasize building scalable, maintainable, and safe SmartApps even in pilot stages.

Software design
- Asynchronous Code: Prefer coroutines and `asyncio` to write non-blocking code for I/O-bound work. The page includes an example that runs multiple short coroutines concurrently to demonstrate reduced wall time versus sequential execution.
- Subscription vs Polling: Use subscription-based connectors (e.g., OPC-UA, MQTT) where available rather than polling (e.g., Modbus) to reduce load and enable event-driven workflows.
- Event-Driven Design: Use queues, select-like constructs, or stream handlers to react to new data rather than polling on a fixed schedule. This saves compute and leads to more responsive apps.

Operational patterns
- Logging: Implement structured logging with severity levels (DEBUG, INFO, WARNING, ERROR, CRITICAL). Expose logging level as a Kelvin Asset Parameter so operators can dynamically adjust verbosity via the UI.
- Open vs Closed Loop Control: Use Kelvin Recommendations to present control changes either as open-loop (user must accept) or closed-loop (auto-applied). Combine with App Parameters to let users switch modes safely.

Deployments
- Workload Resources: Configure Requests (reservation) and Limits (cap) for CPU and memory. Use cluster and workload telemetry to tune these values.
- Requests vs Limits: Requests affect scheduling; limits prevent a workload from using excessive resources. CPU is compressible; memory exhaustion is often fatal.
- Asset to Workload Assignment: Reuse a single workload for many assets when appropriate to reduce overhead. The app receives asset assignments and should handle assets sequentially or in parallel as needed.

Secrets
- Use Kelvin's secret management to store credentials (API keys, passwords). Secrets are injected via tokens at deployment time; values cannot be read back, only replaced or deleted. Prefer secrets over embedding credentials in code or plain configuration.

Key examples :
The page contains a short asyncio example demonstrating three coroutines running concurrently and timing output to show combined vs wall time. Reconstructed example (conceptual):

```python
import asyncio
import time

async def dwell(duration=1.0):
    await asyncio.sleep(duration)
    return duration

async def main():
    start_time = time.time()
    times = await asyncio.gather(*(dwell() for _ in range(3)))
    print(f"Tasks total time: {sum(times):.1f}")
    print(f"Wall time: {time.time() - start_time:.1f}")

asyncio.run(main())
```

Notes:
- Prefer non-blocking I/O and `asyncio` patterns in SmartApps to avoid blocking the event loop and degrading throughput.
- Where connectors support subscription (OPC-UA, MQTT), prefer them over polling to reduce load and latency.
- Expose operational knobs (log level, closed-loop toggle) as App or Asset Parameters to allow runtime control via the UI.
- Tune Requests and Limits based on telemetry; consider grouping multiple assets into a single workload for efficiency.
- Always use Kelvin secret management for sensitive credentials and avoid storing secrets in repo or images.
