const pop_up_signin_signup = document.getElementById('pop-up-signin-signup');
const pop_up_signin_signup_hide_btn = document.getElementById('pop-up-signin-signup-hide-btn');
const pop_up_signin_signup_hide_btn2 = document.getElementById('pop-up-signin-signup-hide-btn2');

const pop_up_signin_signup_show_btn = document.getElementById('pop-up-signin-signup-show-btn');
const pop_up_signin_form = document.getElementById('pop-up-signin-form');
const pop_up_signup_form = document.getElementById('pop-up-signup-form');
const pop_up_signup_form_btn = document.getElementById('pop-up-signup-form-btn');
const pop_up_signin_form_btn = document.getElementById('pop-up-signin-form-btn');

// Show SigninSignup Popup
pop_up_signin_signup_show_btn.addEventListener(
    'click',
    function () {
        pop_up_signin_signup.classList.remove('d-none')
        pop_up_signin_signup.classList.add('d-flex')
    }
)
// Hide SigninSignup Popup
pop_up_signin_signup_hide_btn.addEventListener(
    'click',
    function () {
        pop_up_signin_signup.classList.remove('d-flex')
        pop_up_signin_signup.classList.add('d-none')
    }
)
pop_up_signin_signup_hide_btn2.addEventListener(
    'click',
    function () {
        pop_up_signin_signup.classList.remove('d-flex')
        pop_up_signin_signup.classList.add('d-none')
    }
)

// Reduce pop_up_signin_signup_form width on MD screen/ LG Screen
function reduceSigninPopuWidth() {
    if (getScreenWidth > 768) {
        pop_up_signin_form.classList.remove('w-100')
        pop_up_signin_form.classList.add('w-50')
        pop_up_signup_form.classList.remove('w-100')
        pop_up_signup_form.classList.add('w-75')
    } else {
        pop_up_signin_form.classList.remove('w-25')
        pop_up_signin_form.classList.add('w-100')
        pop_up_signup_form.classList.remove('w-25')
        pop_up_signup_form.classList.add('w-100')
    }
}
window.onresize = reduceSigninPopuWidth
window.onload = reduceSigninPopuWidth
window.onloadstart = reduceSigninPopuWidth

// Show Signin Popup
pop_up_signin_form_btn.addEventListener(
    'click',
    function () {
        // Hide Signup 
        pop_up_signup_form.classList.add('d-none')
        pop_up_signup_form.classList.remove('d-block')
        // Show Signin 
        pop_up_signin_form.classList.remove('d-none')
        pop_up_signin_form.classList.add('d-block')
    }
)
// Show Signup Popup
pop_up_signup_form_btn.addEventListener(
    'click',
    function () {
        // Hide Signin 
        pop_up_signin_form.classList.add('d-none')
        pop_up_signin_form.classList.remove('d-block')
        // Show Signup 
        pop_up_signup_form.classList.remove('d-none')
        pop_up_signup_form.classList.add('d-block')
    }
)

const form = document.getElementById("pop-up-signup-form");
const password_error1 = document.getElementById("password-error1");
const password_error2 = document.getElementById("password-error2");

form.addEventListener("submit", function (event) {
    const password = document.getElementById("password").value;
    const confirm_password = document.getElementById("confirm-password").value;

    let hasError = false; // Track if there are any errors

    // Hide Signin
    pop_up_signin_form.classList.add('d-none');
    pop_up_signin_form.classList.remove('d-block');

    // Show Signup
    pop_up_signup_form.classList.remove('d-none');
    pop_up_signup_form.classList.add('d-block');

    // Check password length
    if (password.length < 8) {
        event.preventDefault(); // Prevent form submission
        password_error1.classList.remove('d-none');
        password_error1.classList.add('d-flex');
        password_error1.innerText = "Password length must be at least 8 characters";
        hasError = true;
    } else {
        // Hide error if previously shown
        password_error1.classList.add('d-none');
        password_error1.classList.remove('d-flex');
    }

    // Check if passwords match
    if (password !== confirm_password) {
        event.preventDefault(); // Prevent form submission
        password_error2.classList.remove('d-none');
        password_error2.classList.add('d-flex');
        password_error2.innerText = "Password and Re-typed Password Don't match";
        hasError = true;
    } else {
        // Hide error if previously shown
        password_error2.classList.add('d-none');
        password_error2.classList.remove('d-flex');
    }

    // If there are no errors, allow form submission
    if (!hasError) {
        form.submit(); // Submit the form if everything is okay
    }
});

// Search Tutorial
document.addEventListener("DOMContentLoaded", function () {
    const searchInput = document.getElementById('search');
    const resultHolder = document.getElementById('result-holder');
    const resultHeader = document.getElementById('result-header');

    searchInput.addEventListener('input', function () {
        const query = searchInput.value;
        if (query.length < 2) {
            resultHolder.innerHTML = ''
            resultHeader.classList.remove('d-block');
            resultHeader.classList.add('d-none');
            return;
        }
        fetch('/Home/Search/', {
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
                    resultHeader.classList.add('d-block');
                    resultHolder.innerHTML = result;
                    if (result === '') {
                        let search_input = searchInput.value
                        search_input = search_input.toString()
                        resultHolder.innerHTML = '<p class="text-center text-dark font-weight-bolder">Tutorial With Name "' + search_input + '" Not Found</p>';
                    }
                }
                else {
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

document.addEventListener("DOMContentLoaded", function () {
    const userTypeSelect = document.getElementById('user_type');
    const regNumberLabel = document.getElementById('reg-number-label');
    const regNumberInput = document.getElementById('reg-number-input');

    const lecturerLabel = document.getElementById('lecturer-label');
    const lecturerInput = document.getElementById('lecturer-input');

    userTypeSelect.addEventListener('change', function () {
        if (userTypeSelect.value === '1') {
            // Show registration number field if user is a student
            regNumberLabel.classList.remove('d-none');
            regNumberInput.setAttribute('required', 'required');
            // Show Lecturer input field if user is a student
            lecturerLabel.classList.remove('d-none');
            lecturerInput.setAttribute('required', 'required');
        } else {
            // Hide registration number field if user is not a student
            regNumberLabel.classList.add('d-none');
            regNumberInput.removeAttribute('required');

             // Hide Lecturer input field if user is not a student
             lecturerLabel.classList.add('d-none');
             lecturerInput.removeAttribute('required');
        }
    });
});
