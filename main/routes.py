from flask import render_template, request, Blueprint,url_for, flash, redirect
from doctors.models import Post, Comment,Like
from flask_login import current_user, login_required
from doctors import db
main = Blueprint('main', __name__)



@main.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    
    return render_template('posts/home.html', user=current_user, posts=posts)


@main.route("/about")
def about():
    return render_template('about.html', title='About')

@main.route("/")
def base():
    return render_template('base.html')

@main.route("/create-comment/<post_id>", methods=['POST'])
@login_required
def create_comment(post_id):
    text = request.form.get('text')

    if not text:
        flash('Comment does not exist.', 'error')
        
    else:
        post = Post.query.filter_by(id=post_id)
        if post:
            comment = Comment(
                text=text, author=current_user.id, post_id=post_id)
            db.session.add(comment)
            db.session.commit()
        else:
            flash('Post does not exist.', 'error')
            

    return redirect(request.referrer)

@main.route("/delete-comment/<comment_id>")
@login_required
def delete_comment(comment_id):
    comment = Comment.query.filter_by(id=comment_id).first()

    if not comment:
        
        flash('Comment does not exist.', 'error')
    elif current_user.id != comment.author and current_user.id != comment.post.author:
        flash('You do not have permission to delete this comment.','error')
    else:
        db.session.delete(comment)
        db.session.commit()

    return redirect(request.referrer)

@main.route("/like-post/<post_id>", methods=['GET'])
@login_required
def like(post_id):
    post = Post.query.filter_by(id=post_id).first()
    like = Like.query.filter_by(
        user_id=current_user.id, post_id=post_id).first()
    
    if not post:
        flash('Post does not exist.', 'error')
        
    elif like:
        db.session.delete(like)
        db.session.commit()
    else:
        like = Like(user_id=current_user.id, post_id=post_id)
        db.session.add(like)
        db.session.commit()
    print(post.likes)
    return redirect(request.referrer)