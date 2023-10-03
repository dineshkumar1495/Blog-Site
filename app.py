from flask import Flask, render_template, redirect, url_for, flash, abort
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from forms import CreatePostForm, RegisterForm, LoginForm
from functools import wraps
from flask_migrate import Migrate
from sqlalchemy import ForeignKey
# from flask_gravatar import Gravatar

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
ckeditor = CKEditor(app)
Bootstrap(app)

##CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app,db)

##For Login
login_manager = LoginManager(app)
login_manager.init_app(app)



##CONFIGURE TABLES

# Child table
class BlogPost(db.Model, UserMixin):
    __tablename__ = "blog_posts"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    img_url = db.Column(db.String(250), nullable=False)
    author_id = db.Column(db.Integer, ForeignKey('users.id'))
    
# Parent Table
class  Users(db.Model,UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String(205), nullable=False, unique=True)
    name = db.Column(db.String(250), nullable = False)
    password = db.Column(db.String(500),nullable = False)
    blog_posts = db.relationship('BlogPost', backref='author')



@login_manager.user_loader
def load_user(user):
    return db.session.query(Users).filter_by(id=int(user)).first()


@app.route('/')
def get_all_posts():
    posts = BlogPost.query.all()
    return render_template("index.html", all_posts=posts, logged_in = current_user.is_authenticated, logged_user = current_user)


@app.route('/register',methods=['GET','POST'])
def register():
    register_form = RegisterForm()

    if register_form.validate_on_submit():
        name = register_form.name.data
        password = register_form.password.data
        email = register_form.email.data
        hashed_password = generate_password_hash(password=password,method='pbkdf2:sha256',salt_length=8)
        check_user = db.session.query(Users).filter_by(email=email).first()
        
        if check_user:
            flash("You've already signed up with this email. Sign in instead")
            return redirect( url_for('login'))
        
        with app.app_context():
            if email == "Admin@gmail.com":
                user = Users(id=1,email=email,name=name,password=hashed_password)
                db.session.add(user)
                db.session.commit()
            else:
                user = Users(email = email,name=name,password=hashed_password)
                db.session.add(user)
                db.session.commit()
        return redirect( url_for('login'))

    return render_template("register.html",form = register_form, logged_in = False)


@app.route('/login',methods=['GET','POST'])
def login():
    form= LoginForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = db.session.query(Users).filter_by(email=email).first()

        if not user:
            flash("There is no user registered in this email. Get signed up!")
            return redirect(url_for('register'))
        elif not check_password_hash(user.password,password):
            flash("The password is incorrect. Try again.")
        else:
            login_user(user)
            return redirect(url_for('get_all_posts'))        
    return render_template("login.html", form = form, logged_in = False)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('get_all_posts'))


@app.route("/post/<int:post_id>")
def show_post(post_id):
    requested_post = BlogPost.query.get(post_id)
    return render_template("post.html", post=requested_post,logged_user = current_user, logged_in=current_user.is_authenticated)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/new-post")
def add_new_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        new_post = BlogPost(
            title=form.title.data,
            subtitle=form.subtitle.data,
            body=form.body.data,
            img_url=form.img_url.data,
            author=current_user,
            date=date.today().strftime("%B %d, %Y")
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("get_all_posts"))
    return render_template("make-post.html", form=form)


@app.route("/edit-post/<int:post_id>")

def edit_post(post_id):
    if current_user.id != 1:
        abort(403,"Haha!! Nice try. You can't perform this operation.")
    post = BlogPost.query.get(post_id)
    edit_form = CreatePostForm(
        title=post.title,
        subtitle=post.subtitle,
        img_url=post.img_url,
        author=post.author,
        body=post.body
    )
    if edit_form.validate_on_submit():
        post.title = edit_form.title.data
        post.subtitle = edit_form.subtitle.data
        post.img_url = edit_form.img_url.data
        post.author = edit_form.author.data
        post.body = edit_form.body.data
        db.session.commit()
        return redirect(url_for("show_post", post_id=post.id))

    return render_template("make-post.html", form=edit_form)


@app.route("/delete/<int:post_id>")
def delete_post(post_id):
    if current_user.id != 1:
        abort(403,"Nope. No No No...You can't do that my man!!")
    post_to_delete = BlogPost.query.get(post_id)
    db.session.delete(post_to_delete)
    db.session.commit()

    return redirect(url_for('get_all_posts'))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000,debug=True)
