#Flask-Based Photo Sharing Platform with MySQL Integration
import os
import re
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
import MySQLdb.cursors
from werkzeug.utils import secure_filename
from flask_bcrypt import Bcrypt

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py')

mysql = MySQL(app)
bcrypt = Bcrypt(app)

# Ensure the upload directory exists
os.makedirs('static/images', exist_ok=True)
os.makedirs('static/profile_pics', exist_ok=True)

# Allowed file extensions for profile pictures
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def is_following(follower_id, followee_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM followers WHERE follower_id = %s AND followee_id = %s', (follower_id, followee_id))
    following = cursor.fetchone()
    cursor.close()
    return following is not None

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/search', methods=['POST'])
def search():
    keyword = request.form.get('keyword', '').strip()
    images = []
    users = []
    if keyword:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        
        # Search for photos with associated user information
        query_photos = """
            SELECT photos.*, accounts.username, accounts.profile_pic
            FROM photos
            JOIN accounts ON photos.user_id = accounts.id
            WHERE photos.description LIKE %s
        """
        cursor.execute(query_photos, ('%' + keyword + '%',))
        images = cursor.fetchall()

        # Search for users
        query_users = "SELECT id, username, profile_pic FROM accounts WHERE username LIKE %s"
        cursor.execute(query_users, ('%' + keyword + '%',))
        users = cursor.fetchall()

        cursor.close()

    return render_template('search.html', images=images, users=users)

@app.route('/profile/<int:user_id>')
def view_profile(user_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM accounts WHERE id = %s', (user_id,))
    user = cursor.fetchone()
    if not user:
        return 'Hmm... Can\'t Find', 404
    
    cursor.execute('SELECT * FROM photos WHERE user_id = %s', (user_id,))
    images = cursor.fetchall()
    cursor.close()

    is_following_user = False
    if 'loggedin' in session:
        is_following_user = is_following(session['id'], user_id)
    
    return render_template('profile.html', user=user, images=images, is_following_user=is_following_user)

@app.route('/follow/<int:followee_id>', methods=['POST'])
def follow(followee_id):
    if 'loggedin' in session:
        follower_id = session['id']
        if not is_following(follower_id, followee_id):
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('INSERT INTO followers (follower_id, followee_id) VALUES (%s, %s)', (follower_id, followee_id))
            mysql.connection.commit()
            cursor.close()
    return redirect(url_for('view_profile', user_id=followee_id))

@app.route('/unfollow/<int:followee_id>', methods=['POST'])
def unfollow(followee_id):
    if 'loggedin' in session:
        follower_id = session['id']
        if is_following(follower_id, followee_id):
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('DELETE FROM followers WHERE follower_id = %s AND followee_id = %s', (follower_id, followee_id))
            mysql.connection.commit()
            cursor.close()
    return redirect(url_for('view_profile', user_id=followee_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s', (username,))
        account = cursor.fetchone()
        if account and bcrypt.check_password_hash(account['password'], password):
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            session['profile_pic'] = account['profile_pic'] if account['profile_pic'] else 'usericon.png'
            return redirect(url_for('home'))
        else:
            msg = 'Hmm... Can\'t Find You'
    return render_template('login.html', msg=msg)

@app.route('/user')
def user_account():
    if not session.get('loggedin'):
        return redirect(url_for('login'))
    
    username = session.get('username')
    profile_pic = session.get('profile_pic', 'usericon.png')
    user_id = session.get('id')

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM photos WHERE user_id = %s', (user_id,))
    images = cursor.fetchall()
    cursor.close()
    
    user = {
        'id': user_id,
        'username': username,
        'profile_pic': profile_pic
    }
    
    return render_template('user.html', user=user, images=images)

@app.route('/followers/<int:user_id>')
def followers(user_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM followers JOIN accounts ON followers.follower_id = accounts.id WHERE followee_id = %s', (user_id,))
    followers = cursor.fetchall()
    cursor.execute('SELECT username, profile_pic FROM accounts WHERE id = %s', (user_id,))
    user = cursor.fetchone()
    cursor.close()
    return render_template('followers.html', user=user, followers=followers)

@app.route('/following/<int:user_id>')
def following(user_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM followers JOIN accounts ON followers.followee_id = accounts.id WHERE follower_id = %s', (user_id,))
    following = cursor.fetchall()
    cursor.execute('SELECT username, profile_pic FROM accounts WHERE id = %s', (user_id,))
    user = cursor.fetchone()
    cursor.close()
    return render_template('following.html', user=user, following=following)

@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    if 'loggedin' in session:
        if request.method == 'POST':
            username = request.form['username']
            profile_pic = request.files.get('profile_pic')  # Using get() to avoid KeyError
            password = request.form.get('password')

            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM accounts WHERE id = %s', (session['id'],))
            account = cursor.fetchone()

            if profile_pic and profile_pic.filename:
                profile_pic_filename = secure_filename(profile_pic.filename)
                file_path = os.path.join('static/profile_pics', profile_pic_filename)
                profile_pic.save(file_path)
                print(f"Profile picture saved to: {file_path}")
            else:
                profile_pic_filename = account['profile_pic'] if account['profile_pic'] else 'usericon.png'

            if password:
                hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
                cursor.execute('UPDATE accounts SET username = %s, password = %s, profile_pic = %s WHERE id = %s',
                               (username, hashed_password, profile_pic_filename, session['id']))
            else:
                cursor.execute('UPDATE accounts SET username = %s, profile_pic = %s WHERE id = %s',
                               (username, profile_pic_filename, session['id']))

            mysql.connection.commit()
            flash('Profile updated successfully!', 'success')
            session['username'] = username
            session['profile_pic'] = profile_pic_filename  # Update session profile pic
            return redirect(url_for('edit_profile'))

        return render_template('edit_profile.html')
    return redirect(url_for('login'))

@app.route('/upload_image', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return redirect(url_for('user_account'))
    
    file = request.files['image']
    if file and file.filename:
        filename = secure_filename(file.filename)
        file.save(os.path.join('static/images', filename))
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO photos (user_id, title, description, filename) VALUES (%s, %s, %s, %s)', 
                       (session['id'], request.form['title'], request.form['description'], filename))
        mysql.connection.commit()
        return redirect(url_for('user_account'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s', (username,))
        account = cursor.fetchone()
        if account:
            flash('Account already exists!', 'error')
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            flash('Invalid email address!', 'error')
        elif not re.match(r'[A-Za-z0-9]+', username):
            flash('Username must contain only characters and numbers!', 'error')
        elif not username or not password or not email:
            flash('Please fill out the form!', 'error')
        else:
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            cursor.execute('INSERT INTO accounts (username, password, email, profile_pic) VALUES (%s, %s, %s, %s)', 
                           (username, hashed_password, email, 'usericon.png'))
            mysql.connection.commit()
            flash('Woohoo! You\'re In!', 'Hooray!')
            return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    msg = ''
    if 'loggedin' in session:
        if request.method == 'POST' and 'title' in request.form and 'description' in request.form and 'file' in request.files:
            title = request.form['title']
            description = request.form['description']
            file = request.files['file']
            filename = secure_filename(file.filename)
            file_path = os.path.join('static/images', filename)
            file.save(file_path)
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('INSERT INTO photos (user_id, title, description, filename) VALUES (%s, %s, %s, %s)', (session['id'], title, description, filename))
            mysql.connection.commit()
            msg = 'Woohoo! Image Added!'
        return render_template('upload.html', msg=msg)
    return redirect(url_for('login'))

@app.route('/edit_image/<int:image_id>', methods=['GET', 'POST'])
def edit_image(image_id):
    if not session.get('loggedin'):
        return redirect(url_for('login'))
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM photos WHERE id = %s AND user_id = %s', (image_id, session['id']))
    image = cursor.fetchone()
    if request.method == 'POST' and image:
        title = request.form['title']
        description = request.form['description']
        cursor.execute('UPDATE photos SET title = %s, description = %s WHERE id = %s', (title, description, image_id))
        mysql.connection.commit()
        return redirect(url_for('user_account'))
    return render_template('edit_image.html', image=image)

@app.route('/delete_image/<int:image_id>')
def delete_image(image_id):
    if not session.get('loggedin'):
        return redirect(url_for('login'))
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('DELETE FROM photos WHERE id = %s AND user_id = %s', (image_id, session['id']))
    mysql.connection.commit()
    return redirect(url_for('user_account'))

@app.route('/delete_account', methods=['POST'])
def delete_account():
    if 'loggedin' in session:
        user_id = session['id']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        
        # Delete user's photos
        cursor.execute('DELETE FROM photos WHERE user_id = %s', (user_id,))
        
        # Delete user's followers and following records
        cursor.execute('DELETE FROM followers WHERE follower_id = %s OR followee_id = %s', (user_id, user_id))
        
        # Delete user account
        cursor.execute('DELETE FROM accounts WHERE id = %s', (user_id,))
        mysql.connection.commit()
        cursor.close()
        
        # Clear session and redirect to home
        session.clear()
        return redirect(url_for('home'))
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

# Register the utility function for Jinja2 templates
@app.context_processor
def utility_processor():
    return dict(is_following=is_following)

if __name__ == '__main__':
    app.secret_key = 'your_secret_key'
    app.run(debug=True)
