# Full-stack-photo-management-system-using-Flask-and-MySQL
## Overview

This is a simple photo sharing platform built using Flask and MySQL. Users can upload, view, and manage photos, as well as follow other users. The platform supports user authentication, profile management, and search functionality.

## Features

- **User Authentication:** Register, login, and edit user profile.
- **Photo Uploading:** Upload photos with titles and descriptions.
- **User Profiles:** View and edit user profiles, including profile pictures.
- **Follow/Unfollow:** Follow or unfollow other users.
- **Search:** Search for users and photos based on keywords.
- **Photo Management:** Edit and delete uploaded photos.
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
    └── edit_image.html     # Image editing page template
```

## Contributing

Feel free to fork the repository and submit pull requests. Please ensure to follow the existing code style and include tests for new features.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For any questions or issues, please contact [your-email@example.com](mailto:your-email@example.com).
```

You can paste this directly into your README file. Adjust the placeholders as needed!
