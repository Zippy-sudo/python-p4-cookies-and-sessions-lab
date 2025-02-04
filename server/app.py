#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, session
from flask_migrate import Migrate

from models import db, Article, User

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/clear')
def clear_session():
    session["page_views"] = 0
    response = make_response({"message": "200: Successfully cleared session data."}, 200)
    response.set_cookie("page_views", f'{session["page_views"]}')
    return response

# @app.route('/articles')
# def index_articles():

#     pass

@app.route('/articles/<int:id>')
def show_article(id):

    session["page_views"] = session.get("page_views") or 0
    session["page_views"] = int(session.get("page_views")) + 1

    if int(session.get("page_views")) != 4:
        article_dict = Article.query.filter_by(id = id).first().to_dict()
        response = make_response(article_dict, 200)
        response.set_cookie ("page_views", f'{session["page_views"]}')
        return response
    else:
        return make_response({'message': 'Maximum pageview limit reached'}, 401)





if __name__ == '__main__':
    app.run(port=5555, debug=True)
