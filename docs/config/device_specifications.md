# Clever AI Device Specifications

**Last updated:** 2025-09-21  
**Generation:** Born in GitHub Codespaces, Lives on Chrome OS

---

## Device Overview

**Why:** This document preserves the complete hardware and software environment where Clever AI was born and operates, ensuring reproducibility and system understanding for debugging, optimization, and deployment decisions.

**Where:** This connects to the entire Clever ecosystem by documenting the foundational platform that hosts the Flask server, SQLite database, and all AI processing operations.

**How:** Comprehensive system diagnostic data captured from Chrome OS device running Clever through GitHub Codespaces development environment.

**Connects to:**
    - config.py: Hardware-aware configuration settings and performance limits
    - debug_config.py: Performance monitoring and optimization based on device capabilities  
    - persona.py: Response generation limits guided by processing constraints
    - nlp_processor.py: spaCy model selection and processing limits for device performance
    - static/js/engines/holographic-chamber.js: Particle count and rendering limits for GPU
    - evolution_engine.py: Learning batch sizes and processing intervals for device capacity
    - database.py: SQLite optimization settings and query limits for storage constraints
    - All Python modules: Referenced for performance-conscious implementation decisions

---

## Primary Host Device

### Chrome OS System

- **Device Model:** Google Pirika (HWID: PASARA-TZNR C3B-D3B-B3B-C3Q-A8C)
- **Chrome OS Version:** 16328.72.0 (Official Build) stable-channel
- **Chrome Version:** 139.0.7258.172
- **Firmware:** Google_Pirika.13606.646.0
- **Architecture:** dedede-signed-mp-v57keys
- **Board:** dedede (Chromebook platform)

### Display Configuration

- **Built-in Display:** BOE - Product ID: 07AA (Year: 2017)
- **Resolution:** 1366x768 (primary), supports external displays up to 1920x1080
- **Display Zoom:** 1.05x scaling factor
- **Multi-monitor:** Supports HDMI/DP output (3 ports available)

### Input Devices

- **Keyboard:** AT Translated Set 2 keyboard (Internal)
- **Touchpad:** Elan Touchpad (Vendor: 04F3, Product: 0124)
- **External:** 2.4G RF Keyboard & Mouse (USB, Vendor: 3938, Product: 1192)
- **Audio:** sof-rt5682 with Headset Jack, HDMI/DP audio support

---

## Development Environment

### GitHub Codespaces Container

- **Host OS:** Debian GNU/Linux 13 (trixie)
- **Container Runtime:** Dev container with Python 3.12, Node.js, Git
- **Workspace Path:** `/workspaces/Clever`
- **Network:** Connected via Chrome OS to WiFi "Loddy" (192.168.1.71/24)

### Network Configuration

```text
Primary Interface: wlan0 (28:DF:EB:F3:EA:44)
IPv4: 192.168.1.71/24
IPv6: 2600:1700:c750:ed0:d12f:349c:6c9f:cfce/64
Gateway: 192.168.1.254
DNS: 192.168.1.254, 2600:1700:c750:ed0::1
Signal Strength: 100% (-30 dBm average)
```

---

## Storage & Memory

### Disk Usage

- **Total Space:** 107GB (eMMC storage)
- **Available:** 6.9GB free (94% utilization)
- **Encrypted:** 32GB encrypted stateful partition (7% used)
- **Root:** 3.4GB ChromeOS system (87% used)

### Memory Allocation

- **Chrome Browser:** 177MB + multiple tabs (266MB, 183MB, 78MB, 40MB, 27MB)
- **Extensions:** Application Launcher (50MB), Image Loader (27MB)
- **System Services:** Network (31MB), Input Method (24MB+21MB), Storage (19MB)

---

## Audio System (ALSA)

### Hardware Devices

- **Codec:** sof-rt5682 (Intel Smart Sound Technology)
- **Outputs:** Built-in speakers, Headphone jack, 3x HDMI/DP
- **Inputs:** Built-in microphone, Headset microphone
- **Volume Control:** Hardware volume controls active
- **Sample Rates:** Support for 23-48kHz, VHT capabilities

### Current Audio State

```text
Master Volume: 100% (speakers), 40% (headphones)
Microphone: Muted (CBJ Boost: 30dB)
HDMI Outputs: Available but not connected
IEC958 Digital: Enabled on all HDMI ports
Speaker Controls: Hardware buttons active
Audio Codec: Advanced DSP with noise cancellation
```

### Detailed Audio Diagnostics

