# Granny Flat Manager

Internal business tool for managing **Granny Flat** construction projects in Australia — covering sales CRM, construction progress tracking, trade partners, and reporting.

**Stack:** Django 5.2 · PostgreSQL · Django Templates

**Repository:** [github.com/nicknguyen-991/granny_flat_manager](https://github.com/nicknguyen-991/granny_flat_manager)

---

## What this app does

| Domain | Purpose |
|--------|---------|
| **CRM** | Track leads, convert won leads to clients |
| **Construction** | Manage projects, build stages, site updates |
| **Partners** | Assign trade partners to projects |
| **Reporting** | Dashboards (planned — queries existing tables) |

Database design follows **3NF** (Third Normal Form). Schema docs: `granny-flat-schema.md` and `granny-flat-schema.sql`.

---

## Project structure

```
granny_flat_manager/
├── accounts/          # Staff (admin, sales, site manager)
├── crm/               # Leads, clients, commissions
├── construction/      # Projects, stages, progress, site updates
├── partners/          # Trade partners + project assignments
├── reporting/         # Dashboards (Phase 4)
├── config/            # Django settings, URLs
├── templates/         # HTML templates
├── static/            # CSS, JS (Admin UX + CRM UI)
├── granny-flat-schema.sql
├── manage.py
└── requirements.txt
```

---

## Prerequisites

- **Python 3.13+**
- **PostgreSQL** (local install with pgAdmin, or hosted)
- **Git** (optional — for cloning the repo)

---

## First-time setup

### 1. Clone or open the project

```powershell
cd <PATH TO THE PROJECT>\granny_flat_manager
```

Example:

```powershell
cd C:\cursor_projects\granny_flat_manager
```

### 2. Create and activate virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

### 4. Configure environment variables

Copy the example file and edit your PostgreSQL password:

```powershell
copy .env.example .env
```

Edit `.env`:

```env
POSTGRES_DB=granny_flat
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password_here
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
```

> **Note:** The project folder is `granny_flat_manager`, but your PostgreSQL database name (`POSTGRES_DB`) can stay as `granny_flat` if that database already exists locally.

### 5. Create PostgreSQL database (if needed)

In pgAdmin or `psql`:

```sql
CREATE DATABASE granny_flat;
```

Optionally run `granny-flat-schema.sql` manually, or let Django migrations create tables (recommended).

### 6. Run migrations

```powershell
python manage.py migrate
```

### 7. Create an admin user

```powershell
python manage.py createsuperuser
```

---

## Run the development server

```powershell
cd <PATH TO THE PROJECT>\granny_flat_manager
.\.venv\Scripts\Activate.ps1
python manage.py runserver
```

Then open in your browser:

| URL | Page |
|-----|------|
| [http://127.0.0.1:8000/](http://127.0.0.1:8000/) | Redirects to Leads |
| [http://127.0.0.1:8000/leads/](http://127.0.0.1:8000/leads/) | CRM — Lead list (table view) |
| [http://127.0.0.1:8000/leads/pipeline/](http://127.0.0.1:8000/leads/pipeline/) | CRM — Sales pipeline (Kanban) |
| [http://127.0.0.1:8000/clients/](http://127.0.0.1:8000/clients/) | CRM — Client list |
| [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/) | Django Admin |

Press `Ctrl+C` in the terminal to stop the server.

---

## Roadmap

### Phase 0 — Design & database ✅

- [x] 3NF schema (10 tables)
- [x] PostgreSQL setup
- [x] Schema documentation (`granny-flat-schema.md`, `.sql`)

### Phase 1 — Django foundation ✅

- [x] Django project + PostgreSQL connection
- [x] Domain apps: `accounts`, `crm`, `construction`, `partners`, `reporting`
- [x] Django models matching schema
- [x] Migrations + seed construction stages
- [x] Django Admin for all models
- [x] Admin UX polish (column autofit, row links, sidebar ordering)

### Phase 2 — Sales CRM ✅

- [x] Lead list with status filter and search
- [x] Lead detail, create, edit
- [x] Convert won lead → client
- [x] Client list, detail, create, and edit pages
- [x] Sales pipeline / Kanban view with in-board status updates

### Phase 3 — Construction tracking 🔄 Next

- [ ] Project list and detail pages
- [ ] Stage progress board
- [ ] Assign partners to projects
- [ ] Site updates (notes / photos)

### Phase 4 — Reporting dashboard ⬜ Planned

- [ ] Lead conversion by sales rep
- [ ] Jobs in progress
- [ ] Revenue overview
- [ ] Commission summary

### Phase 5 — Deploy ⬜ Planned

- [ ] Host on Railway or Render
- [ ] Production PostgreSQL
- [ ] Environment variables and smoke tests

---

## Database tables (overview)

| Table | Purpose |
|-------|---------|
| `users` | Internal staff |
| `leads` | Prospective customers |
| `clients` | Confirmed customers |
| `partners` | Trade subcontractors |
| `projects` | Granny Flat build jobs |
| `project_stages` | Standard build milestones |
| `project_stage_progress` | Per-project stage progress |
| `project_partners` | Project ↔ partner assignments |
| `project_updates` | Site diary entries |
| `commissions` | Sales commissions |

---

## Useful commands

```powershell
# Check project for errors
python manage.py check

# Apply new migrations after model changes
python manage.py migrate

# Open Django shell
python manage.py shell
```

---

## License

Private / internal use — Granny Flat construction company, Australia.
