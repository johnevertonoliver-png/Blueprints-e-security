from flask import render_template, abort
from . import blog_bp
from data import posts

@blog_bp.route('/')
def index():
    return render_template('blog/index.html', posts = posts)


@blog_bp.route('/post/<int:post_id>')
def post(post_id):
    post = next((p for p in posts if p['id'] == post_id), None)
    if post is None:
        abort(404)            # Em vez de renderizar "post=None"
    return render_template('blog/post.html', post=post)
    