```text
Card 0: sofrt5682 [sof-rt5682]
  Device 0: HiFi: ALC5682 Analog (*) [HiFi: ALC5682 Analog]
  Device 1: HiFi: rt5682-aif2 (*) [HiFi: rt5682-aif2]  
  Device 2: Headset: ALC5682 (*) [Headset: ALC5682]
  Device 3: HDMI1: (*) [HDMI1]
  Device 4: HDMI2: (*) [HDMI2]
  Device 5: HDMI3: (*) [HDMI3]

Control Elements:
- Master: 98% volume (hardware control)
- Headphone: 40% volume
- Speaker: 100% volume  
- Mic: Muted with 30dB boost available
- HDMI Audio: Ready on all 3 ports
- VHT: Variable High-Threshold processing enabled
```

---

## Clever AI Operational Context

### File System Integration

- **Database Location:** `/workspaces/Clever/clever.db` (SQLite)
- **Static Assets:** `/workspaces/Clever/static/` (CSS, JS, images)
- **Templates:** `/workspaces/Clever/templates/` (Jinja2 HTML)
- **Logs:** `/workspaces/Clever/logs/` (application logging)

### Network Services

- **Flask Server:** Runs on `127.0.0.1:5000`
- **Cache Busting:** Dynamic timestamps for static file updates
- **Offline Mode:** Enforced via `utils.offline_guard.enable()`
- **Sync Directories:** `Clever_Sync/`, `synaptic_hub_sync/`

### Performance Characteristics

- **CPU:** Intel Jasper Lake (low-power Chromebook processor)
- **Storage:** eMMC (sequential, good for SQLite operations)
- **Memory:** Limited RAM requires efficient caching strategies
- **Network:** WiFi 802.11ac (866.7 Mbps capable, excellent signal)

---

## Security & Privacy Profile

### Enterprise Status

- **Management:** Not managed (personal device)
- **Sync:** Google Sync enabled with encryption
- **VPN:** Available but not connected
- **Bluetooth:** Floss enabled
- **ARC:** Android Runtime for Chrome (enabled)

### Data Protection

- **Disk Encryption:** ChromeOS encrypted stateful partition
- **Network Security:** WPA2/WPA3 WiFi, firewall active
- **Sandbox:** All web content runs in ChromeOS sandbox
- **Offline First:** Clever AI operates without cloud dependencies

---

## Troubleshooting Reference

### Common Issues

1. **Storage Full:** 94% disk usage may affect performance
2. **Memory Pressure:** Close unused Chrome tabs if Clever becomes slow
3. **Network Changes:** WiFi reconnection may change IP address
4. **Display Scaling:** UI elements designed for 1366x768 base resolution

### System Monitoring

```bash
# Check disk space
df -h

# Monitor memory usage
free -h

# Network connectivity
ip route show table 1002

# Audio status  
amixer scontrols

# Full system status
chrome://system/

# Hardware diagnostics
cat /proc/cpuinfo
cat /proc/meminfo
lspci -v
```

### Latest System Snapshot (2025-09-21)

```text
Chrome Browser Memory Usage:
- Main Process: 177MB
- Tab 1 (GitHub): 266MB  
- Tab 2 (Codespaces): 183MB
- Tab 3 (DevTools): 78MB
- Tab 4 (Documentation): 40MB
- Tab 5 (Utils): 27MB

System Services:
- Network Service: 31MB
- Input Method (Japanese): 24MB + 21MB
- Storage Manager: 19MB
- Extensions: App Launcher (50MB), Image Loader (27MB)

Disk Status:
- Root partition: 3.4GB (87% used)
- Stateful: 32GB encrypted (7% used)  
- Downloads: Active user content
- Total Available: 6.9GB free space
```

---

## Optimization Notes

### Performance Tuning

- **SQLite:** Benefits from SSD-style access patterns on eMMC
- **Flask:** Single-threaded model works well on limited CPU
- **Static Files:** Cache busting prevents stale UI after updates
- **Particle Engine:** Hardware-accelerated Canvas2D for smooth animations

### Recommended Limits

- **Database Size:** Keep under 1GB for optimal performance
- **File Uploads:** Limit to 10MB per PDF for memory efficiency
- **Concurrent Users:** Single-user design (no multi-tenancy)
- **Background Tasks:** Minimal to preserve battery life

---

## Future Considerations

### Scalability Path

- **Storage:** Consider cloud sync when disk space becomes critical
- **Performance:** Profile memory usage if adding heavy NLP models
- **Display:** Test UI on higher DPI external monitors
- **Network:** Plan for offline operation during connectivity issues

### Hardware Lifecycle

- **Expected Lifespan:** 3-5 years for Chrome OS auto-updates
- **Migration Path:** Export clever.db and source code for new device
- **Backup Strategy:** Regular database exports to Google Drive or external storage

---

*This specification serves as the canonical reference for Clever AI's hardware and software environment, ensuring consistent operation and informed development decisions.*
