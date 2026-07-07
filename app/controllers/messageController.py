from flask import render_template, request, redirect, url_for, session, flash, abort
from app.auth import login_required
from app.repository import user_repo


@login_required
def inbox():
    partners = user_repo.get_conversation_partners(session["user_id"])
    return render_template("dashboard/inbox.html", partners=partners)


@login_required
def conversation(other_id):
    me = session["user_id"]
    other = user_repo.get_user_by_id(other_id)
    if not other:
        abort(404)

    messages = user_repo.get_conversation(me, other_id)
    return render_template("dashboard/conversation.html", other=other, messages=messages)


@login_required
def send(other_id):
    body = request.form.get("body", "").strip()
    if body:
        other = user_repo.get_user_by_id(other_id)
        if other:
            user_repo.send_message(session["user_id"], other_id, body)
    return redirect(url_for("message.conversation", other_id=other_id))