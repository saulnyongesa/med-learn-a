// Search CAT
document.addEventListener("DOMContentLoaded", function () {
    const searchInput = document.getElementById('search');
    const resultHolder = document.getElementById('result-holder');
    const resultHeader = document.getElementById('result-header');

    searchInput.addEventListener('input', function () {
        const query = searchInput.value;
        if (query.length === 0) {
            resultHolder.innerHTML = ''
            resultHeader.classList.remove('d-flex');
            resultHeader.classList.add('d-none');
            resultHolder.classList.remove('d-flex');
            resultHolder.classList.add('d-none');
            return;
        }
        fetch('/Student/Search/Cat/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken()  // Adjust if needed
            },
            body: JSON.stringify({
                query: query,
            })
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    let result = '';
                    result += ` <div class="m-auto w-100">
                                        <p>CAT NAME: ${data.data.name} </p> 
                                        <p>LECTURER USERNAME: ${data.data.username}</p>
                                        <p>START: ${data.data.start}</p>
                                        <p>END: ${data.data.end}</p>
                                        <a class="btn btn-secondary w-100" href="/Student/Cat/View/${data.data.id}/">Open</a> </div>
                                        </div>
                                        `;
                    resultHeader.classList.remove('d-none');
                    resultHeader.classList.add('d-flex');
                    resultHolder.classList.remove('d-none');
                    resultHolder.classList.add('d-flex');
                    resultHolder.innerHTML = result;
                    if (result === '') {
                        let search_input = searchInput.value
                        search_input = search_input.toString()
                        resultHeader.classList.remove('d-none');
                        resultHeader.classList.add('d-flex');
                        resultHolder.classList.remove('d-none');
                        resultHolder.classList.add('d-flex');
                        resultHolder.innerHTML = '<p>CAT with ID: "' + search_input + '" Not Found</p>';
                    }
                }
                else {
                    resultHeader.classList.remove('d-none');
                    resultHeader.classList.add('d-flex');
                    resultHolder.classList.remove('d-none');
                    resultHolder.classList.add('d-flex');
                    resultHolder.innerHTML = '<p class="text-danger">CAT Not Found</p>'
                }
            });
    }
    );
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
});