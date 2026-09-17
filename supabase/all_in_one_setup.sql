-- =============================================================================
-- SMART WATER SYSTEM - COMPLETE ALL-IN-ONE SUPABASE MIGRATION
-- Run this single script in the Supabase SQL Editor to configure everything:
-- 1. Tables & Schema
-- 2. Row Level Security Policies
-- 3. Triggers
-- 4. Initial Seed Data
-- =============================================================================

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- -----------------------------------------------------------------------------
-- 1. TABLES
-- -----------------------------------------------------------------------------

-- Profiles table
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

-- Gates table
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

-- Sensors table
CREATE TABLE IF NOT EXISTS public.sensors (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    sensor_type TEXT NOT NULL,
    unit TEXT NOT NULL,
    minimum_threshold NUMERIC NOT NULL,
    maximum_threshold NUMERIC NOT NULL,
    status TEXT NOT NULL DEFAULT 'ONLINE' CHECK (status IN ('ONLINE', 'OFFLINE', 'WARNING', 'CRITICAL')),
    last_reading NUMERIC,
    last_updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Sensor readings telemetry
CREATE TABLE IF NOT EXISTS public.sensor_readings (
    id BIGSERIAL PRIMARY KEY,
    sensor_id TEXT NOT NULL REFERENCES public.sensors(id) ON DELETE CASCADE,
    value NUMERIC NOT NULL,
    recorded_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_sensor_readings_sensor_time ON public.sensor_readings(sensor_id, recorded_at DESC);

-- Alerts table
CREATE TABLE IF NOT EXISTS public.alerts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    alert_type TEXT NOT NULL,
    severity TEXT NOT NULL DEFAULT 'info' CHECK (severity IN ('critical', 'warning', 'info')),
    title TEXT NOT NULL,
    message TEXT NOT NULL,
    is_read BOOLEAN NOT NULL DEFAULT false,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_alerts_created_at ON public.alerts(created_at DESC);

-- Distribution sequences
CREATE TABLE IF NOT EXISTS public.distribution_sequences (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'WAITING' CHECK (status IN ('COMPLETED', 'ACTIVE', 'WAITING', 'FAILED')),
    current_step_index INT NOT NULL DEFAULT 0,
    started_at TIMESTAMPTZ,
    completed_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Distribution steps
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

-- Gate operations log
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

-- System events (Audit log)
CREATE TABLE IF NOT EXISTS public.system_events (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    event_type TEXT NOT NULL,
    device TEXT NOT NULL,
    action TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('Success', 'Warning', 'Failed', 'Info')),
    operator TEXT NOT NULL DEFAULT 'System',
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_system_events_time ON public.system_events(timestamp DESC);

-- User notification tokens
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

-- -----------------------------------------------------------------------------
-- 2. ROW LEVEL SECURITY (RLS)
-- -----------------------------------------------------------------------------

ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.gates ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.sensors ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.sensor_readings ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.alerts ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.distribution_sequences ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.distribution_steps ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.gate_operations ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.system_events ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.user_notification_tokens ENABLE ROW LEVEL SECURITY;

DO $$ 
BEGIN
    -- Drop existing policies if re-running
    DROP POLICY IF EXISTS "Users can read own profile" ON public.profiles;
    DROP POLICY IF EXISTS "Users can update own profile" ON public.profiles;
    DROP POLICY IF EXISTS "Admins have full access to profiles" ON public.profiles;
    DROP POLICY IF EXISTS "Authenticated users can read gates" ON public.gates;
    DROP POLICY IF EXISTS "Operators and admins can update gates" ON public.gates;
    DROP POLICY IF EXISTS "Authenticated users can read sensors" ON public.sensors;
    DROP POLICY IF EXISTS "Authenticated users can read sensor readings" ON public.sensor_readings;
    DROP POLICY IF EXISTS "Authenticated users can read distribution sequences" ON public.distribution_sequences;
    DROP POLICY IF EXISTS "Operators and admins can manage distribution sequences" ON public.distribution_sequences;
    DROP POLICY IF EXISTS "Authenticated users can read distribution steps" ON public.distribution_steps;
    DROP POLICY IF EXISTS "Authenticated users can read alerts" ON public.alerts;
    DROP POLICY IF EXISTS "Operators and admins can update/dismiss alerts" ON public.alerts;
    DROP POLICY IF EXISTS "Authenticated users can read system events" ON public.system_events;
    DROP POLICY IF EXISTS "Authenticated users can read gate operations" ON public.gate_operations;
    DROP POLICY IF EXISTS "Users manage own notification tokens" ON public.user_notification_tokens;
END $$;

CREATE POLICY "Users can read own profile" ON public.profiles FOR SELECT USING (auth.uid() = id);
CREATE POLICY "Users can update own profile" ON public.profiles FOR UPDATE USING (auth.uid() = id);
CREATE POLICY "Admins have full access to profiles" ON public.profiles FOR ALL USING (
    EXISTS (SELECT 1 FROM public.profiles WHERE id = auth.uid() AND role = 'admin')
);

CREATE POLICY "Authenticated users can read gates" ON public.gates FOR SELECT TO authenticated USING (true);
CREATE POLICY "Operators and admins can update gates" ON public.gates FOR UPDATE TO authenticated USING (
    EXISTS (SELECT 1 FROM public.profiles WHERE id = auth.uid() AND role IN ('admin', 'operator'))
);

CREATE POLICY "Authenticated users can read sensors" ON public.sensors FOR SELECT TO authenticated USING (true);
CREATE POLICY "Authenticated users can read sensor readings" ON public.sensor_readings FOR SELECT TO authenticated USING (true);
CREATE POLICY "Authenticated users can read distribution sequences" ON public.distribution_sequences FOR SELECT TO authenticated USING (true);
CREATE POLICY "Operators and admins can manage distribution sequences" ON public.distribution_sequences FOR ALL TO authenticated USING (
    EXISTS (SELECT 1 FROM public.profiles WHERE id = auth.uid() AND role IN ('admin', 'operator'))
);
CREATE POLICY "Authenticated users can read distribution steps" ON public.distribution_steps FOR SELECT TO authenticated USING (true);
CREATE POLICY "Authenticated users can read alerts" ON public.alerts FOR SELECT TO authenticated USING (true);
CREATE POLICY "Operators and admins can update/dismiss alerts" ON public.alerts FOR UPDATE TO authenticated USING (
    EXISTS (SELECT 1 FROM public.profiles WHERE id = auth.uid() AND role IN ('admin', 'operator'))
);
CREATE POLICY "Authenticated users can read system events" ON public.system_events FOR SELECT TO authenticated USING (true);
CREATE POLICY "Authenticated users can read gate operations" ON public.gate_operations FOR SELECT TO authenticated USING (true);
CREATE POLICY "Users manage own notification tokens" ON public.user_notification_tokens FOR ALL USING (auth.uid() = user_id);

-- -----------------------------------------------------------------------------
-- 3. TRIGGERS
-- -----------------------------------------------------------------------------

CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO public.profiles (id, email, full_name, role, is_active, created_at, updated_at)
    VALUES (
        NEW.id,
        NEW.email,
        COALESCE(NEW.raw_user_meta_data->>'full_name', split_part(NEW.email, '@', 1)),
        COALESCE(NEW.raw_user_meta_data->>'role', 'viewer'),
        true,
        NOW(),
        NOW()
    )
    ON CONFLICT (id) DO UPDATE
    SET email = EXCLUDED.email,
        full_name = EXCLUDED.full_name,
        updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

DROP TRIGGER IF EXISTS on_auth_user_created ON auth.users;
CREATE TRIGGER on_auth_user_created
    AFTER INSERT ON auth.users
    FOR EACH ROW EXECUTE FUNCTION public.handle_new_user();

-- -----------------------------------------------------------------------------
-- 4. SEED DATA
-- -----------------------------------------------------------------------------

INSERT INTO public.gates (id, name, location, status, mode, is_connected, last_changed_at)
VALUES
    ('GATE_01', 'Gate 01', 'Main Canal - Intake Feed', 'OPEN', 'AUTO', true, NOW() - INTERVAL '15 minutes'),
    ('GATE_02', 'Gate 02', 'Treatment Diversion North', 'OPEN', 'AUTO', true, NOW() - INTERVAL '35 minutes'),
    ('GATE_03', 'Gate 03', 'Distribution Bypass East', 'OPEN', 'AUTO', true, NOW() - INTERVAL '2 hours'),
    ('GATE_04', 'Gate 04', 'Secondary Spillway South', 'CLOSED', 'MANUAL', true, NOW() - INTERVAL '6 hours')
ON CONFLICT (id) DO UPDATE SET
    status = EXCLUDED.status,
    mode = EXCLUDED.mode,
    is_connected = EXCLUDED.is_connected;

INSERT INTO public.sensors (id, name, sensor_type, unit, minimum_threshold, maximum_threshold, status, last_reading, last_updated_at)
VALUES
    ('SENS_LVL_01', 'Reservoir Water Level', 'level', '%', 30.0, 85.0, 'ONLINE', 72.4, NOW()),
    ('SENS_FLW_01', 'Main Line Flow Meter', 'flow', 'L/min', 5.0, 30.0, 'ONLINE', 18.4, NOW()),
    ('SENS_PRS_01', 'Pressure Sensor P1', 'pressure', 'bar', 1.5, 4.0, 'ONLINE', 2.7, NOW()),
    ('SENS_FLW_02', 'Secondary Sector Flow', 'flow', 'L/min', 2.0, 15.0, 'ONLINE', 8.9, NOW()),
    ('SENS_WQL_01', 'Water Quality (pH)', 'ph', 'pH', 6.5, 8.5, 'ONLINE', 7.2, NOW()),
    ('SENS_WQL_02', 'Water Quality (Turbidity)', 'turbidity', 'NTU', 0.5, 5.0, 'ONLINE', 2.4, NOW())
ON CONFLICT (id) DO UPDATE SET
    last_reading = EXCLUDED.last_reading,
    status = EXCLUDED.status;

INSERT INTO public.alerts (alert_type, severity, title, message, is_read, created_at)
VALUES
    ('high_flow', 'warning', 'High Flow Rate in Secondary Sector', 'Flow rate reached 14.2 L/min, approaching maximum threshold (15.0 L/min).', false, NOW() - INTERVAL '12 minutes'),
    ('sensor_cal', 'info', 'Routine Sensor Diagnostic Complete', 'Pressure sensor P1 completed self-calibration cycle with zero drift.', false, NOW() - INTERVAL '45 minutes'),
    ('gate_telemetry', 'info', 'Gate 04 Manual Mode Engaged', 'Operator switched Gate 04 to manual inspection mode.', true, NOW() - INTERVAL '3 hours'),
    ('system_online', 'info', 'System Telemetry Online', 'All 5 sensor nodes and 4 water gate controllers reporting nominal heartbeat.', true, NOW() - INTERVAL '5 hours')
ON CONFLICT DO NOTHING;
