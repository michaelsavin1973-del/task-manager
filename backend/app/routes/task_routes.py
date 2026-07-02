from flask import Blueprint, request, jsonify
from app.services import task_service
import logging

task_bp = Blueprint("tasks", __name__)

logger = logging.getLogger(__name__)

# ---------------------------
# HEALTHCHECK
# ---------------------------
@task_bp.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200


# ---------------------------
# GET ALL TASKS
# ---------------------------
@task_bp.route("/api/tasks", methods=["GET"])
def get_tasks():
    try:
        logger.info("GET /api/tasks called")

        tasks = task_service.get_tasks()

        return jsonify({
            "data": tasks,
            "error": None
        }), 200

    except Exception as e:
        logger.exception("Failed to fetch tasks")
        return jsonify({
            "data": None,
            "error": "Failed to fetch tasks"
        }), 500


# ---------------------------
# GET SINGLE TASK
# ---------------------------
@task_bp.route("/api/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):
    task = task_service.get_task(task_id)

    if not task:
        return jsonify({"error": "Task not found"}), 404

    return jsonify(task), 200


# ---------------------------
# CREATE TASK
# ---------------------------
@task_bp.route("/api/tasks", methods=["POST"])
def create_task():
    try:
        data = request.get_json()

        if not data:
            return jsonify({
                "data": None,
                "error": "Request body is required"
            }), 400

        title = data.get("title")

        if not title or not isinstance(title, str):
            return jsonify({
                "data": None,
                "error": "Field 'title' is required and must be a string"
            }), 400

        logger.info(f"Creating task: {title}")

        new_task = task_service.create_task(title=title)

        return jsonify({
            "data": new_task,
            "error": None
        }), 201

    except Exception:
        logger.exception("Failed to create task")
        return jsonify({
            "data": None,
            "error": "Failed to create task"
        }), 500


# ---------------------------
# UPDATE TASK
# ---------------------------
@task_bp.route("/api/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body is required"}), 400

    result = task_service.update_task(
        task_id,
        title=data.get("title"),
        done=data.get("done")
    )

    if not result:
        return jsonify({"error": "Task not found"}), 404

    return jsonify(result), 200


# ---------------------------
# DELETE TASK
# ---------------------------
@task_bp.route("/api/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    result = task_service.delete_task(task_id)

    if not result:
        return jsonify({"error": "Task not found"}), 404

    return jsonify(result), 200


# ---------------------------
# ROOT
# ---------------------------
@task_bp.route("/")
def home():
    return jsonify({"status": "ok"}), 200
