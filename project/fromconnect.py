from flask import Flask, request, render_template_string
import psycopg2


app = Flask(__name__)

# Database connection parameters
DB_PARAMS = {
    'host': 'localhost',
    'database': 'postgres',
    'user': 'postgres',
    'password': '12345678'  # Replace with your PostgreSQL password
}

# HTML form template
FORM_HTML = open("project/template/from.html", "r").read()

@app.route('/')
def index():
    return render_template_string(FORM_HTML)

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']

    try:
        # Establish database connection
        conn = psycopg2.connect(**DB_PARAMS)
        cursor = conn.cursor()

        # Insert form data into the database
        cursor.execute(
            "INSERT INTO submissions (name, email, message) VALUES (%s, %s, %s)",
            (name, email, message)
        )
        conn.commit()

        return "Thank you for your submission!"

    except Exception as e:
        return f"An error occurred: {e}"

    finally:
        if conn:
            cursor.close()
            conn.close()

if __name__ == '__main__':
    app.run(debug=True)
