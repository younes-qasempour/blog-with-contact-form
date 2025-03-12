from flask import Flask, render_template, request
import requests
import smtplib
from dotenv import load_dotenv
import os

load_dotenv()
posts = requests.get("https://gist.githubusercontent.com/gellowg/389b1e4d6ff8effac71badff67e4d388/raw/"
                     "fc31e41f8e1a6b713eafb9859f3f7e335939d518/data.json").json()

def send_email(name, email, phone, message):
    email_message = f"Subject:New Message\n\nName: {name}\nEmail: {email}\nPhone: {phone}\nMessage:{message}"
    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.starttls()
        connection.login(os.getenv("EMAIL"), os.getenv("PASSWORD"))
        connection.sendmail(os.getenv("EMAIL"), os.getenv("EMAIL"), email_message)

app = Flask(__name__)


@app.route('/')
def get_all_posts():
    return render_template("index.html", all_posts=posts)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact", methods=['POST', 'GET'])
def contact():
    if request.method == 'POST':
        data = request.form
        send_email(data['name'], data['email'], data['phone'], data['message'])
        return render_template("contact.html", msg_sent=True)
    return render_template("contact.html", msg_sent=False)


@app.route("/post/<int:index>")
def show_post(index):
    requested_post = None
    for blog_post in posts:
        if blog_post["id"] == index:
            requested_post = blog_post
    return render_template("post.html", post=requested_post)


if __name__ == "__main__":
    app.run(debug=True, port=5001)
