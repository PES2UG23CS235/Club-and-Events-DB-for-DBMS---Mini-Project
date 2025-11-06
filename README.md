# Club & Event Management System


A comprehensive database management system for managing college clubs, events, student registrations, and payments with role-based access control.

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Database Schema](#database-schema)
- [Installation](#installation)
- [Usage](#usage)
- [User Roles](#user-roles)
- [Screenshots](#screenshots)
- [Database Features](#database-features)
- [Contributors](#contributors)

## Overview

This project is a full-stack database application designed to streamline the management of college clubs and events. It provides a user-friendly GUI interface with authentication and role-based access control, allowing faculty advisors and students to interact with the system according to their privileges.

**Course**: Database Management Systems (DBMS) Lab  
**Institution**: PES University  
**Academic Year**: 2024-2025

## Features

### Core Functionality
- **User Authentication**: Secure login system for Faculty and Students
- **Role-Based Access Control**: Different privileges for different user types
- **Event Management**: Create, view, and manage college events
- **Student Registration**: Register students for events with payment tracking
- **Payment Processing**: Track and update payment status with automatic triggers
- **Report Generation**: Comprehensive event and student analytics

### Advanced Features
- **Database Triggers**: Automatic updates for venue booking, payment confirmation, and age calculation
- **Stored Procedures**: Complex operations like student registration
- **Custom Functions**: Event statistics and revenue calculations
- **Complete CRUD Operations**: Full Create, Read, Update, Delete functionality for all tables

## Technologies Used

- **Backend**: Python 3.12
- **Database**: MySQL 8.0
- **GUI Framework**: Tkinter (built-in)
- **Database Connector**: mysql-connector-python
- **Version Control**: Git & GitHub

## Database Schema

### Tables (10 total)
1. **facultyadvisor** - Faculty information and credentials
2. **student** - Student information and credentials
3. **venue** - Event venues and their availability
4. **sponsor** - Event sponsors
5. **club** - College clubs (depends on facultyadvisor)
6. **event** - Events organized by clubs (depends on venue, club)
7. **membership** - Student club memberships (depends on student, club)
8. **eventregistration** - Event registrations (depends on student, event)
9. **payment** - Payment records (depends on eventregistration)
10. **sponsoredby** - Event sponsorships (depends on event, sponsor)

### ER Diagram
![ER Diagram](database/ER_Diagram.png)

## Installation

### Prerequisites
```bash
- Python 3.8 or higher
- MySQL 8.0 or higher
- pip (Python package manager)
```

### Steps

1. **Clone the repository**
```bash
git clone https://github.com/YOUR_USERNAME/club-event-management-system.git
cd club-event-management-system
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up the database**
```bash
# Login to MySQL
mysql -u root -p

# Create database and import schema
mysql -u root -p < database/schema.sql

# Import sample data (optional)
mysql -u root -p club_and_event < database/sample_data.sql

# Create triggers, procedures, and functions
mysql -u root -p club_and_event < database/triggers.sql
mysql -u root -p club_and_event < database/procedures_functions.sql
```

4. **Configure database connection**
Edit `src/main.py` and update the database credentials:
```python
self.db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'YOUR_PASSWORD',  # Change this
    'database': 'club_and_event'
}
```

5. **Run the application**
```bash
python src/main.py
```

## Usage

### Default Login Credentials

**Faculty Advisor:**
- User ID: `1`
- Password: `default123`

**Student:**
- User ID: `1`
- Password: `default123`

### First Time Setup
After installation, you can:
1. Login with default credentials
2. Add new faculty/students through the GUI
3. Create clubs and events
4. Register students for events

## User Roles

### Faculty Advisor (Full Access)
-  Create, Read, Update, Delete operations on all tables
-  Register students for events
-  Update payment status
-  Add new students and faculty
-  Delete registrations
-  Generate reports
-  Access all 7 tabs

### Student (Read-Only Access)
-  View all data (Read operations only)
-  View event reports and analytics
-  View student participation data
-  Cannot create, update, or delete records
-  Cannot access faculty-only operations
-  Access 3 tabs (Reports, Student Info, CRUD view-only)

## Screenshots

### Login Page
![Login](screenshots/login_page.png)

### Faculty Dashboard
![Faculty Dashboard](screenshots/faculty_dashboard.png)

### Student Dashboard
![Student Dashboard](screenshots/student_dashboard.png)

### CRUD Operations
![CRUD](screenshots/crud_operations.png)

### Event Reports
![Reports](screenshots/event_reports.png)

## Database Features

### Triggers (4)
1. **trg_update_venue_status** - Auto-books venue when event is created
2. **update_attendance_after_payment** - Confirms attendance when payment completed
3. **update_payment_status_after_attendance** - Completes payment when attendance confirmed
4. **update_age_before_insert** - Auto-calculates student age from date of birth

### Stored Procedures (2)
1. **register_student_for_event** - Handles complete student registration process
2. **generate_event_report** - Generates comprehensive event statistics

### Functions (3)
1. **get_total_registrations(event_id)** - Returns registration count for an event
2. **get_total_revenue(event_id)** - Calculates total revenue from completed payments
3. **get_event_count_for_student(student_id)** - Returns number of events attended by student

### Complex Queries
- JOIN operations for multi-table data retrieval
- Aggregate functions (COUNT, SUM) for statistics
- Nested queries for dependent data
- GROUP BY for report generation

##  Documentation
Detailed documentation available in the `docs/` folder:
- **User Requirement Specification** - Complete project requirements
- **Project Report** - Comprehensive project documentation
- **Installation Guide** - Step-by-step setup instructions

## Contributors

- **[Your Name]** - [Your Roll Number]
- **[Teammate Name]** - [Teammate Roll Number]

**Course Instructor**: [Professor Name]  
**Institution**: PES University

## License

This project is created for academic purposes as part of the DBMS Lab course at PES University.

## Acknowledgments

- PES University DBMS Lab faculty
- Course instructors and teaching assistants
- MySQL documentation
- Python Tkinter documentation

## Contact

For queries or suggestions:
- Email: [your.email@university.edu]
- GitHub: [@your_username](https://github.com/your_username)

---

**Note**: This is an academic project. Default passwords should be changed for production use.
```

---

### **2. `.gitignore`** (Files to exclude from Git)
```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
*.egg-info/
dist/
build/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Database
*.sql.backup
*.db

# Sensitive information
config.ini
secrets.py
*.log

# Documentation
*.pdf
*.docx
~$*.docx

# Screenshots (optional - remove if you want to track them)
# screenshots/
```

---

### **3. `requirements.txt`** (Python dependencies)
```
mysql-connector-python==8.2.0
