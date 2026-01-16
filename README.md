<p align="center">
  <img src="https://brands.home-assistant.io/_/solax_local_api/logo.png" alt="SolaX Logo" width="200"/>
</p>

# <img src="https://brands.home-assistant.io/_/solax_local_api/icon.png" alt="SolaX Icon" width="30"/> SolaX Inverter Local API

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg?style=for-the-badge)](https://github.com/hacs/integration)
[![version](https://img.shields.io/github/v/release/GeroComp/Solax-local-API?style=for-the-badge)](https://github.com/GeroComp/Solax-local-API/releases)
![Discovery](https://img.shields.io/badge/discovery-DHCP-orange?style=for-the-badge)
![License](https://img.shields.io/github/license/GeroComp/Solax-local-API?style=for-the-badge)
[![Czech](https://img.shields.io/badge/Language-Czech-red)](README_cs.md)

This integration provides **local monitoring** for **SolaX Hybrid G4** inverters in Home Assistant.
Communication is performed directly over the local network (LAN/WiFi) via HTTP requests to the Pocket Wi-Fi dongle, ensuring cloud independence and fast response times.

---

## ✨ Features
- **Zero-Config Discovery**: Automatic detection of the inverter on the network based on DHCP (searches for Espressif devices with Pocket Wi-Fi).
- **Dynamic Interval**: Change the data update rate (6s to 5 min) instantly via a Select entity in the Dashboard.
- **Robust Connection**: Optimistic startup – the integration loads even at night when the inverter is asleep (entities show as unavailable, but the integration does not fail).
- **Efficient Data Collection**: Uses `DataUpdateCoordinator` to fetch all data in a single request.
- **Smart Icons**: Icons dynamically change based on battery SoC, energy flow (import/export), and time of day.
- **Energy Dashboard**: Fully compatible with the native Home Assistant Energy Dashboard.

---

## 🔍 Auto-Discovery
The integration supports **Auto-Discovery**. Once the inverter with the Pocket Wi-Fi dongle connects to the network, Home Assistant will recognize it.

In the **Devices & Services** section, you will see a notification:
> **Discovered: SolaX Local API** > *SolaX Power*

Click **Configure**. The integration will automatically fill in the detected IP address; you only need to enter the API password (usually the dongle's registration number).

---

## ⚡ Energy Dashboard Setup
For correct statistics in the Energy Panel, use the following entities:

| Energy Dashboard Section | Home Assistant Entity |
| :--- | :--- |
| **Solar production** | `sensor.solax_solar_total` |
| **Grid consumption** | `sensor.solax_grid_in_total` |
| **Return to grid** | `sensor.solax_grid_out_total` |
| **Battery storage - In** | `sensor.solax_battery_in_total` |
| **Battery storage - Out** | `sensor.solax_battery_out_total` |

> [!TIP]
> The `_total` sensors are of the `TOTAL_INCREASING` state class, which is required for long-term statistics.

---

## ⚙️ Installation & Configuration

### Manual Installation
1. Download the repository and copy the `solax_local_api` folder into your `custom_components` directory.
2. **Restart Home Assistant.**
3. The integration should be automatically discovered. If not, add it via **Settings -> Devices & Services -> Add Integration -> SolaX Local API**.

### Configuration
- **IP Address**: Local IP address of the Pocket Wi-Fi dongle.
- **Password**: API password (often the same as the dongle serial number or registration code).
- **Scan Interval**: Default is 10 seconds.

---

## 📊 Entities & Controls

### Main Sensors
The integration creates approximately 50 sensors, including:
- **PV**: Voltage, Current, and Power for both strings (PV1, PV2).
- **Battery**: SoC, Voltage, Current, Temperature, BMS Status, and Remaining Energy.
- **Grid**: Import/Export (Current W and Total kWh).
- **Inverter**: Temperatures, Frequency, Power Factor, Serial Number.

### Controls (New)
The integration now includes a `Select` entity:
- **Scan Interval** (`select.solax_scan_interval`): Allows changing the polling rate on the fly.
  - *Options:* 6s (Aggressive), 10s, ..., up to 5 minutes.
  - Changes take effect immediately and are saved to the configuration.

### Diagnostics
- **Current Scan Interval** (`sensor.solax_interval_diagnostic`): Displays the actual time in seconds between the last data updates.

---

## 📂 Project Structure
- `__init__.py`: Integration initialization and platform loading.
- `coordinator.py`: Data fetching management and session handling.
- `sensor.py`: Sensor definitions, data parsing, and icon logic.
- `select.py`: Implementation of the scan interval switch.
- `const.py`: Register tables, constants, and model mapping.
- `config_flow.py`: Configuration flow and DHCP discovery.
- `manifest.json`: Version and dependency definitions.

---

**Disclaimer**: This integration is not an official product of SolaX Power. Use at your own risk.
