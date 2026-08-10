-- ============================================================
-- Reset business tables created by granny-flat-schema.sql
-- so Django migrations can recreate them cleanly.
--
-- Run this ONCE in pgAdmin (Query Tool) on your PostgreSQL database
-- (the name in POSTGRES_DB inside .env, e.g. granny_flat)
-- BEFORE: python manage.py migrate
--
-- Safe for Phase 1 learning data (drops business tables only).
-- Does NOT drop Django system tables (auth_*, django_*).

-- `DROP TABLE`: to delete tables
-- `IF EXISTS`: if table is gone and already not exists --> Won't throw error, skip the `DROP TABLE` cmd to next step
-- `CASCADE`: To remove dependent constraints/objects so the drop can succeed

-- Purpose of this SQL file:
-- Those tables were created by hand. Django needs to recreate them via migrations so it can track changes.
-- ============================================================

DROP TABLE IF EXISTS commissions CASCADE; 
DROP TABLE IF EXISTS project_updates CASCADE;
DROP TABLE IF EXISTS project_partners CASCADE;
DROP TABLE IF EXISTS project_stage_progress CASCADE;
DROP TABLE IF EXISTS project_stages CASCADE;
DROP TABLE IF EXISTS projects CASCADE;
DROP TABLE IF EXISTS partners CASCADE;
DROP TABLE IF EXISTS clients CASCADE;
DROP TABLE IF EXISTS leads CASCADE;
DROP TABLE IF EXISTS users CASCADE;

