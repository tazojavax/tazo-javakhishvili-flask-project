from flask import Flask, render_template, request, redirect

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/blog")
def blog():
    return render_template("blog.html")

@app.route("/about")
def about():
    return render_template("about.html")

from flask_sqlalchemy import SQLAlchemy

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///food.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    ingredients = db.Column(db.Text)
    recipe = db.Column(db.Text)
    image = db.Column(db.String(500))

@app.route("/add_recipe", methods=["GET", "POST"])
def add_recipe():
            if request.method == "POST":
                recipe = Recipe(
                    title=request.form["title"],
                    ingredients=request.form["ingredients"],
                    recipe=request.form["recipe"],
                    image=request.form["image"]
                )

                db.session.add(recipe)
                db.session.commit()

                return redirect("/recipes")

            return render_template("add_recipe.html")

@app.route("/recipes")
def recipes():
    recipes = Recipe.query.all()

    return render_template(
        "recipes.html",
        recipes=recipes
    )

@app.route("/register", methods=["GET", "POST"])
def register():
        if request.method == "POST":
            user = User(
                username=request.form["username"],
                email=request.form["email"],
                password=request.form["password"]
            )

            db.session.add(user)
            db.session.commit()

            return redirect("/")

        return render_template("register.html")

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
