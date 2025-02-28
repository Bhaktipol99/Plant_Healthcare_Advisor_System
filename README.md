# Plant Healthcare Advisor System

## Overview
The **Plant Healthcare Advisor System** is a web-based application developed using **Flask**, **HTML**, **CSS**, and an **SQLite** database. This system allows both **users** and **admins** to interact with the platform for diagnosing plant diseases, managing plant data, and getting treatment recommendations.

## Features
### User Features:
- **User Registration**: Users can create an account by providing necessary details (username, email, password).
- **User Login**: Existing users can log in to the system.
- **CRUD Operations for User**: Users can perform **Create**, **Read**, **Update**, and **Delete** operations on their profiles and plant health records.
- **Disease Diagnosis**: Users can input plant symptoms or upload images to diagnose plant diseases.
- **Treatment Suggestions**: Based on the diagnosis, users are provided with treatment options for the affected plant.

### Admin Features:
- **Admin Login**: Admins have a special login to access the admin panel.
- **Admin CRUD Operations**: Admins can perform **Create**, **Read**, **Update**, and **Delete** operations on plant records, user profiles, and disease data.
- **Manage Users**: Admins can manage users, including activating or deactivating user accounts.
- **Manage Plant Data**: Admins can add, update, or remove plant records and their associated diseases and treatments.
- **View User Diagnoses**: Admins can access and review diagnoses performed by users.

## Technologies Used
- **Frontend**: HTML, CSS (for responsive web design)
- **Backend**: Python with Flask (for web framework and server-side logic)
- **Database**: SQLite (for storing plant data, diagnoses, treatment information, and user profiles)
- **Version Control**: Git and GitHub (for version control)

## Installation

### Prerequisites:
- **Python 3.11.0** (You can download it from [python.org](https://www.python.org/downloads/))
- **Flask 3.1.0**
- **Werkzeug 3.1.3**
- **SQLite** (SQLite comes built-in with Python)
- **Git** (For version control)

### Steps:
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Bhaktipol99/Plant_Healthcare_Advisor.git
