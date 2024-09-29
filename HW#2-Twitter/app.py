from flask import Flask, request, jsonify, render_template
from mastodon import Mastodon

app = Flask(__name__)

# Serve the index.html template
@app.route('/')
def serve_index():
    return render_template('index.html')

# Initialize Mastodon client with your credentials
mastodon = Mastodon(
    client_id='7iITmbhzR0EbK8-XjJVMuwwSUZbi-LiZWhNVyrVnrL0',
    client_secret='5oI9KFU-MMBNdJvNm8IFDwvOJMWJhuRNo02THAqWJxE',
    access_token='x7wgyaFogOoI04OWOnJpKcY7GnI0Fv33xU60vystSP0',
    api_base_url='https://mastodon.social'  # Use your instance URL
)

@app.route('/create', methods=['POST'])
def create_post():
    """Create a new post."""
    post_content = request.data.decode('utf-8')
    if not post_content:
        return jsonify({"error": "Post content is required"}), 400
    post = mastodon.status_post(post_content)
    print(post, post['id'])
    return jsonify({"id": post['id'], "content": post['content']}), 201

@app.route('/retrieve/<post_id>', methods=['GET'])
def retrieve_post(post_id):
    """Retrieve a post by its ID."""
    try:
        post = mastodon.status(post_id)  # Fetch the post from Mastodon
        return jsonify({"content": post['content']}), 200  # Return post content as JSON
    except Exception as e:
        return jsonify({"error": str(e)}), 404  # Return error message as JSON

@app.route('/delete/<post_id>', methods=['DELETE'])
def delete_post(post_id):
    """Delete a post by its ID."""
    try:
        mastodon.status_delete(post_id)  # Delete the post using Mastodon API
        return jsonify({"id": post_id, "message": "Post deleted successfully."}), 200  # Success message
    except Exception as e:
        return jsonify({"error": str(e)}), 404  # Return error message if deletion fails

if __name__ == '__main__':
    app.run(debug=True)
