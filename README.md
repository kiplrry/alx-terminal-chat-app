🖥️ Terminal Chat App

📜 Overview

The Terminal Chat App is a command-line based chat application built using Python. Leveraging Prompt Toolkit, Socket.IO, and SQLAlchemy, this app allows users to connect, join chat rooms, and exchange messages in real-time.
✨ Features

    🔐 User Authentication: Register and log in securely.
    💬 Chat Rooms: Create and join multiple chat rooms.
    ⚡ Real-Time Messaging: Instant messaging between users.
    🖥️ Command-Line Interface: User-friendly CLI using Prompt Toolkit.
    🗄️ Persistent Storage: Data stored with SQLAlchemy and MySQL.

📋 Requirements

    Python 3.10+
    MySQL
    Python libraries (install via pip):
        prompt_toolkit
        sqlalchemy
        socketio
        eventlet
        MySQLdb

🛠️ Installation

    Clone the repository

    bash

git clone https://github.com/yourusername/terminal-chat-app.git
cd terminal-chat-app

Install dependencies

bash

pip install -r requirements.txt

Configure the database

    Create a MySQL database and update the database connection settings in app/database.py.

Initialize the database

python

from app.database import Base, engine
Base.metadata.create_all(engine)

Run the server

bash

gunicorn -k eventlet --reload --threads 60 run:app
