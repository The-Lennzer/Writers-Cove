// Infinite Scroll Functionality
const feed = document.getElementById('feed');
const loading = document.getElementById('loading');

// Dummy Posts for Demonstration
const dummyPosts = [
    {
        author: 'Alice Brown',
        timestamp: '6 hours ago',
        title: 'The Mystery of the Lost Key',
        content: 'There was an old mansion at the edge of the town...',
    },
    {
        author: 'Chris Evans',
        timestamp: '8 hours ago',
        title: 'Journey to the Stars',
        content: 'The spaceship roared as it lifted off the ground...',
    },
    {
        author: 'Sophia Grace',
        timestamp: '10 hours ago',
        title: 'A Day in the Life of a Detective',
        content: 'Detective Jones always started his day with a black coffee...',
    },
];

// Simulate API call to load more posts
function loadMorePosts() {
    loading.style.display = 'block';

    setTimeout(() => {
        dummyPosts.forEach((post) => {
            const postDiv = document.createElement('div');
            postDiv.classList.add('post');

            postDiv.innerHTML = `
                <div class="post-header">
                    <span class="author">Posted by: ${post.author}</span>
                    <span class="timestamp">${post.timestamp}</span>
                </div>
                <h2 class="post-title">${post.title}</h2>
                <p class="post-content">${post.content}</p>
            `;

            feed.appendChild(postDiv);
        });

        loading.style.display = 'none';
    }, 1500); // Simulate network delay
}

// Detect Scroll to Bottom
window.addEventListener('scroll', () => {
    if (window.innerHeight + window.scrollY >= document.body.offsetHeight - 10) {
        loadMorePosts();
    }
});
