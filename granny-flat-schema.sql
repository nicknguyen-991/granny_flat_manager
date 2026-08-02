-- ============================================================
-- SCHEMA: Cong cu quan ly doi tac xay dung Granny Flat
-- Database: PostgreSQL
-- Thiet ke theo chuan 3NF (Third Normal Form)
-- ============================================================

-- ============================================================
-- 1. USERS: nhan vien noi bo (admin, sales, quan ly cong trinh)
-- ============================================================
-- PRIMARY KEY (PK):
--   id  -> uniquely identifies each staff member
--
-- FOREIGN KEYS (FK):
--   (none in this table — users is a root/parent table)
--
-- RELATIONSHIPS (how other tables connect to users):
--   users  1 ----< *  leads              (one sales rep, many leads)
--   users  1 ----< *  projects           (one sales rep, many projects)
--   users  1 ----< *  project_updates    (one user, many site updates)
--   users  1 ----< *  commissions        (one sales rep, many commissions)
-- ============================================================
CREATE TABLE users (
    id SERIAL PRIMARY KEY,                  -- PK
    first_name VARCHAR(75) NOT NULL,
    last_name VARCHAR(75) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    phone VARCHAR(20),
    role VARCHAR(20) NOT NULL CHECK (
		role IN(
			'admin', 
			'sales', 
			'site_manager'
		)
	),
    created_at TIMESTAMP NOT NULL DEFAULT now()
);

-- ============================================================
-- 2. LEADS: khach hang tiem nang, truoc khi ky hop dong
-- ============================================================
-- PRIMARY KEY (PK):
--   id  -> uniquely identifies each lead
--
-- FOREIGN KEYS (FK):
--   assigned_sales_id  ->  users(id)     (nullable)
--
-- RELATIONSHIPS:
--   leads  * ----> 1  users              (many leads assigned to one sales rep)
--   leads  1 ----< *  clients            (one lead may convert to zero or more clients)
-- ============================================================
CREATE TABLE leads (
    id SERIAL PRIMARY KEY,                  -- PK
    first_name VARCHAR(75) NOT NULL,
    last_name VARCHAR(75) NOT NULL,
    phone VARCHAR(20),
    email VARCHAR(150),
    source VARCHAR(30) CHECK (
		source IN (
			'google_ads', 
			'referral', 
			'walk_in', 
			'website', 
			'other'
			)
		),
    assigned_sales_id INTEGER REFERENCES users(id),  -- FK -> users.id
    status VARCHAR(20) NOT NULL DEFAULT 'new'
        CHECK (status IN (
			'new', 
			'contacted', 
			'quoted', 
			'won', 
			'lost'
			)
		),
    notes TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT now()
);

-- ============================================================
-- 3. CLIENTS: khach hang chinh thuc (sau khi lead chuyen doi thanh cong)
-- ============================================================
-- PRIMARY KEY (PK):
--   id  -> uniquely identifies each client
--
-- FOREIGN KEYS (FK):
--   lead_id  ->  leads(id)                 (nullable — client may exist without a lead record)
--
-- RELATIONSHIPS:
--   clients  * ----> 1  leads             (many clients may trace back to one lead)
--   clients  1 ----< *  projects          (one client, many granny flat projects)
-- ============================================================
CREATE TABLE clients (
    id SERIAL PRIMARY KEY,                  -- PK
    lead_id INTEGER REFERENCES leads(id), -- FK -> leads.id
    first_name VARCHAR(75) NOT NULL,
    last_name VARCHAR(75) NOT NULL,
    phone VARCHAR(20),
    email VARCHAR(150),
    site_address TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT now()
);

-- ============================================================
-- 4. PARTNERS: cac doi tac/nha thau trong mang luoi
-- ============================================================
-- PRIMARY KEY (PK):
--   id  -> uniquely identifies each partner/trade contractor
--
-- FOREIGN KEYS (FK):
--   (none in this table — partners is a root/parent table)
--
-- RELATIONSHIPS:
--   partners  * ----<>---- *  projects     (many-to-many via project_partners)
-- ============================================================
CREATE TABLE partners (
    id SERIAL PRIMARY KEY,                  -- PK
    company_name VARCHAR(150) NOT NULL,
    abn VARCHAR(20),
    contact_name VARCHAR(150),
    contact_phone VARCHAR(20),
    contact_email VARCHAR(150),
    trade_type VARCHAR(50), -- vd: 'builder', 'electrician', 'plumber', 'concreter'
    active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMP NOT NULL DEFAULT now()
);

