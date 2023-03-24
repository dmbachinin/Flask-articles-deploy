import click
from flask import redirect, render_template

from blog.app import create_app
from blog.models.database import db

app = create_app()


@app.cli.command('init-db')
def init_db():
    db.create_all()
    print("done!")


@app.cli.command('delete-db')
def delete_db():
    db.drop_all()
    print("done!")


@app.cli.command('create-init-tags')
def init_tags():
    from blog.models import Tag
    tag_list = ["flask", "django", "IT", "Life", "sql"]
    for tag in tag_list:
        db.session.add(Tag(name=tag))
    db.session.commit()



@app.route('/', methods=["GET"])
def index():
    return render_template('main/index.html')


if __name__ == "__main__":
    app.run()
