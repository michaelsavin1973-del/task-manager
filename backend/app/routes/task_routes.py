from flask import Blueprint, request, jsonify
from app.services import task_service
import logging

task_bp = Blueprint("tasks", __name__)

logger = logging.getLogger(__name__)


# ---------------------------
# HEALTHCHECK (DEVOPS MUST)
# ---------------------------
@task_bp.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok"
    }), 200


# ---------------------------
# GET TASKS (with safe response)
# ---------------------------
@task_bp.route("/api/tasks")
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
# CREATE TASK (production safe)
# ---------------------------
@task_bp.route("/api/tasks")
def create_task():
    try:
        data = request.get_json()

        # ---- validation ----
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

        # ---- service layer ----
        new_task = task_service.create_task(title=title)

        return jsonify({
            "data": new_task,
            "error": None
        }), 201

    except Exception as e:
        logger.exception("Failed to create task")
        return jsonify({
            "data": None,
            "error": "Failed to create task"
        }), 500
@task_bp.route("/api/tasks", methods=["DELETE"])
def delete_task(task_id):
    result = task_service.delete_task(task_id)

    if "error" in result:
        return jsonify(result), 404

    return jsonify(result), 200

@task_bp.route("/api/tasks", methods=["PUT"])
def update_task(task_id):
    data = request.get_json()

    result = task_service.update_task(
        task_id,
        title=data.get("title"),
        done=data.get("done")
    )

    if not result:
        return jsonify({"error": "Task not found"}), 404

    return jsonify(result)
@task_bp.route("/api/tasks", methods=["GET"])
def get_task(task_id):
    task = task_service.get_task(task_id)

    if not task:
        return jsonify({"error": "Task not found"}), 404

    return jsonify(task)


