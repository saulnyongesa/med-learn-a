document.addEventListener("DOMContentLoaded", function () {
    function saveChanges() {
        const tutorial_id = document.getElementById('tutorial-id').innerText;
        let name = document.getElementById('tutorial-name').innerText;
        let description = document.getElementById('tutorial-description').innerText;
        if (name.toString() === ''){
            name = 'No name'
        }
        if (description.toString() === ''){
            description = 'Tutorial Description'
        }
        // Replace with the URL where your server handles saving
        fetch('/Author/Tutorial/Save/' + tutorial_id + '/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken()  // Django CSRF token, adjust if needed
            },
            body: JSON.stringify({
                name: name,
                description: description
            })
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    window.location.href = "/Author/Tutorial/Edit/" + tutorial_id + "/"
                } else {
                    alert('Failed to save changes.');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Error saving changes.');
            });
    }

    function getCsrfToken() {
        const cookies = document.cookie.split(';');
        for (const cookie of cookies) {
            const [name, value] = cookie.split('=');
            if (name.trim() === 'csrftoken') {
                return value;
            }
        }
        return '';
    }

    document.getElementById('tutorial-name').addEventListener('blur', saveChanges);
    document.getElementById('tutorial-description').addEventListener('blur', saveChanges);
});

document.addEventListener("DOMContentLoaded", function () {
    function saveTopicChanges(topicId, field, value) {
        const tutorialId = document.getElementById('tutorial-id').innerText;
        fetch('/Author/Tutorial/Topic/Save/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken()  // Adjust if needed
            },
            body: JSON.stringify({
                id: topicId,
                field: field,
                value: value
            })
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    window.location.href = "/Author/Tutorial/Edit/" + tutorialId + "/"
                } else {
                    window.location.href = "/Author/Tutorial/Edit/" + tutorialId + "/"
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
    }

    function getCsrfToken() {
        const cookies = document.cookie.split(';');
        for (const cookie of cookies) {
            const [name, value] = cookie.split('=');
            if (name.trim() === 'csrftoken') {
                return value;
            }
        }
        return '';
    }

    document.querySelectorAll('.editable-topic-name, .editable-topic-notes').forEach(element => {
        element.addEventListener('blur', function () {
            const topicId = this.closest('.card-body').dataset.topicId;
            const field = this.dataset.field;
            const value = this.innerText;

            saveTopicChanges(topicId, field, value);
        });
    });
});


// Create Topic 
// Show Popup
const create_topic_btn = document.getElementById('create-topic-btn')
const create_topic_fields = document.getElementById('create-topic-fields')

create_topic_btn.addEventListener(
    'click',
    function () {
        create_topic_fields.classList.add('d-block')
        create_topic_fields.classList.remove('d-none')
        create_topic_btn.classList.add('d-none')
    }
)
document.getElementById('save-topic-btn').addEventListener(
    'click',
    function () {
        function createTopic() {
            const tutorialId = document.getElementById('tutorial-id').innerText;
            const name = document.getElementById('create-topic-name').innerText;
            const notes = document.getElementById('create-topic-notes').value;
            fetch('/Author/Tutorial/Topic/Create/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCsrfToken()  // Adjust if needed
                },
                body: JSON.stringify({
                    id: tutorialId,
                    name: name,
                    notes: notes
                })
            })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        create_topic_fields.classList.add('d-none')
                        create_topic_fields.classList.remove('d-block')
                        create_topic_btn.classList.remove('d-none')
                        create_topic_btn.classList.add('d-block')
                        window.location.href = "/Author/Tutorial/Edit/" + tutorialId + "/"
                    } else {
                        alert('Failed to Create Topic.');
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                });
        }

        function getCsrfToken() {
            const cookies = document.cookie.split(';');
            for (const cookie of cookies) {
                const [name, value] = cookie.split('=');
                if (name.trim() === 'csrftoken') {
                    return value;
                }
            }
            return '';
        }
        createTopic()
    }
)
