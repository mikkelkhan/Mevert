from flask import Flask, request, render_template,Blueprint,jsonify
import pyodbc
from flask_socketio import join_room, emit
from configparser import ConfigParser
from string import Template
from flask import session
from datetime import datetime

mv_chats = Blueprint("chats",__name__,url_prefix="/api")
config = ConfigParser()
config.read("config.ini")
def get_connection():
    return pyodbc.connect(config["MSSQL"]["connect"])

from extensions import socketio
@socketio.on('join')
def on_join(room):
    join_room(room)


#SEND MESSAGE
@socketio.on('send_message')
def handle_send_message(data):
    match_id = data.get("match_id")
    message = data.get("message")
    sender_username = session.get("username")

    if not message:
        return

    try:

        cnxn = get_connection()
        cursor = cnxn.cursor()

        cursor.execute("""
            INSERT INTO chat_messages (match_id, sender_username, message, created_at)
            VALUES (?, ?, ?, ?)
        """, (match_id, sender_username, message, datetime.utcnow()))

        cnxn.commit()
        cursor.close()
        cnxn.close()

        room = f"match_{match_id}"

        emit("new_message", {
            "match_id": match_id,
            "sender_username": sender_username,
            "message": message
        }, room=room)

    except Exception as e:
        print(e)

@mv_chats.route('/chat_users', methods=['GET'])
def get_chat_users():
    username = session.get("username")
    if not username:
        return jsonify({"error": "Unauthorized"}), 401

    cnxn = get_connection()
    cursor = cnxn.cursor()

    cursor.execute("""
        SELECT DISTINCT 
            m.id,
            CASE 
                WHEN m.username = ? THEN m.receiver
                ELSE m.username
            END AS other_user
        FROM Matches m
        JOIN chat_messages c ON c.match_id = m.id
        WHERE (m.username = ? OR m.receiver = ?)
        AND m.status = 1
        ORDER BY m.id DESC
    """, (username, username, username))

    rows = cursor.fetchall()

    users = []
    for row in rows:
        users.append({
            "match_id": row[0],
            "other_user": row[1]
        })

    cursor.close()
    cnxn.close()

    return jsonify(users)

@mv_chats.route('/chat_messages/<int:match_id>', methods=['GET'])
def get_messages(match_id):
    cnxn = get_connection()
    cursor = cnxn.cursor()

    cursor.execute("""
        SELECT sender_username, message, created_at
        FROM chat_messages
        WHERE match_id = ?
        ORDER BY created_at ASC
    """, (match_id,))

    rows = cursor.fetchall()

    messages = []
    for row in rows:
        messages.append({
            "sender_username": row[0],
            "message": row[1],
            "created_at": str(row[2])
        })

    cursor.close()
    cnxn.close()

    return jsonify(messages)