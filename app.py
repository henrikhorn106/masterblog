import json

from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


@app.route('/')
def index():
    with open('blog_posts.json') as f:
        blog_posts = json.load(f)
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        content = request.form['content']

        with open('blog_posts.json', 'r') as f:
            blog_posts = json.load(f)

        # Get id of next post
        next_id = len(blog_posts) + 1

        post = {
            'id': next_id,
            'title': title,
            'author': author,
            'content': content
        }

        blog_posts.append(post)

        with open('blog_posts.json', 'w') as f:
            json.dump(blog_posts, f)

        return redirect(url_for('index'))

    return render_template('add.html')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
