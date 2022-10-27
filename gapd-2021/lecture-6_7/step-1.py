from flask import Flask


app = Flask(__name__)


# Return "Hello, World!" on the homepage
@app.route('/')
def hello_world():
    return 'Hello, World!'


# Start a simple web server
if __name__ == '__main__':
    app.run()
