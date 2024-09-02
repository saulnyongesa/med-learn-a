// Cat Submission
document.addEventListener("DOMContentLoaded", function() {
    const forms = document.querySelectorAll("form[id^='form-']");
    forms.forEach(form => {
        form.addEventListener("change", function(event) {
            event.preventDefault();
            const formData = new FormData(form);
            const questionId = form.getAttribute("id").split('-')[1];
            const savedMessage = document.getElementById(`saved-${questionId}`);

            fetch(`/Cat/Response/Save/${questionId}`, {
                method: "POST",
                body: formData,
                headers: {
                    'X-CSRFToken': formData.get('csrfmiddlewaretoken')
                },
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    savedMessage.classList.remove('d-none');
                }
            })
            .catch(error => console.error('Error:', error));
        });
    });
});
