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
-- Users Table
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY, -- User ID
    username VARCHAR(50) NOT NULL,     -- Username
    password VARCHAR(255) NOT NULL,    -- Password (hashed)
    email VARCHAR(100) NOT NULL,       -- User email
    profile_pic VARCHAR(255),          -- Profile picture filename
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Account creation timestamp
    UNIQUE(email)
);

-- Photos Table
CREATE TABLE photos (
    id INT AUTO_INCREMENT PRIMARY KEY, -- Photo ID
    user_id INT NOT NULL,              -- Foreign key to users table
    filename VARCHAR(255) NOT NULL,    -- Filename of the photo
    title VARCHAR(100),                -- Title of the photo
    description TEXT,                  -- Description of the photo
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Timestamp when photo was uploaded
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Followers Table
CREATE TABLE followers (
    id INT AUTO_INCREMENT PRIMARY KEY, -- Record ID
    follower_id INT NOT NULL,          -- ID of the user who follows
    followee_id INT NOT NULL,          -- ID of the user being followed
    FOREIGN KEY (follower_id) REFERENCES users(id),
    FOREIGN KEY (followee_id) REFERENCES users(id),
    UNIQUE(follower_id, followee_id)   -- Ensure no duplicate follow relationships
);

-- Sessions Table (Optional for user sessions)
CREATE TABLE sessions (
    id INT AUTO_INCREMENT PRIMARY KEY, -- Session ID
    user_id INT NOT NULL,              -- User ID
    session_token VARCHAR(255) NOT NULL, -- Session token
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Session creation timestamp
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```
