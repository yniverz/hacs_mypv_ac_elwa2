[![License: NCPUL](https://img.shields.io/badge/license-NCPUL-blue.svg)](./LICENSE.md)

# my‑PV AC ELWA 2 – Home Assistant Integration

A simple integration that lets Home Assistant talk to a **my‑PV AC ELWA 2** water‑heater using HTTP. The component exposes live temperature readings and gives you a convenient slider to set the heater’s target power.

---

## ✨ Features

| Entity                           | Type   | Description                             |
| -------------------------------- | ------ | --------------------------------------- |
| **AC Elwa 2 Boiler Temperature** | Sensor | Current boiler temperature              |
| **AC Elwa 2 Target Power**       | Sensor | Last target power written to the device |
| **AC Elwa 2 Target Power**       | Number | Writable slider (0 … 3500 W)            |

* Target power is automatically resent every *30 s* (configurable) so the ELWA does not time‑out.
* Poll interval is configurable (default 10 s).

---

## 📦 Installation

### Via HACS (recommended)

1. Make sure you have [HACS](https://hacs.xyz) installed.
2. In **HACS → Integrations → ⋯ → *Custom repositories*** add
```
[https://github.com/yniverz/mypv\_ac\_elwa2](https://github.com/yniverz/mypv_ac_elwa2)
```
   as **Integration**.
3. Search for **“my‑PV AC ELWA 2”**, click **Download**, then **Install**.
4. **Restart** Home Assistant to load the new integration.

---

## ⚙️ Configuration (UI‑only)

This integration requires the **my-PV AC ELWA 2** to be set to **HTTP mode**.

Add the integration via **Settings → Devices & Services → + Add** and fill in:

| Field             | Default | Notes                                  |
|-------------------|---------|----------------------------------------|
| **IP address**    | –       | ELWA 2 HTTP host                       |
| **Poll interval** | 10 s    | Minimum 5 s                            |
| **Resend target** | 30 s    | How often to resend a non‑zero target  |

No YAML required.

---

## 📝 How it works
* Connects to `port 502`, slave‑id `1`.
* Reads two holding registers:
  * `1000`: power (W)
  * `1001`: temperature (°C × 0.1)
* Writes register `1000` to set power.
* Values outside **0 … 3500 W** are automatically clamped.
