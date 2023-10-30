# Blog-Site
![blog_homepage](https://github.com/dineshkumar1495/Blog-Site/assets/94850695/b9404a20-5e79-4380-a874-661641a24269)

**app.py:**

1. Configuration and Setup:
   - Configuring the app with a secret key, SQLAlchemy database URI, and disabling track modifications.
   - Initializing the CKEditor and Bootstrap extensions for the app.
   - Creating the Flask app instance, SQLAlchemy database instance, and Migrate object for database migrations.
   - Setting up the LoginManager for user authentication.

2. Database Models:
   - Defining the `BlogPost` model with columns for blog post details and an `author_id` column as a foreign key to the `Users` table.
   - Defining the `Users` model with columns for user details and a relationship with `BlogPost` using `db.relationship`.

3. User Loader Function:
   - The `login_manager.user_loader` function is defined to load a user by its `id`.

4. Routes and Views:
   - `/`: The home route, retrieves all blog posts and renders the `index.html` template.
   - `/register`: Renders the registration form and handles user registration logic.
   - `/login`: Renders the login form and handles user login logic.
   - `/logout`: Logs out the user and redirects to the home page.
   - `/post/<int:post_id>`: Retrieves and displays a specific blog post.
   - `/about`: Renders the about page.
   - `/contact`: Renders the contact page.
   - `/new-post`: Renders the form to create a new blog post and handles post creation logic.
   - `/edit-post/<int:post_id>`: Renders the form to edit a blog post and handles post update logic.
   - `/delete/<int:post_id>`: Deletes a specific blog post.

5. Running the App: The app runs if executed directly.

**forms.py:**
![Screenshot (342)](https://github.com/dineshkumar1495/Blog-Site/assets/94850695/99a38658-d10f-445e-a78e-1a27dc639788)


1. Importing FlaskForm and necessary fields and validators from Flask-WTF.

2. Defining three classes: `CreatePostForm`, `RegisterForm`, and `LoginForm`, each representing a form in the application.

**templates/index.html:**

1. The template extends `header.html` and includes the page header with Angela's Blog name and subtitle.

2. It iterates over all the blog posts and displays their titles, subtitles, authors, and dates with links to view individual posts.

3. If the user is logged in and is the admin (with ID 1), a delete button is shown next to each post for admin-specific actions.

**templates/header.html:**

1. Common header template included in other pages.

2. Contains the navigation bar with links to home, login, register, logout, about, and contact pages.

**templates/register.html:**

1. Extends `bootstrap/base.html` and includes `header.html`.

2. Displays a form to register a new user, including fields for name, email, and password.

**templates/post.html:**

1. Includes `header.html`.

2. Displays a single blog post with its title, subtitle, author, date, and content.

3. If the user is logged in and is the admin, an edit button is shown to modify the post.

**templates/login.html:**

1. Extends `bootstrap/base.html` and includes `header.html`.

2. Displays a form to log in with fields for email and password.

**templates/make-post.html:**

1. Extends `bootstrap/base.html` and includes `header.html`.

2. Displays a form to create or edit a blog post with fields for title, subtitle, image URL, and post content (using CKEditor).

**templates/footer.html:**

1. Contains the footer section of the website, including social media links and copyright information.

**templates/about.html:**

1. Extends `bootstrap/base.html` and includes `header.html`.

2. Displays a page containing information about the website author.

**templates/contact.html:**

![Screenshot (343)](https://github.com/dineshkumar1495/Blog-Site/assets/94850695/6515723d-e5c1-4d29-a289-9bcc58efd069)


1. Extends `bootstrap/base.html` and includes `header.html`.

2. Displays a form for users to contact the website owner.

