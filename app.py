import json

from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


def fetch_blog_posts():
    with open('blog_posts.json') as f:
        blog_posts = json.load(f)
    return blog_posts


def save_blog_posts(blog_posts):
    with open('blog_posts.json', 'w') as f:
        json.dump(blog_posts, f)


def fetch_post_by_id(post_id):
    blog_posts = fetch_blog_posts()
    for post in blog_posts:
        if post['id'] == post_id:
            return post
    return None


@app.route('/')
def index():
    blog_posts = fetch_blog_posts()
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        title = request.form.get('title')
        author = request.form.get('author')
        content = request.form.get('content')

        # Get id of next post
        blog_posts = fetch_blog_posts()
        next_id = len(blog_posts) + 1

        post = {
            'id': next_id,
            'author': author,
            'title': title,
            'content': content
        }

        blog_posts.append(post)
        save_blog_posts(blog_posts)

        return redirect(url_for('index'))

    return render_template('add.html')


@app.route('/delete/<int:post_id>')
def delete(post_id):
    blog_posts = fetch_blog_posts()
    post = fetch_post_by_id(post_id)
    blog_posts.remove(post)
    save_blog_posts(blog_posts)

    return redirect(url_for('index'))


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    # Fetch the blog posts from the JSON file
    post = fetch_post_by_id(post_id)
    if post is None:
        # Post not found
        return "Post not found", 404

    if request.method == 'POST':
        # Update the post in the JSON file
        blog_posts = fetch_blog_posts()

        for post in blog_posts:
            if post['id'] == post_id:
                post['author'] = request.form.get('author')
                post['title'] = request.form.get('title')
                post['content'] = request.form.get('content')

        save_blog_posts(blog_posts)

        # Redirect back to index
        return redirect(url_for('index'))

    return render_template('update.html', post=post)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
