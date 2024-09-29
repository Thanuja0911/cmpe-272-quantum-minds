document.addEventListener("DOMContentLoaded", () => {
    const createPostForm = document.getElementById("createPostForm");
    const deletePostForm = document.getElementById("deletePostForm");
    const retrievePostForm = document.getElementById("retrievePostForm");
    const createResult = document.getElementById("createResult");
    const deleteResult = document.getElementById("deleteResult");
    const retrieveResult = document.getElementById("retrieveResult");

    // Create post
    createPostForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        const postText = document.getElementById("postText").value;
        if (postText.trim() === "") {
            createResult.textContent = "Please enter post text.";
            return;
        }

        const response = await fetch("http://127.0.0.1:5000/create", {
            method: "POST",
            headers: {
                "Content-Type": "text/plain",
            },
            body: postText,
        });

        if (response.ok) {
            const data = await response.json();
            createResult.textContent = `Post created successfully! Post ID: ${data.id}`;
        } else {
            createResult.textContent = "Error creating post.";
        }
    });

    // Retrieve post
    retrievePostForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        const postId = document.getElementById("retrievePostId").value;
        if (postId.trim() === "") {
            retrieveResult.textContent = "Please enter post ID.";
            return;
        }

        const response = await fetch(`http://127.0.0.1:5000/retrieve/${postId}`, {
            method: "GET",
        });

        // const response = await fetch("http://localhost:5000/retrieve", {
        //     method: "POST",
        //     headers: {
        //         "Content-Type": "text/plain",
        //     },
        //     body: postId,
        // });

        if (response.ok) {
            const data = await response.json();
            retrieveResult.textContent = `Post content: ${data.content}`;
        } else {
            retrieveResult.textContent = "Error retrieving post.";
        }
    });

    // Delete post
    deletePostForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        const postId = document.getElementById("deletePostId").value;
        if (postId.trim() === "") {
            deleteResult.textContent = "Please enter post ID.";
            return;
        }

        try {
            const response = await fetch(`http://127.0.0.1:5000/delete/${postId}`, {
                method: "DELETE",
            });
    
            if (response.ok) {
                deleteResult.textContent = "Post deleted successfully!";
            } else {
                deleteResult.textContent = "Error deleting post.";
            }
        } catch (error) {
            console.error("Error:", error);
            deleteResult.textContent = "Error deleting post.";
        }
    });
});
