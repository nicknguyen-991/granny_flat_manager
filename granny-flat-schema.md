# Database schema: Công cụ quản lý đối tác xây dựng Granny Flat

## Nguyên tắc thiết kế

Dữ liệu được tách thành các bảng theo đúng tinh thần chuẩn hóa 3NF (Third Normal Form) — mỗi bảng chỉ chứa thông tin về một loại thực thể, tránh lặp dữ liệu:

- **leads** tách biệt với **clients**: một lead có thể chưa bao giờ thành khách hàng (mất lead), nên không nên nhét chung vào bảng clients.
- **projects** và **partners** liên kết qua bảng trung gian **project_partners** (quan hệ nhiều-nhiều) vì một dự án Granny Flat thường cần nhiều đối tác khác nhau (đổ móng, khung, điện, nước...) chứ không chỉ một.
- **project_stages** là bảng "lookup" chứa các giai đoạn chuẩn (site prep → slab → frame → lock-up → fit-out → handover), còn **project_stage_progress** mới là bảng lưu tiến độ thực tế của từng dự án — tách ra để không lặp lại định nghĩa giai đoạn cho mỗi dự án.

## Các bảng chính trong schema

- **users** — nhân viên nội bộ (admin, sales, quản lý công trình)
- **leads** — khách hàng tiềm năng, trước khi ký hợp đồng
- **clients** — khách hàng chính thức (sau khi lead chuyển đổi thành công)
- **partners** — các đối tác/nhà thầu trong mạng lưới
- **projects** — dự án Granny Flat cụ thể
- **project_stages** — bảng tra cứu các giai đoạn xây dựng chuẩn
- **project_stage_progress** — tiến độ thực tế của từng dự án qua từng giai đoạn
- **project_partners** — bảng trung gian (nhiều-nhiều) nối dự án với đối tác
- **project_updates** — nhật ký cập nhật tiến độ (ảnh, ghi chú từ hiện trường)
- **commissions** — hoa hồng cho sales rep theo từng dự án

## Ràng buộc quan trọng

- **project_stage_progress** có ràng buộc `UNIQUE (project_id, stage_id)` — đảm bảo mỗi dự án chỉ có một dòng tiến độ cho mỗi giai đoạn, tránh dữ liệu trùng lặp.
- **project_partners** là bảng trung gian giải quyết quan hệ nhiều-nhiều — một dự án có nhiều đối tác, một đối tác có thể tham gia nhiều dự án.

## Mã nguồn SQL đầy đủ

