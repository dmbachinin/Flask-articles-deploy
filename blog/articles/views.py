from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from sqlalchemy.orm import joinedload
from werkzeug.exceptions import NotFound

from blog.forms.article import ArticleCreateForm
from blog.models import Article, Author, Tag
from blog.models.database import db


articleBlueprint = Blueprint('articleBlueprint', __name__, url_prefix="/articles", static_folder="../static")


@articleBlueprint.route('/list', methods=["GET"])
def article_list():
    return render_template("articles/list.html", articles=Article.query.all())


@articleBlueprint.route('/', methods=["GET"])
@login_required
def article_create_form():
    form = ArticleCreateForm(request.form)
    form.tags.choices = [(tag.id, tag.name) for tag in Tag.query.order_by("name")]
    return render_template("articles/create.html", form=form)

@articleBlueprint.route('/', methods=["POST"])
@login_required
def article_create():
    form = ArticleCreateForm(request.form)
    form.tags.choices = [(tag.id, tag.name) for tag in Tag.query.order_by("name")]
    if form.validate_on_submit():
        _article = Article(author_id=current_user.id, title=form.title.data, text=form.text.data)
        if form.tags.data:
            selected_tags = Tag.query.filter(Tag.id.in_(form.tags.data))
            for tag in selected_tags:
                _article.tags.append(tag)

        if not current_user.author:
            author = Author(user_id=current_user.id)
            db.session.add(author)

        db.session.add(_article)

        db.session.commit()

        return redirect(url_for("articleBlueprint.article_current", pk=_article.id))

    return redirect(url_for("articleBlueprint.article_create_form"))



@articleBlueprint.route('/list/<int:pk>')
def article_current(pk: int):
    current_article = Article.query.filter_by(id=pk).options(joinedload(Article.tags)).one_or_none()
    if current_article:
        return render_template("articles/current.html", article=current_article)
    raise NotFound(f"Article with id = {pk} not found")


@articleBlueprint.route('/list/tag/<string:tag_name>')
def article_by_tag(tag_name: str):
    tag = Tag.query.filter_by(name=tag_name).one_or_none()
    if tag:
        all_article = Article.query.all()
        article_with_tag = []
        for article in all_article:
            if tag in article.tags:
                article_with_tag.append(article)

        return render_template("articles/list.html", articles=article_with_tag, tag=tag_name)
    # raise NotFound(f"Article with tag = {tag_name} not found")
    raise NotFound(f"Tag with name = {tag_name} not found")
