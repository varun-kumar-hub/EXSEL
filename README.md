# 🚀 Smart Water Distribution & Sequential Water-Gate Control System

A production-grade Python web application for monitoring and controlling an industrial smart water distribution network, featuring **NiceGUI**, **FastAPI**, **Supabase (PostgreSQL + Auth)**, **Plotly**, and a modular **Hardware Abstraction Layer** supporting both high-fidelity simulation and physical ESP8266/ESP32 microcontrollers.

---

## 🏗️ Architecture & Layer Separation

The application strictly enforces a 5-layer decoupled architecture:

```
┌─────────────────────────────────────────────┐
│                  UI LAYER                    │
│                 NiceGUI                     │
├─────────────────────────────────────────────┤
│               APPLICATION LAYER             │
│        FastAPI REST API / Controllers       │
├─────────────────────────────────────────────┤
│                 SERVICE LAYER                │
│    Auth / Gates / Sensors / Alerts / etc.   │
├─────────────────────────────────────────────┤
│                 DATA LAYER                   │
│           Supabase / PostgreSQL             │
├─────────────────────────────────────────────┤
│               HARDWARE LAYER                │
│       ESP8266 / ESP32 / MQTT / Simulator    │
└─────────────────────────────────────────────┘
```

### Architectural Rules:
- **UI never directly accesses Supabase**: `UI → Service → Repository → Supabase`
- **UI never directly controls hardware**: `UI → Service → HardwareInterface → ESP8266`
- **Safety Interlocks**: Confirmation modals before any physical gate actuation or sequence start/stop.
- **Role-Based Access Control (RBAC)**: `ADMIN`, `OPERATOR`, and `VIEWER` roles enforced on all endpoints.

---

## 📂 Project Structure

```
smart-water/
├── app/
│   ├── main.py                     # Application entry point (FastAPI + NiceGUI)
│   ├── config/                     # Pydantic settings & constants
│   ├── core/                       # Security, exceptions, dependencies, logging
│   ├── database/                   # Supabase client, models, & repositories
│   ├── auth/                       # Authentication service & RBAC permissions
│   ├── services/                   # Business logic (Dashboard, Gates, Sensors, etc.)
│   ├── hardware/                   # Hardware abstraction (Simulator & ESP client)
│   ├── api/                        # FastAPI REST API endpoints
│   ├── schemas/                    # Pydantic request/response schemas
│   ├── ui/                         # NiceGUI interface (Layout, Components, Pages, Theme)
│   ├── mock/                       # Fixtures & realistic telemetry generators
│   └── utils/                      # Validators, formatters, calculations
│
├── supabase/
│   ├── all_in_one_setup.sql        # Single copy-paste setup for Supabase
│   ├── schema.sql                  # Database table definitions
│   ├── policies.sql                # Row Level Security (RLS) policies
│   ├── triggers.sql                # Auth signup trigger functions
│   └── seed.sql                    # Initial gates, sensors, and telemetry seed
│
├── tests/                          # Pytest unit & integration test suite
├── logs/                           # Rotating application & error logs
├── requirements.txt                # Python dependencies
├── run.py                          # Development launcher
├── Dockerfile                      # Production Docker container
└── docker-compose.yml              # Multi-container orchestration
```

---

## ⚡ Quick Start

### 1. Prerequisites
- Python 3.11+
- Git

### 2. Installation
```bash
# Clone the repository
git clone <repo-url>
cd EXSEL

# Create and activate virtual environment
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On Linux/macOS:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Environment Configuration
Copy the template `.env.example` to `.env`:
```bash
cp .env.example .env
```

| Variable | Description | Default |
|---|---|---|
| `APP_NAME` | System display name | `Smart Water Distribution System` |
| `APP_ENV` | Environment (`development` / `production`) | `development` |
| `HARDWARE_MODE` | Hardware layer mode (`simulation` / `esp`) | `simulation` |
| `SUPABASE_URL` | Supabase project URL | *(Optional - has in-memory fallback)* |
| `SUPABASE_ANON_KEY` | Supabase public anonymous key | *(Optional)* |
| `ESP_DEVICE_URL` | Local network URL for ESP8266 | `http://192.168.1.100` |
| `SECRET_KEY` | Secret session & signing key | *(Auto-configured)* |

> **Note**: If Supabase credentials are not provided, the application runs in **High-Fidelity In-Memory Mode**, allowing complete instant testing of all auth, gates, sensors, alerts, analytics, and history!

### 4. Supabase Database Setup (Optional)
If connecting to a real Supabase project:
1. Open your Supabase project dashboard → **SQL Editor**.
2. Copy and paste the contents of `supabase/all_in_one_setup.sql`.
3. Click **Run**.
4. Update `SUPABASE_URL` and `SUPABASE_ANON_KEY` in `.env`.

### 5. Running the Application
```bash
python run.py
```
Open your browser and navigate to:
**`http://localhost:8000`**

---

## 👤 Demo User Accounts

| Role | Email | Password | Permissions |
|---|---|---|---|
| **Admin** | `admin@smartwater.io` | `Admin@123` | Full control, User Management, Gate Actuation, Sequence, Settings |
| **Operator** | `operator@smartwater.io` | `Operator@123` | Gate Actuation, Sequence Start/Stop, Telemetry Monitoring, History |
| **Viewer** | `viewer@smartwater.io` | `Viewer@123` | Read-only telemetry (Actuation buttons disabled) |

*(Quick-fill buttons for these demo accounts are built directly into the `/login` screen)*

---

## 🧪 Testing

Run the automated test suite with pytest:
```bash
.venv\Scripts\pytest -v
```

---

## 📡 Hardware & IoT Integration

### Mode 1 — Realistic Simulation (`HARDWARE_MODE=simulation`)
Generates gradual, continuous hydraulic drift:
- Water Level: Smooth variations around 72.4% with threshold detection
- Flow Rate: Dynamically responds to gate open/close positions and pump status
- Pressure: 2.7 bar nominal with sensor fluctuations
- Gate Actuators: Realistic 2-second transit duration (`CLOSED` → `OPENING` → `OPEN`)

### Mode 2 — Physical ESP8266 / ESP32 (`HARDWARE_MODE=esp`)
The `ESPClient` connects via REST endpoints:
- `GET /api/sensors`: Fetches live analog transducer voltages and flow meters
- `POST /api/gate/{id}/open`: Actuates relay coils for sluice gate motors
- `POST /api/gate/{id}/close`: Reverses actuator polarity for closing
- `POST /api/pump/start`: Triggers the high-pressure booster pump relay

---

## 📊 REST API Endpoints

FastAPI endpoints are automatically documented at **`http://localhost:8000/docs`**:

- `POST /api/auth/login` — User authentication
- `POST /api/auth/signup` — Account registration with password strength checking
- `GET  /api/dashboard` — Live telemetry overview & summary metrics
- `GET  /api/gates` — Water gate status list
- `POST /api/gates/{id}/open` — Open gate actuator
- `POST /api/gates/{id}/close` — Close gate actuator
- `GET  /api/sensors` — Transducer readings & threshold parameters
- `GET  /api/distribution/status` — Automated routing pipeline status
- `POST /api/distribution/start` — Initiate automated distribution sequence
- `POST /api/distribution/stop` — Emergency sequence shutdown
- `GET  /api/analytics` — Statistical modeling (Pandas / NumPy)
- `GET  /api/history` — Audit log with multi-criteria filters
- `GET  /api/history/export` — Download complete audit log as CSV
#   E X S E L  
 