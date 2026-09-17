-- =============================================================================
-- SMART WATER DISTRIBUTION & SEQUENTIAL WATER-GATE CONTROL SYSTEM
-- DATABASE SCHEMA DEFINITION (SUPABASE / POSTGRESQL)
-- =============================================================================

-- Enable UUID extension if not enabled
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 1. PROFILES TABLE (Mirrors and extends auth.users)
CREATE TABLE IF NOT EXISTS public.profiles (
    id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    email TEXT UNIQUE NOT NULL,
    full_name TEXT,
    avatar_url TEXT,
    role TEXT NOT NULL DEFAULT 'viewer' CHECK (role IN ('admin', 'operator', 'viewer')),
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 2. WATER GATES TABLE
CREATE TABLE IF NOT EXISTS public.gates (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    location TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'CLOSED' CHECK (status IN ('OPEN', 'CLOSED', 'OPENING', 'CLOSING', 'ERROR')),
    mode TEXT NOT NULL DEFAULT 'AUTO' CHECK (mode IN ('AUTO', 'MANUAL')),
    is_connected BOOLEAN NOT NULL DEFAULT true,
    last_changed_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 3. SENSORS TABLE
CREATE TABLE IF NOT EXISTS public.sensors (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    sensor_type TEXT NOT NULL, -- level, flow, pressure, ph, turbidity
    unit TEXT NOT NULL,
    minimum_threshold NUMERIC NOT NULL,
    maximum_threshold NUMERIC NOT NULL,
    status TEXT NOT NULL DEFAULT 'ONLINE' CHECK (status IN ('ONLINE', 'OFFLINE', 'WARNING', 'CRITICAL')),
    last_reading NUMERIC,
    last_updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 4. SENSOR READINGS TABLE (Timeseries Telemetry)
CREATE TABLE IF NOT EXISTS public.sensor_readings (
    id BIGSERIAL PRIMARY KEY,
    sensor_id TEXT NOT NULL REFERENCES public.sensors(id) ON DELETE CASCADE,
    value NUMERIC NOT NULL,
    recorded_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_sensor_readings_sensor_time ON public.sensor_readings(sensor_id, recorded_at DESC);

-- 5. ALERTS TABLE
CREATE TABLE IF NOT EXISTS public.alerts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    alert_type TEXT NOT NULL, -- low_water, high_pressure, gate_offline, sensor_offline, sequence_failed
    severity TEXT NOT NULL DEFAULT 'info' CHECK (severity IN ('critical', 'warning', 'info')),
    title TEXT NOT NULL,
    message TEXT NOT NULL,
    is_read BOOLEAN NOT NULL DEFAULT false,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_alerts_created_at ON public.alerts(created_at DESC);

-- 6. DISTRIBUTION SEQUENCES TABLE
CREATE TABLE IF NOT EXISTS public.distribution_sequences (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'WAITING' CHECK (status IN ('COMPLETED', 'ACTIVE', 'WAITING', 'FAILED')),
    current_step_index INT NOT NULL DEFAULT 0,
    started_at TIMESTAMPTZ,
    completed_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 7. DISTRIBUTION STEPS TABLE
CREATE TABLE IF NOT EXISTS public.distribution_steps (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    sequence_id UUID NOT NULL REFERENCES public.distribution_sequences(id) ON DELETE CASCADE,
    step_order INT NOT NULL,
    step_name TEXT NOT NULL,
    gate_target TEXT,
    target_flow NUMERIC,
    status TEXT NOT NULL DEFAULT 'WAITING' CHECK (status IN ('COMPLETED', 'ACTIVE', 'WAITING', 'FAILED')),
    notes TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 8. GATE OPERATIONS LOG
CREATE TABLE IF NOT EXISTS public.gate_operations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    gate_id TEXT NOT NULL REFERENCES public.gates(id) ON DELETE CASCADE,
    operation TEXT NOT NULL CHECK (operation IN ('OPEN', 'CLOSE', 'MODE_AUTO', 'MODE_MANUAL')),
    requested_by UUID REFERENCES public.profiles(id) ON DELETE SET NULL,
    status TEXT NOT NULL DEFAULT 'SUCCESS' CHECK (status IN ('SUCCESS', 'FAILED', 'CANCELLED')),
    details JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_gate_operations_gate ON public.gate_operations(gate_id, created_at DESC);

-- 9. SYSTEM EVENTS TABLE (Audit Trail)
CREATE TABLE IF NOT EXISTS public.system_events (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    event_type TEXT NOT NULL, -- Gate Operation, Sensor Alert, Sequence, Auth, System
    device TEXT NOT NULL,
    action TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('Success', 'Warning', 'Failed', 'Info')),
    operator TEXT NOT NULL DEFAULT 'System',
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_system_events_time ON public.system_events(timestamp DESC);

-- 10. USER NOTIFICATION TOKENS TABLE
CREATE TABLE IF NOT EXISTS public.user_notification_tokens (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES public.profiles(id) ON DELETE CASCADE,
    device_token TEXT UNIQUE NOT NULL,
    device_type TEXT NOT NULL CHECK (device_type IN ('web', 'mobile')),
    device_name TEXT,
    is_active BOOLEAN NOT NULL DEFAULT true,
    last_used_at TIMESTAMPTZ DEFAULT NOW(),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
