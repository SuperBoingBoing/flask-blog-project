from flask import Blueprint, render_template, request, session, flash, redirect, url_for
from .auth import connect_db, get_id

views = Blueprint('views', __name__)

def fetch_data():
    base = connect_db()
    conn = base.cursor()
    conn.execute("""SELECT b.id AS post_id, b.text AS post_text, u.id AS user_id,
                    u.name AS user_name, u.email AS user_email, u.password AS user_password,
                    b.datetime AS post_time
                 FROM blog_post b
                 JOIN blog_project u ON b.author_id = u.id
                 """)
    results = conn.fetchall()
    base.commit()
    base.close()
    conn.close()
    return results

def fetch_comment_data():
    base = connect_db()
    conn = base.cursor()
    conn.execute("SELECT text FROM `blog_comment`")
    comments = conn.fetchall()
    base.commit()
    base.close()
    conn.close()
    return comments

def add_data(text, author_id):
    base = connect_db()
    conn = base.cursor()
    conn.execute("INSERT INTO `blog_post` (text, author_id) VALUES(%s, %s)", (text, author_id))
    base.commit()
    base.close()
    conn.close()

def delete_data(id):
    base = connect_db()
    conn = base.cursor()
    conn.execute("DELETE FROM `blog_post` WHERE id = %s", (id))
    base.commit()
    base.close()
    conn.close()

def get_post_id(author_id):
    base = connect_db()
    conn = base.cursor()
    conn.execute("SELECT (id) FROM `blog_post` WHERE author_id = %s", (author_id))
    result = conn.fetchone()
    base.commit()
    base.close()
    conn.close()
    return result

def add_comment_data(comment, post_id, author_id):
    base = connect_db()
    conn = base.cursor()
    conn.execute("INSERT INTO `blog_comment` (text, post_id, author_id) VALUES (%s, %s, %s)", (comment, post_id, author_id),)
    base.commit()
    base.close()
    conn.close()


@views.route('/')
@views.route('/home')
def home():
    results = fetch_data()
    comments = fetch_comment_data()
    return render_template('home.html', results=results, comments=comments)

@views.route('/create-post', methods=['POST', 'GET'])
def create_post():
    if request.method == 'POST':
        text = request.form.get('text')
        if 'email' in session:
            email = session['email']
            author_id = get_id(email)
            add_data(text, author_id['id'])
            flash('Post successfully', category='success')
            return redirect(url_for('views.home'))

    return render_template('create_post.html')


@views.route('/delete-post/<int:id>', methods=['POST'])
def delete_post(id):
    if 'email' in session:
        email = session['email']
        author_id = get_id(email)

        try:
            base = connect_db()
            conn = base.cursor()
            conn.execute("SELECT author_id FROM `blog_post` WHERE id = %s", (id,))
            post_author = conn.fetchone()
            
            if post_author and post_author['author_id'] == author_id['id']:
                conn.execute("DELETE FROM `blog_post` WHERE id = %s", (id,))               
                flash('Post deleted successfully', category='success')
    
            else:                
                flash('You are not the author of this post, cannot delete', category='danger')
            
            base.commit()
               
        finally:
            base.close()
            conn.close()     
    
    return redirect(url_for("views.home"))


@views.route('/create-comment/<int:post_id>', methods=["POST"])
def create_comment(post_id):
    comment = request.form.get("comment")
    if not comment:
        flash("Comment cannot be empty...", category="danger")

    else:
        email = session["email"]
        author_id = get_id(email)
        add_comment_data(comment, post_id, author_id['id'])

    return redirect(url_for("views.home"), comment=comment)