-- ============================================================
-- 5. PROJECTS: du an Granny Flat cu the
-- ============================================================
-- PRIMARY KEY (PK):
--   id  -> uniquely identifies each build project
--
-- FOREIGN KEYS (FK):
--   client_id      ->  clients(id)        (required)
--   sales_rep_id   ->  users(id)          (nullable)
--
-- RELATIONSHIPS:
--   projects  * ----> 1  clients           (many projects belong to one client)
--   projects  * ----> 1  users             (many projects assigned to one sales rep)
--   projects  1 ----< *  project_stage_progress   (one project, many stage progress rows)
--   projects  * ----<>---- *  partners     (many-to-many via project_partners)
--   projects  1 ----< *  project_updates   (one project, many site update logs)
--   projects  1 ----< *  commissions       (one project, many commission records)
-- ============================================================
CREATE TABLE projects (
    id SERIAL PRIMARY KEY,                        -- PK
    client_id INTEGER NOT NULL REFERENCES clients(id),       -- FK -> clients.id
    sales_rep_id INTEGER REFERENCES users(id),               -- FK -> users.id
    contract_value NUMERIC(12, 2),
    contract_signed_date DATE,
    status VARCHAR(20) NOT NULL DEFAULT 'planning'
        CHECK (status IN ('planning', 'in_progress', 'completed', 'on_hold')),
    created_at TIMESTAMP NOT NULL DEFAULT now()
);

-- ============================================================
-- 6. PROJECT_STAGES: bang tra cuu cac giai doan xay dung chuan
-- ============================================================
-- PRIMARY KEY (PK):
--   id  -> uniquely identifies each standard construction stage
--
-- FOREIGN KEYS (FK):
--   (none — this is a lookup/reference table)
--
-- RELATIONSHIPS:
--   project_stages  1 ----< *  project_stage_progress
--                   (one stage definition used by many project progress rows)
--
-- NOTE: This table stores the master list of stages (site_prep, slab, frame...).
--       It does NOT store per-project progress — that lives in project_stage_progress.
-- ============================================================
CREATE TABLE project_stages (
    id SERIAL PRIMARY KEY,                  -- PK
    stage_name VARCHAR(50) NOT NULL UNIQUE, -- site_prep, slab, frame, lockup, fitout, handover
    sequence_order INTEGER NOT NULL,
    typical_duration_days INTEGER
);

-- ============================================================
-- 7. PROJECT_STAGE_PROGRESS: tien do thuc te cua tung du an qua tung giai doan
-- ============================================================
-- PRIMARY KEY (PK):
--   id  -> uniquely identifies each progress row
--
-- FOREIGN KEYS (FK):
--   project_id  ->  projects(id)           (required, ON DELETE CASCADE)
--   stage_id    ->  project_stages(id)     (required)
--
-- RELATIONSHIPS:
--   project_stage_progress  * ----> 1  projects        (many rows per project)
--   project_stage_progress  * ----> 1  project_stages  (many rows per stage definition)
--
-- CARDINALITY (combined):
--   projects  * ----<>---- *  project_stages   (many-to-many)
--   Resolved through this junction/associative table, which also stores
--   planned dates, actual dates, and status for each project-stage pair.
--
-- CONSTRAINT:
--   UNIQUE (project_id, stage_id)  -> each project can only have ONE progress
--   row per stage (prevents duplicate stage entries for the same project)
-- ============================================================
CREATE TABLE project_stage_progress (
    id SERIAL PRIMARY KEY,                                      -- PK
    project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,  -- FK -> projects.id
    stage_id INTEGER NOT NULL REFERENCES project_stages(id),                -- FK -> project_stages.id
    planned_start_date DATE,
    planned_end_date DATE,
    actual_start_date DATE,
    actual_end_date DATE,
    status VARCHAR(20) NOT NULL DEFAULT 'not_started'
        CHECK (status IN ('not_started', 'in_progress', 'completed', 'delayed')),
    UNIQUE (project_id, stage_id)
);

-- ============================================================
-- 8. PROJECT_PARTNERS: bang trung gian (nhieu-nhieu) noi du an voi doi tac
-- ============================================================
-- PRIMARY KEY (PK):
--   id  -> uniquely identifies each project-partner assignment
--
-- FOREIGN KEYS (FK):
--   project_id  ->  projects(id)           (required, ON DELETE CASCADE)
--   partner_id  ->  partners(id)           (required)
--
-- RELATIONSHIPS:
--   project_partners  * ----> 1  projects   (many assignment rows per project)
--   project_partners  * ----> 1  partners   (many assignment rows per partner)
--
-- CARDINALITY (combined):
--   projects  * ----<>---- *  partners       (many-to-many)
--   One project can have many partners (concreter, electrician, etc.).
--   One partner can work on many projects.
--   This junction table also stores trade_role and agreed_price per assignment.
--
-- CONSTRAINT:
--   UNIQUE (project_id, partner_id, trade_role)
--   -> the same partner cannot be assigned the same trade role twice on one project
-- ============================================================
CREATE TABLE project_partners (
    id SERIAL PRIMARY KEY,                                      -- PK
    project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,  -- FK -> projects.id
    partner_id INTEGER NOT NULL REFERENCES partners(id),                    -- FK -> partners.id
    trade_role VARCHAR(50), -- vd: 'concreting', 'framing', 'electrical'
    agreed_price NUMERIC(12, 2),
    UNIQUE (project_id, partner_id, trade_role)
);

