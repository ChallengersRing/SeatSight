
let title = document.querySelector("#title");
let account_form = document.querySelector("#account");
let nameField = document.querySelector("#nameField");
let signupBtn = document.querySelector("#signupBtn");
let signinBtn = document.querySelector("#signinBtn");
let cr_act = document.querySelector("#cr_act");
let lg_act = document.querySelector("#lg_act");

lg_act.onclick = function () {
    console.log("signin clicked");
    title.innerHTML = "Sign In";
    nameField.style.display = 'none';
    lg_act.style.display = 'none';
    cr_act.style.display = 'block';
    signupBtn.style.display = 'none';
    signinBtn.style.display = 'block';
    account_form.action = 'signin/';
}

cr_act.onclick = function () {
    console.log("signup clicked");
    title.innerHTML = "Sign Up";
    nameField.style.display = 'block';
    cr_act.style.display = 'none';
    lg_act.style.display = 'block';
    signupBtn.style.display = 'block';
    signinBtn.style.display = 'none';
    account_form.action = 'signup/';
}

function postData(formData, url) {
    var xhr = new XMLHttpRequest();
    xhr.open("POST", url, true);

    // Construct the payload object with additional user data
    var payload = {
        browser: {
            userAgentData: navigator.userAgentData,
            userAgent: navigator.userAgent,
            language: navigator.language,
            platform: navigator.platform,
            cookiesEnabled: navigator.cookieEnabled,
            online: navigator.onLine,
            vendor: navigator.vendor,
            product: navigator.product,
            appVersion: navigator.appVersion,
            appName: navigator.appName
        }
    };
    console.log(payload)

    // Append the JSON payload as a field in the FormData
    formData.append('payload', JSON.stringify(payload));

    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4) {
            var response = JSON.parse(xhr.responseText);
            if (xhr.status === 200) {
                document.querySelector("#result").innerHTML = response['result'];
                console.log("Success:", xhr.status, response);
                if (response['result'] === "SignUp Successful") {
                    setTimeout(function () {
                        lg_act.click();
                        document.querySelector("#result").innerHTML = response['result'] + "\nPlease Login";
                    }, 1000);
                }
                if (response['result'] === "SignIn Successful") {
                    setTimeout(function () {
                        window.location.href = "/";
                    }, 1000);
                }
            } else {
                document.querySelector("#result").innerHTML = response['result'];
                console.log("Error:", xhr.status, response);
            }
        }
    };

    xhr.send(formData);
}

// Add form submission event listener
account_form.addEventListener('submit', function (event) {
    event.preventDefault();
    const formData = new FormData(this);
    const url = this.getAttribute('action');
    postData(formData, url)
});