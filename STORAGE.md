# Megalith Storage Strategy: Master-Slave Sync

To ensure zero-latency and high availability, Megalith uses a hierarchical storage system.

## 📂 1. The "Master" (NAS)

The NAS acts as the central repository for all GGUF/Ollama model files.

- **Path:** `/mnt/nas/ai/models`
- **Purpose:** Long-term storage, version control, and initial seeding.

## 📂 2. The "Slaves" (Local NVMe)

Each node uses its internal high-speed NVMe storage for the **Active Pinned Library**.

- **Path:** `/var/lib/ollama` (Default)
- **Purpose:** Elimination of network-boot latency.

## 🔄 Sync Logic

### Initial Deployment

When adding a new node:

1. Pull models from the NAS to the local node's NVMe.
2. Run `ollama run <model>` once to verify integrity.

### Active Sync (Optional)

For frequently updated models, use a simple `rsync` cron job:

```bash
# Run on each node
rsync -avz --ignore-existing /mnt/nas/ai/models/ /var/lib/ollama/models/
```

### Pinning Benefits

By using `OLLAMA_KEEP_ALIVE=-1` and local NVMe storage:

- **TTFT (Time To First Token):** < 100ms
- **Network Reliability:** Nodes can continue serving even if the NAS goes offline.
