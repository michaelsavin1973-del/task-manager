from app.db.db import db
from app.models.task import Task


def get_tasks():
    tasks = Task.query.order_by(Task.id).all()

    return [
        {"id": t.id, "title": t.title, "done": t.done}
        for t in tasks
    ]


def get_task(task_id):
    task = Task.query.get(task_id)

    if not task:
        return None

    return {
        "id": task.id,
        "title": task.title,
        "done": task.done
    }


def create_task(title):
    task = Task(title=title)

    db.session.add(task)
    db.session.commit()   # 🔥 FIX CRITICAL

    return {
        "id": task.id,
        "title": task.title,
        "done": task.done
    }


def update_task(task_id, title=None, done=None):
    task = Task.query.get(task_id)

    if not task:
        return None

    if title:
        task.title = title

    if done is not None:
        task.done = done

    db.session.commit()

    return {
        "id": task.id,
        "title": task.title,
        "done": task.done
    }


def delete_task(task_id):
    task = Task.query.get(task_id)

    if not task:
        return {"error": "Task not found"}

    db.session.delete(task)
    db.session.commit()

    return {"message": "deleted", "id": task_id}
