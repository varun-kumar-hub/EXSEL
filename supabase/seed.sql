-- =============================================================================
-- SMART WATER SYSTEM - SEED DATA
-- =============================================================================

-- Seed Gates
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

-- Seed Sensors
INSERT INTO public.sensors (id, name, sensor_type, unit, minimum_threshold, maximum_threshold, status, last_reading, last_updated_at)
VALUES
    ('SENS_LVL_01', 'Reservoir Water Level', 'level', '%', 30.0, 85.0, 'ONLINE', 72.4, NOW()),
    ('SENS_FLW_01', 'Main Line Flow Meter', 'flow', 'L/min', 5.0, 30.0, 'ONLINE', 18.4, NOW()),
    ('SENS_PRS_01', 'Pressure Sensor P1', 'pressure', 'bar', 1.5, 4.0, 'ONLINE', 2.7, NOW()),
    ('SENS_FLW_02', 'Secondary Sector Flow', 'flow', 'L/min', 2.0, 15.0, 'ONLINE', 8.9, NOW()),
    ('SENS_WQL_01', 'Water Quality (pH Level)', 'quality', 'pH', 6.5, 8.5, 'ONLINE', 7.2, NOW()),
    ('SENS_WQL_02', 'Water Quality (Turbidity)', 'turbidity', 'NTU', 0.5, 5.0, 'ONLINE', 2.4, NOW())
ON CONFLICT (id) DO UPDATE SET
    last_reading = EXCLUDED.last_reading,
    status = EXCLUDED.status;

-- Seed Initial Alerts
INSERT INTO public.alerts (alert_type, severity, title, message, is_read, created_at)
VALUES
    ('high_flow', 'warning', 'High Flow Rate in Secondary Sector', 'Flow rate reached 14.2 L/min, approaching maximum threshold (15.0 L/min).', false, NOW() - INTERVAL '12 minutes'),
    ('sensor_cal', 'info', 'Routine Sensor Diagnostic Complete', 'Pressure sensor P1 completed self-calibration cycle with zero drift.', false, NOW() - INTERVAL '45 minutes'),
    ('gate_telemetry', 'info', 'Gate 04 Manual Mode Engaged', 'Operator switched Gate 04 to manual inspection mode.', true, NOW() - INTERVAL '3 hours'),
    ('system_online', 'info', 'System Telemetry Online', 'All 5 sensor nodes and 4 water gate controllers reporting nominal heartbeat.', true, NOW() - INTERVAL '5 hours');

-- Seed System Events (Audit Log)
INSERT INTO public.system_events (timestamp, event_type, device, action, status, operator, metadata)
VALUES
    (NOW() - INTERVAL '5 minutes', 'Gate Operation', 'Gate 01', 'OPEN', 'Success', 'Operator', '{"source": "Auto-Sequence", "target_pct": 100}'::jsonb),
    (NOW() - INTERVAL '12 minutes', 'Sensor Alert', 'Secondary Flow', 'ALERT', 'Warning', 'System', '{"reading": 14.2, "unit": "L/min"}'::jsonb),
    (NOW() - INTERVAL '35 minutes', 'Sequence', 'Sector B', 'START', 'Success', 'Admin', '{"sequence": "Sector B Distribution", "steps": 4}'::jsonb),
    (NOW() - INTERVAL '2 hours', 'Gate Operation', 'Gate 03', 'OPEN', 'Success', 'Admin', '{"source": "Manual Override"}'::jsonb),
    (NOW() - INTERVAL '4 hours', 'Auth', 'User Session', 'LOGIN', 'Success', 'Operator', '{"email": "operator@smartwater.local"}'::jsonb);
