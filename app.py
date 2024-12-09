from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Database setup
def init_db():
    with sqlite3.connect("data/journal.db") as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS journal (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            date TEXT,
                            trigger TEXT,
                            thought TEXT,
                            symptoms TEXT,
                            behaviors TEXT,
                            rational_thought TEXT,
                            coping_actions TEXT,
                            outcome TEXT
                        )''')

@app.route("/", methods=["GET", "POST"])
def journal():
    if request.method == "POST":
        # Get form data
        entry = (
            request.form['date'],
            request.form['trigger'],
            request.form['thought'],
            request.form['symptoms'],
            request.form['behaviors'],
            request.form['rational_thought'],
            request.form['coping_actions'],
            request.form['outcome']
        )
        # Save entry to database
        with sqlite3.connect("data/journal.db") as conn:
            conn.execute("INSERT INTO journal (date, trigger, thought, symptoms, behaviors, rational_thought, coping_actions, outcome) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", entry)
        return redirect(url_for("journal"))

    # Display entries
    with sqlite3.connect("data/journal.db") as conn:
        entries = conn.execute("SELECT * FROM journal").fetchall()
    return render_template("journal.html", entries=entries)

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
