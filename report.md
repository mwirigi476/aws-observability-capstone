# Capstone Project Report: Observability-as-a-Service
**System Deployment Verification Audit**

## 1. Observability Architectural Overview
This framework deploys an automated multi-tier telemetry and self-healing engine to maintain low-latency response thresholds for users in Kenya. 
*   **Web Tier Monitoring**: An Amazon Linux 2023 host running the CloudWatch Agent tracking system memory, root storage utilization, and Apache access profiles.
*   **App Tier Monitoring**: An Amazon ECS Fargate cluster routing microservice runtime exception parameters directly via native containerized `awslogs` telemetry hooks.
*   **Data Tier Monitoring**: An Amazon RDS MySQL instance configured with 60-second Enhanced Monitoring and engine exports (Audit, Error, and Slow Query logs) to capture query bottlenecks.
*   **Automation Loop**: Decoupled alarms routing event payloads natively via an Amazon EventBridge Rule bus straight to an AWS Lambda self-healing computing engine.

## 2. Saved Log Analytics Insights Framework
The optimized query logic targeted systemic anomalies by filtering standard 5xx status exceptions and critical operational codes within tight 5-minute tracking bins:
```sql
fields @timestamp, @message, @logStream

| filter @message like /(?i)(ERROR|Exception| 5\d{2} )/
| stats count(*) as errorCount by bin(5m) as timeWindow

| sort timeWindow desc
| limit 20
```
This enables auditors to distinguish between an isolated infrastructure error and a full cascading cross-tier database outage.

## 3. Chaos Simulation & Remediation Testing Verification
We verified our infrastructure monitoring configurations by invoking a mock high-load CPU threshold breach payload (`SimulateCpuSpikeAlarm` crossing the 80% boundary). 
*   **Alarm State Alteration**: The `ecs-task-high-cpu-80` alarm intercepted the condition and flipped status blocks cleanly.
*   **Event Handling & Orchestration**: Amazon EventBridge matched the custom filter pattern and instantly ran our automated Python script.
*   **Auto-Remediation Execution**: The script triggered a rolling service redeployment to clear out problematic tasks, successfully labeled target web assets (`i-0a559ebe51f64b5eb`) with remediation review tags, and paged the on-call response engineering team via Amazon SNS.

## 4. Operational Lessons & Evolutionary Vectors
*   **Decoupled Intelligence Benefits**: Triggering self-healing workloads outside of the application environment isolates operations. This ensures alerts pass through cleanly even if individual containers crash.
*   **Dynamic Baseline Enhancements**: Static threshold barriers can cause alert fatigue during standard Kenyan peak traffic hours. Upgrading to CloudWatch Anomaly Detection bands will allow alert boundaries to dynamically scale alongside real consumption baselines.
