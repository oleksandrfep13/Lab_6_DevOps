from flask import Blueprint, request, jsonify
from app.models import Task
from app.database import db

main = Blueprint("main", __name__)


@main.route("/")
def home():
    return jsonify({
        "message": "DevOps Lab 6 API is working"
    })


@main.route("/tasks", methods=["GET"])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([task.to_dict() for task in tasks])


@main.route("/tasks", methods=["POST"])
def create_task():
    data = request.get_json()

    if not data or "title" not in data:
        return jsonify({"error": "Title is required"}), 400

    task = Task(title=data["title"])

    db.session.add(task)
    db.session.commit()

    return jsonify(task.to_dict()), 201