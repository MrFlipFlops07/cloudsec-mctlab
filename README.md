# Multi-Cloud Threat Detection & Automated IR Lab

A hands-on, end-to-end cloud security project simulating real-time threat detection, alerting, and automated incident response in AWS. Designed to demonstrate advanced SOC analyst workflows, cloud monitoring, and automated mitigation strategies.

---

## Project Overview

This project replicates a real-world Security Operations Center (SOC) pipeline in a cloud environment:

- Continuous ingestion of AWS CloudTrail logs from multiple regions.
- Centralized analysis using Elasticsearch (ELK Stack) for real-time visibility.
- Detection of suspicious activity patterns, such as console logins from unfamiliar IPs or unauthorized IAM key creation.
- Automated incident response via Lambda functions to isolate compromised resources, including stopping EC2 instances and revoking access keys.
- Red-team vs blue-team simulation: attack scenarios are generated and mitigated within the lab to demonstrate defense capabilities.

The project demonstrates **cloud security best practices**, automated monitoring, and the workflow of a SOC analyst in handling cloud threats.

- **Ingest Lambda:** Collects CloudTrail logs from CloudWatch and indexes them into Elasticsearch for analysis.
- **Detector Lambda:** Runs detection queries on Elasticsearch for suspicious events and triggers automated responses.
- **Playbook Lambda:** Executes response actions such as stopping EC2 instances, revoking IAM keys, and generating alerts.

---

## Key Features

- **Real-Time Threat Detection:** Monitors AWS activity and flags anomalies.
- **Automated Incident Response:** Playbooks isolate compromised resources without human intervention.
- **Centralized Logging and Visualization:** ELK Stack enables clear visualization of cloud events and alerts.
- **Red-Team vs Blue-Team Simulation:** Includes scenarios to test and validate security controls.
- **Modular Architecture:** Lambda functions, Terraform infrastructure, and ELK Stack are separated for clarity and scalability.
- **Extensible Pipeline:** Additional detection rules, threat intelligence feeds, or multi-cloud ingestion can be added.

---

## Technologies Used

- **Cloud & Security Services:** AWS CloudTrail, CloudWatch Logs, Lambda, S3, IAM
- **Infrastructure as Code:** Terraform
- **Monitoring & Visualization:** Elasticsearch, Kibana (ELK Stack)
- **Programming & Automation:** Python 3.11, `boto3`, `requests`
- **Containerization:** Docker (for local ELK deployment)
- **Version Control:** Git & GitHub

---

## Evidence / Outcomes

- Kibana dashboards visualizing detected suspicious events.
- Logs from Lambda functions showing automated response actions.
- Sample CloudTrail events demonstrating triggers for detection and remediation.
- Simulated attack scenarios including unauthorized access attempts and privilege escalation attempts.
- A fully functional cloud lab pipeline illustrating end-to-end SOC workflows.

**Sample Evidence:**

| Artifact | Description |
|----------|-------------|
| `evidence/kibana_dashboard.png` | Visualization of detected events in Elasticsearch/Kibana |
| `evidence/playbook_logs.png` | CloudWatch logs from Playbook Lambda showing automated response |
| `evidence/sample_event.json` | Example CloudTrail log triggering detection and response |

---

## Lessons Learned

- Real-time ingestion and processing of cloud logs is critical for SOC operations.
- Automation of incident response reduces human error and accelerates threat mitigation.
- Terraform enables reproducible cloud lab environments and safer experimentation.
- ELK Stack provides powerful, flexible visualization for cloud security events.
- Integration between detection logic and automated playbooks demonstrates the value of serverless SOC pipelines.

---

## Future Improvements

- **Multi-Cloud Integration:** Extend ingestion to Azure and GCP logs for centralized monitoring.
- **Threat Intelligence Enrichment:** Integrate APIs such as AbuseIPDB and VirusTotal for contextualized alerts.
- **SOAR Automation:** Automate ticket creation and escalation workflows in Jira or ServiceNow.
- **MITRE ATT&CK Mapping:** Classify detections and responses according to the MITRE ATT&CK framework for standardized reporting.
- **Alert Correlation:** Implement advanced event correlation to reduce false positives and prioritize high-severity incidents.

---

## Project Highlights

- End-to-end demonstration of **cloud SOC operations**.
- Real-time threat detection, alerting, and automated response pipeline.
- Modular and extensible architecture for hands-on experimentation.
- Clear portfolio-ready evidence of cloud security skills suitable for SOC analyst or cloud security roles.
- Fully documented and GitHub-ready for recruiters, hiring managers, or technical reviewers.

---

## Takeaways

This project showcases advanced cloud security concepts including:

- Monitoring and detection of cloud events in real-time.
- Automated remediation using serverless infrastructure.
- Centralized logging and visual analytics for threat management.
- Practical demonstration of SOC analyst workflows and cloud defense mechanisms.

It serves as a strong portfolio piece for anyone targeting **SOC analyst or cloud security roles**.
