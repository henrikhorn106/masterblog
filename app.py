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
        title = request.form.get('title')
        author = request.form.get('author')
        content = request.form.get('content')

        with open('blog_posts.json', 'r') as f:
            blog_posts = json.load(f)

        # Get id of next post
        next_id = len(blog_posts) + 1

        post = {
            'id': next_id,
            'author': author,
            'title': title,
            'content': content
        }

        blog_posts.append(post)

        with open('blog_posts.json', 'w') as f:
            json.dump(blog_posts, f)

        return redirect(url_for('index'))

    return render_template('add.html')


@app.route('/delete/<int:post_id>')
def delete(post_id):
    with open('blog_posts.json', 'r') as f:
        blog_posts = json.load(f)

    list_index = 0
    for index, post in enumerate(blog_posts):
        if post['id'] == post_id:
            list_index = index

    blog_posts.pop(list_index)

    with open('blog_posts.json', 'w') as f:
        json.dump(blog_posts, f)

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
