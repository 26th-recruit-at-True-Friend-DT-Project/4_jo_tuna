from flask import Flask
import sys
from flask import Flask, session, render_template, redirect, request, url_for 

application = Flask(__name__)


@application.route("/")
def main():
    return "Hello goorm!"
    # return render_template("index.html")

@application.route("/")
if __name__ == "__main__":
    application.run(host='0.0.0.0', port="8080")