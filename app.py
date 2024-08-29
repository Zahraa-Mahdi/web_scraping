from flask import Flask, jsonify
from pymongo import MongoClient, errors
from bson import ObjectId
from datetime import datetime, timedelta
import json
import sys

app = Flask(__name__)

# MongoDB connection
try:
    client = MongoClient("mongodb://localhost:27017/")
    db = client["almayadeen"]
    collection = db["articles"]
except errors.ConnectionFailure:
    print("Failed to connect to MongoDB server")
    sys.exit(1)

# Custom JSON Encoder to handle ObjectId and datetime
class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, datetime):
            return o.isoformat()
        return super().default(o)

app.json_encoder = JSONEncoder

# General error handler
@app.errorhandler(Exception)
def handle_exception(error):
    response = jsonify({"error": str(error)})
    response.status_code = 500
    return response

# Endpoint: Top Keywords
@app.route('/top_keywords', methods=['GET'])
def top_keywords():
    pipeline = [
        {"$unwind": "$keywords"},
        {"$group": {"_id": "$keywords", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ]
    result = list(collection.aggregate(pipeline))
    return jsonify({item["_id"]: item["count"] for item in result})

# Endpoint: Top Authors
@app.route('/top_authors', methods=['GET'])
def top_authors():
    pipeline = [
        {"$group": {"_id": "$author", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ]
    result = list(collection.aggregate(pipeline))
    return jsonify({item["_id"]: item["count"] for item in result})

# Endpoint: Articles by Date
@app.route('/articles_by_date', methods=['GET'])
def articles_by_date():
    pipeline = [
        {"$group": {"_id": "$published_date", "count": {"$sum": 1}}},
        {"$sort": {"_id": 1}}
    ]
    result = list(collection.aggregate(pipeline))
    return jsonify({str(item["_id"]): item["count"] for item in result})

# Endpoint: Articles by Word Count
@app.route('/articles_by_word_count', methods=['GET'])
def articles_by_word_count():
    pipeline = [
        {"$group": {"_id": "$word_count", "count": {"$sum": 1}}},
        {"$sort": {"_id": 1}}
    ]
    result = list(collection.aggregate(pipeline))
    return jsonify({item["_id"]: item["count"] for item in result})

# Endpoint: Articles by Language
@app.route('/articles_by_language', methods=['GET'])
def articles_by_language():
    pipeline = [
        {"$group": {"_id": "$language", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}}
    ]
    result = list(collection.aggregate(pipeline))
    return jsonify({item["_id"]: item["count"] for item in result})

# Endpoint: Articles by Category
@app.route('/articles_by_classes', methods=['GET'])
def articles_by_classes():
    pipeline = [
        {"$group": {"_id": "$classes", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}}
    ]
    result = list(collection.aggregate(pipeline))
    return jsonify({item["_id"]: item["count"] for item in result})

# Endpoint: Recent Articles
@app.route('/recent_articles', methods=['GET'])
def recent_articles():
    try:
        result = list(collection.find().sort("published_date", -1).limit(10))
        return jsonify(result)
    except errors.PyMongoError as e:
        return handle_exception(e)

# Endpoint: Articles by Keyword
@app.route('/articles_by_keyword/<keyword>', methods=['GET'])
def articles_by_keyword(keyword):
    try:
        result = list(collection.find({"keywords": keyword}))
        return jsonify(result)
    except errors.PyMongoError as e:
        return handle_exception(e)

# Endpoint: Articles by Author
@app.route('/articles_by_author/<author_name>', methods=['GET'])
def articles_by_author(author_name):
    try:
        result = list(collection.find({"author": author_name}))
        return jsonify(result)
    except errors.PyMongoError as e:
        return handle_exception(e)

# Endpoint: Top Classes
@app.route('/top_classes', methods=['GET'])
def top_classes():
    pipeline = [
        {"$group": {"_id": "$classes", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ]
    result = list(collection.aggregate(pipeline))
    return jsonify({item["_id"]: item["count"] for item in result})

# Endpoint: Article Details
@app.route('/article_details/<postid>', methods=['GET'])
def article_details(postid):
    try:
        article = collection.find_one({"postid": postid})
        if article:
            return jsonify(article)
        else:
            return jsonify({"error": "Article not found"}), 404
    except errors.PyMongoError as e:
        return handle_exception(e)

# Endpoint: Articles Containing Video
@app.route('/articles_with_video', methods=['GET'])
def articles_with_video():
    try:
        result = list(collection.find({"video_duration": {"$ne": None}}))
        return jsonify(result)
    except errors.PyMongoError as e:
        return handle_exception(e)

# Endpoint: Articles by Publication Year
@app.route('/articles_by_year/<year>', methods=['GET'])
def articles_by_year(year):
    try:
        result = list(collection.find({"published_date": {"$regex": f"^{year}"}}))
        return jsonify({year: len(result)})
    except errors.PyMongoError as e:
        return handle_exception(e)

# Endpoint: Longest Articles
@app.route('/longest_articles', methods=['GET'])
def longest_articles():
    pipeline = [
        {"$sort": {"word_count": -1}},
        {"$limit": 10}
    ]
    result = list(collection.aggregate(pipeline))
    return jsonify(result)

# Endpoint: Shortest Articles
@app.route('/shortest_articles', methods=['GET'])
def shortest_articles():
    pipeline = [
        {"$sort": {"word_count": 1}},
        {"$limit": 10}
    ]
    result = list(collection.aggregate(pipeline))
    return jsonify(result)

# Endpoint: Articles by Keyword Count
@app.route('/articles_by_keyword_count', methods=['GET'])
def articles_by_keyword_count():
    pipeline = [
        {"$unwind": "$keywords"},
        {"$group": {"_id": {"article_id": "$_id", "keyword_count": {"$sum": 1}}}},
        {"$group": {"_id": "$_id.keyword_count", "count": {"$sum": 1}}},
        {"$sort": {"_id": 1}}
    ]
    result = list(collection.aggregate(pipeline))
    return jsonify({item["_id"]: item["count"] for item in result})

# Endpoint: Articles by Thumbnail Presence
@app.route('/articles_with_thumbnail', methods=['GET'])
def articles_with_thumbnail():
    try:
        result = list(collection.find({"thumbnail": {"$ne": None}}))
        return jsonify(result)
    except errors.PyMongoError as e:
        return handle_exception(e)

# Endpoint: Articles Updated After Publication
@app.route('/articles_updated_after_publication', methods=['GET'])
def articles_updated_after_publication():
    try:
        result = list(collection.find({"last_updated": {"$gt": "$published_date"}}))
        return jsonify(result)
    except errors.PyMongoError as e:
        return handle_exception(e)

# Endpoint: Articles by Coverage
@app.route('/articles_by_coverage/<coverage>', methods=['GET'])
def articles_by_coverage(coverage):
    try:
        result = list(collection.find({"classes": coverage}))
        return jsonify(result)
    except errors.PyMongoError as e:
        return handle_exception(e)

# Endpoint: Most Popular Keywords in the Last X Days
@app.route('/popular_keywords_last_X_days/<int:days>', methods=['GET'])
def popular_keywords_last_X_days(days):
    date_threshold = datetime.now() - timedelta(days=days)
    pipeline = [
        {"$match": {"published_date": {"$gte": date_threshold}}},
        {"$unwind": "$keywords"},
        {"$group": {"_id": "$keywords", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ]
    result = list(collection.aggregate(pipeline))
    return jsonify({item["_id"]: item["count"] for item in result})

# Endpoint: Articles by Published Month
@app.route('/articles_by_month/<int:year>/<int:month>', methods=['GET'])
def articles_by_month(year, month):
    try:
        start_date = datetime(year, month, 1)
        end_date = datetime(year, month + 1, 1) if month < 12 else datetime(year + 1, 1, 1)

        count = collection.count_documents({
            "published_date": {
                "$gte": start_date,
                "$lt": end_date
            }
        })

        return jsonify({f"{month}/{year}": count})
    except errors.PyMongoError as e:
        return handle_exception(e)
    except Exception as e:
        return handle_exception(e)


# Endpoint: Articles by Word Count Range
@app.route('/articles_by_word_count_range/<int:min>/<int:max>', methods=['GET'])
def articles_by_word_count_range(min, max):
    try:
        result = list(collection.find({"word_count": {"$gte": min, "$lte": max}}))
        return jsonify(result)
    except errors.PyMongoError as e:
        return handle_exception(e)

# Endpoint: Articles with Specific Keyword Count
@app.route('/articles_with_specific_keyword_count/<int:count>', methods=['GET'])
def articles_with_specific_keyword_count(count):
    try:
        pipeline = [
            {"$match": {"keywords": {"$exists": True}}},
            {"$addFields": {"keywordCount": {"$size": "$keywords"}}},
            {"$match": {"keywordCount": count}},
            {"$project": {"_id": 1, "title": 1, "keywords": 1}}
        ]
        result = list(collection.aggregate(pipeline))
        return jsonify(result)
    except errors.PyMongoError as e:
        return handle_exception(e)


# Endpoint: Articles by Specific Date
@app.route('/articles_by_specific_date/<date>', methods=['GET'])
def articles_by_specific_date(date):
    try:
        specific_date = datetime.strptime(date, "%Y-%m-%d")
        result = list(collection.find({"published_date": specific_date}))
        return jsonify(result)
    except ValueError:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400
    except errors.PyMongoError as e:
        return handle_exception(e)

# Endpoint: Articles Containing Specific Text
@app.route('/articles_containing_text/<text>', methods=['GET'])
def articles_containing_text(text):
    try:
        result = list(collection.find({"content": {"$regex": text, "$options": "i"}}))
        return jsonify(result)
    except errors.PyMongoError as e:
        return handle_exception(e)

# Endpoint: Articles with More than N Words
@app.route('/articles_with_more_than/<int:word_count>', methods=['GET'])
def articles_with_more_than(word_count):
    try:
        result = list(collection.find({"word_count": {"$gt": word_count}}))
        return jsonify(result)
    except errors.PyMongoError as e:
        return handle_exception(e)

# Endpoint: Articles Grouped by Coverage
@app.route('/articles_grouped_by_coverage', methods=['GET'])
def articles_grouped_by_coverage():
    pipeline = [
        {"$group": {"_id": "$classes", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}}
    ]
    result = list(collection.aggregate(pipeline))
    return jsonify({item["_id"]: item["count"] for item in result})

# Endpoint: Articles Published in Last X Hours
@app.route('/articles_last_X_hours/<int:hours>', methods=['GET'])
def articles_last_X_hours(hours):
    date_threshold = datetime.now() - timedelta(hours=hours)
    try:
        result = list(collection.find({"published_date": {"$gte": date_threshold}}))
        return jsonify(result)
    except errors.PyMongoError as e:
        return handle_exception(e)

# Endpoint: Articles by Length of Title
@app.route('/articles_by_title_length', methods=['GET'])
def articles_by_title_length():
    pipeline = [
        {"$project": {"title_length": {"$strLenCP": "$title"}}},
        {"$group": {"_id": "$title_length", "count": {"$sum": 1}}},
        {"$sort": {"_id": 1}}
    ]
    result = list(collection.aggregate(pipeline))
    return jsonify({item["_id"]: item["count"] for item in result})

# Endpoint: Most Updated Articles
@app.route('/most_updated_articles', methods=['GET'])
def most_updated_articles():
    pipeline = [
        {"$match": {"last_updated": {"$exists": True}}},
        {"$group": {"_id": "$_id", "update_count": {"$sum": 1}}},
        {"$sort": {"update_count": -1}},
        {"$limit": 10}
    ]
    result = list(collection.aggregate(pipeline))
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)

