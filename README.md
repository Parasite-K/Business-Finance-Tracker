# Business Finance Tracker

A Python-based business finance management application built as a learning project to develop practical software engineering and backend development skills.

The project started as a simple console application and is being progressively developed toward a production-ready business finance platform.

## Current Features

### Transactions
- Add income transactions
- Add expense transactions
- View transactions
- Edit transactions
- Delete transactions
- Assign transactions to projects
- Support for unassigned transactions

### Projects
- Create projects
- View projects
- Edit projects
- Delete projects
- Associate transactions with projects
- Project-level financial statistics
- Prevent deletion of projects with associated transactions

### Reports
- Overall financial summary
- Monthly financial reports
- Yearly financial reports
- Category-based reports
- Income and expense breakdown
- Profit/loss calculations

### Data & Validation
- PostgreSQL database persistence
- Input validation for dates, amounts, transaction types, categories, months, and years
- PostgreSQL constraints for data integrity
- Parameterized SQL queries
- PostgreSQL JOINs and aggregate queries

## Technologies

- Python
- PostgreSQL
- psycopg3
- Git
- GitHub
- python-dotenv

## Architecture

The application currently follows a modular structure:

main.py
├── projects.py
├── transactions.py
├── reports.py
├── validation.py
└── storage.py
        │
        ↓
   PostgreSQL


- main.py — application navigation and CLI interface
- transactions.py — transaction operations
- projects.py — project operations
- reports.py — financial reporting and analytical queries
- validation.py — input validation
- storage.py — PostgreSQL database access

Database-specific logic is isolated primarily within the storage layer to make future backend development and infrastructure changes easier.

## Planned Features
- Backend
- FastAPI backend
- REST API
- User authentication and accounts
- Business-specific data separation
- Production database deployment

## Frontend
- Web-based business dashboard
- Transaction management interface
- Project management
- Financial charts and visualizations
- Search and filtering
- Business Features
- Client management
- Invoicing
- GST-related functionality
- Advanced financial reporting

## AI Features
- AI-powered financial analysis
- atural-language financial queries
- Automated invoice/receipt data extraction
- AI-assisted business insights