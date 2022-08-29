from flask import Flask, jsonify, request

from storage import all_articles, liked_articles, not_liked_articles
from demographic_filtering import output
from content_filtering import get_recommendations

app = Flask(__name__)

@app.route("/get-article")
def get_movie():
    article_data = {
        "title": all_articles[0][19],
        "url" : all_articles[0][27],
        "contentType": all_articles[0][13] or "N/A",
        "lang": all_articles[0][15],
        "total_events": all_articles[0][20],
        }
    return jsonify({
        "data": article_data,
        "status": "success"
    })

@app.route("/liked-article", methods=["POST"])
def liked_article():
    article = all_articles[0]
    liked_article.append(article)
    all_articles.pop(0)
    return jsonify({
        "status": "success"
    }), 201

@app.route("/unliked-articles", methods=["POST"])
def unliked_article():
    article = all_articles[0]
    not_liked_articles.append(article)
    all_articles.pop(0)
    return jsonify({
        "status": "success"
    }), 201


@app.route("/popular-articles")
def popular_articles():
    article_data = []
    for article in output:
        _d = {
            "title": article[0],
            "url": article[1],
            "contentType": article[2] or "N/A",
            "lang": article[3],
            "total_events": article[5]
        }
        article_data.append(_d)
    return jsonify({
        "data": article_data,
        "status": "success"
    }), 200

@app.route("/recommended-articles")
def recommended_articles():
    all_recommended = []
    for liked_article in liked_articles:
        output = get_recommendations(liked_article[19])
        for data in output:
            all_recommended.append(data)
    import itertools
    all_recommended.sort()
    all_recommended = list(all_recommended for all_recommended,_ in itertools.groupby(all_recommended))
    article_data = []
    for recommended in all_recommended:
        _d = {
            "title": recommended[0],
            "url": recommended[1],
            "contentType": recommended[2] or "N/A",
            "lang": recommended[3],
            "total_events": recommended[4],
        }
        article_data.append(_d)
    return jsonify({
        "data": article_data,
        "status": "success"
    }), 200

if __name__ == "__main__":
  app.run()