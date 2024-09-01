
document.addEventListener('DOMContentLoaded', function() {
const  articleId = "{{ article.id }}"
const author = "{{ user.username }}" ? "{{user.username}}" : 'Guest'
const data = {articleId: articleId, author: author}


//The states of the reactions
let liked_state = '{{ reactions.liked }}'
let disliked_state = "{{ reactions.disliked }}"

//Handling of the view functionality
const view_state = "{{ reactions.viewed }}"

if (view_state  === 'False') {
    fetch('{% url "article_view_count" %}', {
        method: 'POST',
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": "{{ csrf_token }}"
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        let viewCountDiv = document.getElementById('viewcount')
        viewCountDiv.textContent = data.viewcount
    })
    .catch(err => {console.error(err)})
} else {
    // pass
}

//Handling of the like functionality
const likeBtn = document.getElementById('likes')

likeBtn.addEventListener('click', function() {

    data.action = liked_state === 'True' ? 'Remove' : 'Add'
    
    fetch("{% url 'article_like_count' %}", {
        method: 'POST',
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": "{{ csrf_token }}"
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        const likecountdiv = document.getElementById('likecount')
        const likeicon = document.getElementById('like-icon')

        if (data.status === 'Added') {
            likeicon.style.fill = 'chocolate'
            likeicon.style.stroke = 'chocolate'
        } else {
            likeicon.removeAttribute('style')                      
        }

        likecountdiv.textContent = data.likecount
        liked_state = data.status === 'Added' ? 'True' : 'False'
    })
    .catch(err => {
        console.log(err)
    })

    disliked_state === "True" ? dislikeBtn.click() : null
})

//Fucntionality for the dislikes
const dislikeBtn = document.getElementById('dislikes')
const dislikecount = document.getElementById('dislikecount')
const dislikeIcon = document.getElementById('dislike-icon')

dislikeBtn.addEventListener('click', function() {
    data.action = disliked_state === 'True' ? 'Remove' : 'Add'

    fetch("{% url 'article_dislike_count' %}",{
        method: 'POST',
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": "{{ csrf_token }}"
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === "Added") {
            dislikeIcon.style.fill = "chocolate"
            dislikeIcon.style.stroke = 'chocolate'
        } else {
            dislikeIcon.removeAttribute('style')
        }

        dislikecount.textContent = data.dislikecount
        disliked_state = data.status === "Added" ? 'True' : 'False'
    })
    .catch(err => {
        console.error(err)
    })
    
    liked_state === "True" ? likeBtn.click() : null

})

//Functionality for adding bookmark
const bookmarkbtn = document.getElementById('saves')
let saveState = "{{ reactions.saved }}"

bookmarkbtn.addEventListener('click', function() {

    data.action = saveState === 'True' ? 'Remove' : 'Add'

    fetch("{% url 'article_save_count' %}", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            "X-CSRFToken": "{{ csrf_token }}"
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        const saveicon = document.getElementById('save-icon')

        if (data.status === 'Added') {
            saveicon.style.fill = 'chocolate'
            saveicon.style.stroke = 'chocolate'
        } else {
            saveicon.removeAttribute('style')
        }
        
        document.getElementById('savecount').textContent = data.savecount
        saveState = data.status === 'Added' ? 'True' : 'False'
    })
    .catch(err => {
        console.error(err)
    })

}) 

//Functionality for the display of the comments and addition of new ones
const commentBtn = document.getElementById('comments')
const commentContainer = document.getElementById('comments-container')

commentBtn.addEventListener('click', function() {
    commentContainer.style.display = commentContainer.style.display === "flex" ? 'none' : 'flex'
})

const commentinput = document.getElementById('comment')
const sendcomment = document.getElementById('sendcomment')

sendcomment.addEventListener('click', () => {
    const inputval = commentinput.value
    data.content = inputval

    fetch("{% url 'article_comment_count' %}", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            "X-CSRFToken": "{{ csrf_token }}"
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        console.log(data)
        document.getElementById('commentcount').textContent = data.commentcount
        commentinput.value = ''
    })
    .catch(err => {
        console.error('Error submiting comment:', err)
    })
})

})

// Handling the display of the various reaction-links
const reactionLinks = document.querySelectorAll('.reactionlink');
const reactionContainers = document.querySelectorAll('.reaction-container');

let hideTimeout; // Declare the hideTimeout globally to manage timeouts

reactionLinks.forEach((element, index) => {
// Show the corresponding reaction container on mouseover
element.addEventListener('mouseover', function() {
    // Cancel any hide timeouts if they exist
    clearTimeout(hideTimeout);

    // Hide all other reaction containers
    reactionContainers.forEach(container => {
        container.style.display = 'none';
    });

    // Show the current reaction container
    reactionContainers[index].style.display = 'flex';
});

// Handle mouseout on the trigger element
element.addEventListener('mouseout', function() {
    const container = reactionContainers[index];

    // Start a timeout to hide the container after a delay
    hideTimeout = setTimeout(() => {
        container.style.display = 'none';
    }, 2000);
});

// Ensure the container stays visible while the mouse is over it
reactionContainers[index].addEventListener('mouseover', function() {
    clearTimeout(hideTimeout); // Prevent hiding while hovering over the container
});

// Hide the container when the mouse leaves it
reactionContainers[index].addEventListener('mouseout', function() {
    hideTimeout = setTimeout(() => {
        reactionContainers[index].style.display = 'none';
    }, 2000); // Delay to allow quick re-entry
});
});
