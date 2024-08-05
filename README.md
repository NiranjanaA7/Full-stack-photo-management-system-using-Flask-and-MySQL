# Full-stack-photo-management-system-using-Flask-and-MySQL

## Overview

This is a simple photo sharing platform built using Flask and MySQL. Users can upload, view, and manage photos, as well as follow other users. The platform supports user authentication, profile management, search functionality, and allows users to download images as Polaroids with customized text.

## Features

- **User Authentication:** Register, login, and edit user profile.
- **Photo Uploading:** Upload photos with titles and descriptions.
- **User Profiles:** View and edit user profiles, including profile pictures.
- **Follow/Unfollow:** Follow or unfollow other users.
- **Search:** Search for users and photos based on keywords.
- **Photo Management:** Edit and delete uploaded photos.
- **Download as Polaroid:** Download photos as Polaroid-style images with customizable text.
- **Account Deletion:** Delete user accounts and all associated data.

## Requirements

- Python 3.x
- Flask
- Flask-MySQLdb
- Flask-Bcrypt
- Werkzeug

## Setup

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/photo-sharing-platform.git
   cd photo-sharing-platform
   ```

2. **Create a Virtual Environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Create and Configure the Database:**

   - Ensure MySQL is installed and running.
   - Create a new database and configure the `config.py` file with your database credentials.

5. **Run the Application:**

   ```bash
   python app.py
   ```

   By default, the application will run on `http://127.0.0.1:5000/`.

## Configuration

Edit `config.py` to configure your MySQL database connection. Example configuration:

```python
# config.py
MYSQL_HOST = 'localhost'
MYSQL_USER = 'yourusername'
MYSQL_PASSWORD = 'yourpassword'
MYSQL_DB = 'photo_sharing_db'
SECRET_KEY = 'your_secret_key'
```

## File Uploads

Ensure that the `static/images` and `static/profile_pics` directories exist and have the correct permissions for file uploads.

## Project Structure

```
photo-sharing-platform/
│
├── app.py                  # Main application file
├── config.py               # Configuration file for database and secrets
├── requirements.txt        # Python package dependencies
├── static/
│   ├── images/             # Directory for photo uploads
│   └── profile_pics/       # Directory for profile pictures
└── templates/
    ├── home.html           # Home page template
    ├── login.html          # Login page template
    ├── register.html       # Registration page template
    ├── profile.html        # User profile page template
    ├── search.html         # Search results page template
    ├── upload.html         # Photo upload page template
    ├── edit_profile.html   # Profile editing page template
    ├── edit_image.html     # Image editing page template
    └── download.html       # Polaroid download page template (if applicable)
```

## SQL Schema

Here are the SQL comments for your database schema:

```sql
--Accounts Table
CREATE TABLE accounts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(100) NOT NULL
);

-- Photos Table
CREATE TABLE photos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    filename VARCHAR(255) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES accounts(id)
);

-- Followers Table
CREATE TABLE followers (
    follower_id INT NOT NULL,
    followee_id INT NOT NULL,
    PRIMARY KEY (follower_id, followee_id),
    FOREIGN KEY (follower_id) REFERENCES accounts(id) ON DELETE CASCADE,
    FOREIGN KEY (followee_id) REFERENCES accounts(id) ON DELETE CASCADE
);

```
