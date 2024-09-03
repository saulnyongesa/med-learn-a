const create_cat_pop_up = document.getElementById('create-cat-pop-up');
const create_cat_pop_up_show_btn = document.getElementById('create-cat-pop-up-show-btn');
const create_cat_pop_up_hide_btn = document.getElementById('create-cat-pop-up-hide-btn');


// Show Create Cat Popup
create_cat_pop_up_show_btn.addEventListener(
    'click',
    function () {
        create_cat_pop_up.classList.remove('d-none')
        create_cat_pop_up.classList.add('d-flex')
    }
)
// Hide Create Cat Popup
create_cat_pop_up_hide_btn.addEventListener(
    'click',
    function () {
        create_cat_pop_up.classList.remove('d-flex')
        create_cat_pop_up.classList.add('d-none')
    }
)

// Search Tutorial
document.addEventListener("DOMContentLoaded", function () {
    const searchInput = document.getElementById('search');
    const resultHolder = document.getElementById('result-holder');
    const resultHeader = document.getElementById('result-header');

    searchInput.addEventListener('input', function () {
        const query = searchInput.value;
        if (query.length < 2) {
            resultHolder.innerHTML = ''
            resultHeader.classList.remove('d-flex');
            resultHeader.classList.add('d-none');
            return;
        }
        fetch('/Author/Tutorial/Search/', {
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
                    for (let i in data.data) {
                        result += `<a class="btn btn-link w-100 p-1 m-1 text-left font-weight-bolder" href="/Student/Tutorial/View/${data.data[i].id}/">${data.data[i].name}  <span class="text-secondary">By: ${data.data[i].user__username}</span></a><br>`;
                    }
                    resultHeader.classList.remove('d-none');
                    resultHeader.classList.add('d-flex');
                    resultHolder.innerHTML = result;
                    if(result === ''){
                        let search_input = searchInput.value
                        search_input = search_input.toString()
                        resultHolder.innerHTML = '<p>Tutorial With Name "' + search_input + '" Not Found</p>';
                    }
                }
                else{
                    resultHolder.innerHTML = '<p class="text-danger">No Tutorial Found</p>'
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
