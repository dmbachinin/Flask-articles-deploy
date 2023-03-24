from flask import Blueprint, render_template

from blog.models import Author

authorBlueprint = Blueprint('authorBlueprint', __name__, url_prefix="/author", static_folder="../static")


@authorBlueprint.route('/')
def author_list():
    return render_template("authors/list.html", authors=Author.query.all())
