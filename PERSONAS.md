# Megalith Node Persona Guide

This guide outlines the specific configurations required for each hardware persona in the Megalith swarm.

## 🟢 1. The "Cruncher" (RTX 5090 Nodes)

**Priority:** Ultra-Low Latency Reasoning & Coding.

### Environment Tuning

```bash
# Permanent model pinning
OLLAMA_KEEP_ALIVE=-1
# Allow concurrent requests (1 per GPU)
OLLAMA_NUM_PARALLEL=2
# Host pinning
OLLAMA_HOST=0.0.0.0
```

### Recommended Models

- `deepseek-r1:latest`
- `qwen2.5-coder:latest`
- `flux-schnell`

---

## 🔵 2. The "Fat Brains" (AMD Halo Strix)

**Priority:** High-Context Analysis & RAG.

### Environment Tuning

```bash
# Expand context window to leverage 128GB RAM
OLLAMA_MAX_SIZE=64G
# Enable parallel processing for RAG
OLLAMA_NUM_PARALLEL=4
OLLAMA_KEEP_ALIVE=-1
```

### Recommended Models

- `llama3:70b`
- `mixtral:8x22b`

---

## 🟡 3. The "Media Labs" (3080Ti / 2080 / Corals)

**Priority:** Vision & Voice processing.

### Environment Tuning

```bash
# Offload to specific GPUs
CUDA_VISIBLE_DEVICES=0 # Set per machine
OLLAMA_KEEP_ALIVE=-1
```

### Recommended Models

- `llama3.2-vision`
- `whisper:large-v3`

---

## ⚪ 4. The "Micro-Logic Swarm" (Pi 5s)

**Priority:** Function Calling & Tool Routing.

### Environment Tuning

```bash
# Lightweight tuning for ARM
OLLAMA_NOPRELOAD=1 # Load on demand if memory is tight, or -1 if pinned
OLLAMA_NUM_PARALLEL=1
```

### Recommended Models

- `llama3.2:3b`
- `phi3.5:latest`

---

## 🛠️ Global Network Setup

All nodes must be accessible to the **Controller (Mac Studio M4)** via:

1. **10GbE Island** (Crunchers)
2. **2.5GbE Backbone** (Fat Brains/Media Labs)
3. **1GbE Cluster** (Swarm)

Ensure `OLLAMA_HOST=0.0.0.0` is set on all nodes to allow the Controller to route traffic.
