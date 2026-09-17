-- =============================================================================
-- ROW LEVEL SECURITY (RLS) POLICIES
-- =============================================================================

-- Enable RLS on all tables
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

-- 1. Profiles Policies
CREATE POLICY "Users can read own profile"
    ON public.profiles FOR SELECT
    USING (auth.uid() = id);

CREATE POLICY "Users can update own profile"
    ON public.profiles FOR UPDATE
    USING (auth.uid() = id);

CREATE POLICY "Admins have full access to profiles"
    ON public.profiles FOR ALL
    USING (
        EXISTS (
            SELECT 1 FROM public.profiles
            WHERE id = auth.uid() AND role = 'admin'
        )
    );

-- 2. Monitoring Tables Policies (Gates, Sensors, Readings, Sequences, Steps)
-- All authenticated users can read telemetry and status
CREATE POLICY "Authenticated users can read gates"
    ON public.gates FOR SELECT
    TO authenticated
    USING (true);

CREATE POLICY "Operators and admins can update gates"
    ON public.gates FOR UPDATE
    TO authenticated
    USING (
        EXISTS (
            SELECT 1 FROM public.profiles
            WHERE id = auth.uid() AND role IN ('admin', 'operator')
        )
    );

CREATE POLICY "Authenticated users can read sensors"
    ON public.sensors FOR SELECT
    TO authenticated
    USING (true);

CREATE POLICY "Authenticated users can read sensor readings"
    ON public.sensor_readings FOR SELECT
    TO authenticated
    USING (true);

CREATE POLICY "Authenticated users can read distribution sequences"
    ON public.distribution_sequences FOR SELECT
    TO authenticated
    USING (true);

CREATE POLICY "Operators and admins can manage distribution sequences"
    ON public.distribution_sequences FOR ALL
    TO authenticated
    USING (
        EXISTS (
            SELECT 1 FROM public.profiles
            WHERE id = auth.uid() AND role IN ('admin', 'operator')
        )
    );

CREATE POLICY "Authenticated users can read distribution steps"
    ON public.distribution_steps FOR SELECT
    TO authenticated
    USING (true);

-- 3. Alerts Policies
CREATE POLICY "Authenticated users can read alerts"
    ON public.alerts FOR SELECT
    TO authenticated
    USING (true);

CREATE POLICY "Operators and admins can update/dismiss alerts"
    ON public.alerts FOR UPDATE
    TO authenticated
    USING (
        EXISTS (
            SELECT 1 FROM public.profiles
            WHERE id = auth.uid() AND role IN ('admin', 'operator')
        )
    );

-- 4. Audit & Operations Logs Policies
CREATE POLICY "Authenticated users can read system events"
    ON public.system_events FOR SELECT
    TO authenticated
    USING (true);

CREATE POLICY "Authenticated users can read gate operations"
    ON public.gate_operations FOR SELECT
    TO authenticated
    USING (true);

-- 5. User Notification Tokens Policies
CREATE POLICY "Users manage own notification tokens"
    ON public.user_notification_tokens FOR ALL
    USING (auth.uid() = user_id);
