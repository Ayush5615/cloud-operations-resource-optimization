\# Cloud Operations \& Resource Optimization Platform



A cloud operations platform for monitoring AWS EC2 resources, detecting cost anomalies, generating optimization recommendations, and executing remediation through a human approval workflow.



\## Overview



Cloud infrastructure can accumulate unnecessary cost when resources are underutilized, misconfigured, or left running without sufficient monitoring.



This project provides an operational workflow:



AWS Resources

&#x20;   ↓

Resource Monitoring

&#x20;   ↓

Cost / Usage Analysis

&#x20;   ↓

Anomaly Detection

&#x20;   ↓

AI-Assisted Explanation

&#x20;   ↓

Optimization Recommendation

&#x20;   ↓

Human Approval

&#x20;   ↓

Remediation

&#x20;   ↓

Audit Log



The goal is not to automate every decision blindly. The platform keeps a human approval step before remediation and records the resulting action in an audit log.



\## Key Features



\- AWS EC2 resource discovery

\- EC2 instance state and metadata monitoring

\- CPU utilization monitoring through Amazon CloudWatch

\- Cost anomaly detection

\- AI-assisted explanation of detected anomalies

\- Cloud optimization recommendations

\- Persistent recommendation management

\- Human approval workflow

\- Recommendation rejection workflow

\- EC2 remediation through AWS APIs

\- Approval and rejection state validation

\- Audit logging for operational actions

\- Dashboard for resource and recommendation visibility



\## Architecture



```text

&#x20;                   AWS

&#x20;                    |

&#x20;             +------+------+

&#x20;             |             |

&#x20;            EC2        CloudWatch

&#x20;             |             |

&#x20;             +------+------+

&#x20;                    |

&#x20;               AWS Service

&#x20;                    |

&#x20;                    v

&#x20;            Resource Analysis

&#x20;                    |

&#x20;         +----------+----------+

&#x20;         |                     |

&#x20;         v                     v

&#x20;   Cost Anomaly            CPU Analysis

&#x20;     Detection                 |

&#x20;         |                     |

&#x20;         +----------+----------+

&#x20;                    |

&#x20;                    v

&#x20;             AI Explanation

&#x20;                    |

&#x20;                    v

&#x20;         Optimization Engine

&#x20;                    |

&#x20;                    v

&#x20;            Recommendation

&#x20;                    |

&#x20;             Human Approval

&#x20;              /          \\

&#x20;             /            \\

&#x20;         Reject          Approve

&#x20;           |                |

&#x20;           v                v

&#x20;       REJECTED         Remediation

&#x20;           |                |

&#x20;           +-------+--------+

&#x20;                   |

&#x20;                   v

&#x20;               Audit Log