```sql
-- ============================================================
-- SCHEMA: Cong cu quan ly doi tac xay dung Granny Flat
-- Database: PostgreSQL
-- Thiet ke theo chuan 3NF (Third Normal Form)
-- ============================================================

-- 1. USERS: nhan vien noi bo (admin, sales, quan ly cong trinh)
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(75) NOT NULL,
    last_name VARCHAR(75) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    phone VARCHAR(20),
    role VARCHAR(20) NOT NULL CHECK (role IN ('admin', 'sales', 'site_manager')),
    created_at TIMESTAMP NOT NULL DEFAULT now()
);

-- 2. LEADS: khach hang tiem nang, truoc khi ky hop dong
CREATE TABLE leads (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(75) NOT NULL,
    last_name VARCHAR(75) NOT NULL,
    phone VARCHAR(20),
    email VARCHAR(150),
    source VARCHAR(30) CHECK (source IN ('google_ads', 'referral', 'walk_in', 'website', 'other')),
    assigned_sales_id INTEGER REFERENCES users(id),
    status VARCHAR(20) NOT NULL DEFAULT 'new'
        CHECK (status IN ('new', 'contacted', 'quoted', 'won', 'lost')),
    notes TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT now()
);

-- 3. CLIENTS: khach hang chinh thuc (sau khi lead chuyen doi thanh cong)
CREATE TABLE clients (
    id SERIAL PRIMARY KEY,
    lead_id INTEGER REFERENCES leads(id),
    first_name VARCHAR(75) NOT NULL,
    last_name VARCHAR(75) NOT NULL,
    phone VARCHAR(20),
    email VARCHAR(150),
    site_address TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT now()
);

-- 4. PARTNERS: cac doi tac/nha thau trong mang luoi
CREATE TABLE partners (
    id SERIAL PRIMARY KEY,
    company_name VARCHAR(150) NOT NULL,
    abn VARCHAR(20),
    contact_name VARCHAR(150),
    contact_phone VARCHAR(20),
    contact_email VARCHAR(150),
    trade_type VARCHAR(50), -- vd: 'builder', 'electrician', 'plumber', 'concreter'
    active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMP NOT NULL DEFAULT now()
);

-- 5. PROJECTS: du an Granny Flat cu the
CREATE TABLE projects (
    id SERIAL PRIMARY KEY,
    client_id INTEGER NOT NULL REFERENCES clients(id),
    sales_rep_id INTEGER REFERENCES users(id),
    contract_value NUMERIC(12, 2),
    contract_signed_date DATE,
    status VARCHAR(20) NOT NULL DEFAULT 'planning'
        CHECK (status IN ('planning', 'in_progress', 'completed', 'on_hold')),
    created_at TIMESTAMP NOT NULL DEFAULT now()
);

-- 6. PROJECT_STAGES: bang tra cuu cac giai doan xay dung chuan
CREATE TABLE project_stages (
    id SERIAL PRIMARY KEY,
    stage_name VARCHAR(50) NOT NULL UNIQUE, -- site_prep, slab, frame, lockup, fitout, handover
    sequence_order INTEGER NOT NULL,
    typical_duration_days INTEGER
);

-- 7. PROJECT_STAGE_PROGRESS: tien do thuc te cua tung du an qua tung giai doan
CREATE TABLE project_stage_progress (
    id SERIAL PRIMARY KEY,
    project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    stage_id INTEGER NOT NULL REFERENCES project_stages(id),
    planned_start_date DATE,
    planned_end_date DATE,
    actual_start_date DATE,
    actual_end_date DATE,
    status VARCHAR(20) NOT NULL DEFAULT 'not_started'
        CHECK (status IN ('not_started', 'in_progress', 'completed', 'delayed')),
    UNIQUE (project_id, stage_id)
);

-- 8. PROJECT_PARTNERS: bang trung gian (nhieu-nhieu) noi du an voi doi tac
CREATE TABLE project_partners (
    id SERIAL PRIMARY KEY,
    project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    partner_id INTEGER NOT NULL REFERENCES partners(id),
    trade_role VARCHAR(50), -- vd: 'concreting', 'framing', 'electrical'
    agreed_price NUMERIC(12, 2),
    UNIQUE (project_id, partner_id, trade_role)
);

-- 9. PROJECT_UPDATES: nhat ky cap nhat tien do (anh, ghi chu tu hien truong)
CREATE TABLE project_updates (
    id SERIAL PRIMARY KEY,
    project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    posted_by INTEGER REFERENCES users(id),
    update_text TEXT,
    photo_url TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT now()
);

-- 10. COMMISSIONS: hoa hong cho sales rep theo tung du an
CREATE TABLE commissions (
    id SERIAL PRIMARY KEY,
    project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    sales_rep_id INTEGER NOT NULL REFERENCES users(id),
    commission_amount NUMERIC(10, 2) NOT NULL,
    paid BOOLEAN NOT NULL DEFAULT false,
    paid_date DATE
);

-- ============================================================
-- DU LIEU MAU CHO PROJECT_STAGES (cac giai doan chuan Granny Flat)
-- ============================================================
INSERT INTO project_stages (stage_name, sequence_order, typical_duration_days) VALUES
    ('site_prep', 1, 5),
    ('slab', 2, 7),
    ('frame', 3, 10),
    ('lockup', 4, 14),
    ('fitout', 5, 21),
    ('handover', 6, 3);

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
```
