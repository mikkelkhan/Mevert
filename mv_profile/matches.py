from flask import Flask, request, render_template,Blueprint,jsonify,url_for
import pyodbc
from configparser import ConfigParser
from string import Template
from flask import session
import logging
from datetime import datetime

mv_profile_matches = Blueprint("matches",__name__)
config = ConfigParser()
config.read("config.ini")
def get_connection():
    return pyodbc.connect(config["MSSQL"]["connect"])



@mv_profile_matches.route('/api/matches', methods=["GET"])
def fetch_matches():
    username = session.get('username')
    if not username:
        return {"error": "Unauthorized"}, 401

    cnxn = get_connection()

    cursor = cnxn.cursor()
    try:
        query = Template(config["Query"]["matches_data"]).safe_substitute(username=username)
        fetch_data = cursor.execute(query)
        all_data = cursor.fetchall()

        data = [
            {
                "username": row[0],
                "profile_url": url_for('profile.other_profile', other_username=row[0]),
                "name": row[1],
                "age": row[2]
            }
            for row in all_data
        ]
        return jsonify(data)
    finally:
        cursor.close()
        cnxn.close()


@mv_profile_matches.route('/api/decline_matches/<string:other_username>', methods=["POST"])
def decline_matches(other_username):
    username = session.get('username')
    if not username:
        return jsonify({"error": "User not logged in"}), 401
    cnxn = get_connection()
    cursor = cnxn.cursor()
    try:
        query = Template(config["Query"]["decline_matches"]).safe_substitute(receiver=other_username, username=username)

        cursor.execute(query)
        cnxn.commit()
    except Exception as e:
        logging.error(f"Error declining match: {e}")
        return jsonify({"error": "Failed to decline match"}), 500

    return jsonify({"status": "success"})

@mv_profile_matches.route('/api/accept_matches/<string:other_username>', methods=["POST"])
def accept_matches(other_username):
    username = session.get('username')
    if not username:
        return jsonify({"error": "User not logged in"}), 401

    try:
        cnxn = get_connection()
        cursor = cnxn.cursor()

        query = """
        UPDATE Matches
        SET status = '1'
        WHERE username = ? AND receiver = ?
        """

        cursor.execute(query, (other_username, username))


        cursor.execute("""
                    SELECT id FROM Matches
                    WHERE username = ? AND receiver = ?
                """, (other_username, username))

        row = cursor.fetchone()

        if not row:
            return jsonify({"error": "Match not found"}), 404

        match_id = row[0]


        cursor.execute("""
                    INSERT INTO chat_messages (match_id, sender_username, message, created_at)
                    VALUES (?, ?, ?, ?)
                """, (match_id, "Mevert", "You are now matched! Say hello!", datetime.utcnow()))


        cnxn.commit()

        cursor.close()
        cnxn.close()

        return jsonify({"status": "accepted"})

    except Exception as e:
        logging.error(f"Error accepting match: {e}")
        return jsonify({"error": "Failed to accept match"}), 500