-- ============================================================
-- 9. PROJECT_UPDATES: nhat ky cap nhat tien do (anh, ghi chu tu hien truong)
-- ============================================================
-- PRIMARY KEY (PK):
--   id  -> uniquely identifies each site update entry
--
-- FOREIGN KEYS (FK):
--   project_id  ->  projects(id)           (required, ON DELETE CASCADE)
--   posted_by   ->  users(id)              (nullable — who wrote the update)
--
-- RELATIONSHIPS:
--   project_updates  * ----> 1  projects   (many updates belong to one project)
--   project_updates  * ----> 1  users       (many updates posted by one user)
-- ============================================================
CREATE TABLE project_updates (
    id SERIAL PRIMARY KEY,                                      -- PK
    project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,  -- FK -> projects.id
    posted_by INTEGER REFERENCES users(id),                                 -- FK -> users.id
    update_text TEXT,
    photo_url TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT now()
);

-- ============================================================
-- 10. COMMISSIONS: hoa hong cho sales rep theo tung du an
-- ============================================================
-- PRIMARY KEY (PK):
--   id  -> uniquely identifies each commission record
--
-- FOREIGN KEYS (FK):
--   project_id     ->  projects(id)        (required, ON DELETE CASCADE)
--   sales_rep_id   ->  users(id)           (required)
--
-- RELATIONSHIPS:
--   commissions  * ----> 1  projects       (many commission rows per project)
--   commissions  * ----> 1  users          (many commission rows per sales rep)
-- ============================================================
CREATE TABLE commissions (
    id SERIAL PRIMARY KEY,                                      -- PK
    project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,  -- FK -> projects.id
    sales_rep_id INTEGER NOT NULL REFERENCES users(id),                     -- FK -> users.id
    commission_amount NUMERIC(10, 2) NOT NULL,
    paid BOOLEAN NOT NULL DEFAULT false,
    paid_date DATE
);

-- ============================================================
-- RELATIONSHIP MAP (quick reference)
-- ============================================================
-- users          1 ----< *   leads
-- users          1 ----< *   projects
-- users          1 ----< *   project_updates
-- users          1 ----< *   commissions
--
-- leads          1 ----< *   clients
-- clients        1 ----< *   projects
--
-- projects       * ----<>---- *   partners          (via project_partners)
-- projects       * ----<>---- *   project_stages    (via project_stage_progress)
--
-- projects       1 ----< *   project_stage_progress
-- projects       1 ----< *   project_partners
-- projects       1 ----< *   project_updates
-- projects       1 ----< *   commissions
--
-- project_stages 1 ----< *   project_stage_progress
-- partners       1 ----< *   project_partners
-- ============================================================

-- ============================================================
-- DU LIEU MAU CHO PROJECT_STAGES (cac giai doan chuan Granny Flat)
-- ============================================================
INSERT INTO project_stages (
	stage_name, 
	sequence_order, 
	typical_duration_days
) 
VALUES
(
	'site_prep', 
	1, 
	5
),
(
	'slab', 
	2, 
	7
),
(
	'frame', 
	3, 
	10
),
(
	'lockup', 
	4, 
	14
),
(
	'fitout', 
	5, 
	21
),
(
	'handover', 
	6, 
	3
);

-- ============================================================
-- VI DU TRUY VAN HUU ICH
-- ============================================================

-- Xem tien do tat ca du an dang "in_progress", sap xep theo giai doan
-- SELECT p.id, c.first_name || ' ' || c.last_name AS client_name, ps.stage_name, psp.status, psp.planned_end_date
-- FROM projects p
-- JOIN clients c ON c.id = p.client_id
-- JOIN project_stage_progress psp ON psp.project_id = p.id
-- JOIN project_stages ps ON ps.id = psp.stage_id
-- WHERE p.status = 'in_progress'
-- ORDER BY p.id, ps.sequence_order;

-- Ty le chuyen doi lead -> khach hang theo tung sales rep
-- SELECT u.first_name || ' ' || u.last_name AS sales_rep_name,
--        COUNT(*) AS total_leads,
--        COUNT(*) FILTER (WHERE l.status = 'won') AS won_leads,
--        ROUND(COUNT(*) FILTER (WHERE l.status = 'won')::numeric / COUNT(*) * 100, 1) AS conversion_pct
-- FROM leads l
-- JOIN users u ON u.id = l.assigned_sales_id
-- GROUP BY u.first_name, u.last_name;
