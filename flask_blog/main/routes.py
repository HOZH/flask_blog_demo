from flask import render_template, request, Blueprint
from flask_blog.models import Post
main = Blueprint('main', __name__)


@main.route('/')
@main.route('/home')
def home_page():

    page = request.args.get('page', 1, type=int)

    post_per_page = 3

    # posts = Post.query.all()
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(
        page=page, per_page=post_per_page)
    # not showing up all the posts, paginate posts

    return render_template('home.html', posts=posts)


@main.route('/about')
def about_page():

    return render_template('about.html', title="About Page")
