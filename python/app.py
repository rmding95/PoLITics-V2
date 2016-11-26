from flask import Flask
from flaskext.mysql import MySQL

app = Flask(__name__)
mysql = MySQL()
app.config['MYSQL_DATABASE_HOST'] = 'politicsdb.cdcme9z9rkbx.us-west-2.rds.amazonaws.com'
mysql.init_app(app)

@app.route('/todo/')
def index():
    conn = mysql.connect()
    cursor = conn.cursor()
    return 'Hello World!'

if __name__ == '__main__':
    app.run(debug=True)