
from flask import Blueprint, flash, g, redirect
from flask import render_template, request, url_for

from werkzeug.exceptions import abort

from webapp.auth import login_required
from webapp.database import db_session
from webapp.models import Post

bp = Blueprint('blog', __name__)

@bp.route('/')
def index():
    posts = Post.query.all()
    return render_template('blog/index.html', posts=posts)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required'
        
        if error is not None:
            flash(error)
        else:
            newpost = Post(author=g.user, title=title, body=body)
            db_session.add(newpost)
            db_session.commit()
            return redirect(url_for('blog.index'))
    return render_template('blog/create.html')

def get_post(id, check_author=True):
    post = Post.query.filter(Post.id==id).first()
    if post is None:
        abort(404, f"Post id {id} doesn't exist.")
    if check_author and post.author_id != g.user.id:
        abort(403)
    return post

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required'
        
        if error is not None:
            flash(error)
        else:
            post.title = title
            post.body = body
            db_session.commit()
            return redirect(url_for('blog.index'))
    return render_template('blog/update.html', post=post)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    post = get_post(id)
    db_session.delete(post)
    db_session.commit()
    return redirect(url_for('blog.index'))
