Project Overview
The Sentinel-Sidecar is a deterministic safety layer designed to prevent "The Butterfly Effect" in autonomous AI agents. As agents gain the ability to manage infrastructure, a single recursive logic loop or a prompt-injection attack can trigger a cascading failure across the Network, Application, and Hardware layers.

Sentinel acts as a Circuit Breaker, monitoring the "blast radius" of an agent from an isolated container. If the agent exceeds defined safety envelopes, Sentinel executes a hard kill to protect the global internet fabric.

Quick Start: Deployment
1. Prerequisites
Docker & Docker Compose

An autonomous agent image (e.g., AutoGPT, LangChain, or custom Python agents)

2. Configuration (config.json)
Define your safety thresholds before launching:

JSON
{
  "cpu_limit": 60.0,
  "mem_limit_mb": 1024,
  "net_limit_mbps": 50.0,
  "temp_limit_c": 80,
  "max_actions_per_window": 3,
  "window_seconds": 300
}
3. Launch with Docker Compose
Sentinel uses pid: "service:ai_agent" to monitor the agent's heartbeat without being part of the agent's logic.

Bash
docker-compose up --build
Security Philosophy: Determinism Over Intelligence
We believe that an AI should never be the primary monitor for another AI. Logic loops can be contagious. If a "Supervisor AI" uses the same underlying LLM as the "Worker AI," they can share the same hallucinations or vulnerabilities. Sentinel-Sidecar is written in deterministic Python. It doesn't "think"—it measures. If the math doesn't add up, the power is cut.

Contributing
We are looking for researchers to help expand the Hardware Layer to support specific GPU thermal offsets (NVIDIA/AMD) and Network Layer support for automated BGP null-routing.

Blog Post Summary
"The internet isn't a single entity; it’s a series of trust relationships. Agentic AI is the first technology capable of breaking those relationships at machine speed. Sentinel-Sidecar is the 'Human-in-the-Loop' translated into 100 lines of defensive code." — IT Security Blogger & Coder
