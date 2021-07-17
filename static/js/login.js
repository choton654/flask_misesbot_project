const error = $("#error")
const emailError = $("#email_error")
const passInvalid = $("#invalid_pass")
const userInvalid = $("#invalid_user")
const handleLogin = (e) => {
    e.preventDefault();
    const email = $("#in_login_email").val();
    const password = $("#in_login_password").val();
    const data = {
        email: email,
        password: password,
    }
    if (email === "" || password === "") {
        error.removeClass("hidden");
        console.log("Please enter email and password");
    } else if (email.indexOf("@") === -1 || email.indexOf(".") === -1) {
        emailError.removeClass("hidden");
    } else {
        fetch("http://localhost:8000/login", {
            body: JSON.stringify(data),
            headers: {
                "Content-Type": "application/json"
            },
            method: "POST"
        })
            .then((res) => res.json())
            .then((res_data) => {
                console.log(res_data);
                const { email, not_email, not_pass, not_user } = res_data
                if (email !== undefined) {
                    window.location.assign("http://localhost:8000/")
                } else if (not_email !== undefined) {
                    window.location.assign("http://localhost:8000/verify_email")
                } else if (not_pass !== undefined) {
                    passInvalid.removeClass("hidden")
                    console.log("password didn't match");
                } else if (not_user !== undefined) {
                    userInvalid.removeClass("hidden")
                    console.log("user not found");
                } else {
                    console.log("invalid response");
                }
            })
            .catch((err) => {
                console.log(err)
            })
    }
}
const handleGoogleLogin = (e) => {
    e.preventDefault();
    // console.log(e);
}

const handleFacebookLogin = (e) => {
    e.preventDefault();
    // console.log(e);
}
const handleEmailChange = () => {
    emailError.addClass("hidden");
    error.addClass("hidden");
    passInvalid.addClass("hidden");
    userInvalid.addClass("hidden");
}
const handlePasswordChange = () => {
    emailError.addClass("hidden");
    error.addClass("hidden");
    passInvalid.addClass("hidden");
    userInvalid.addClass("hidden");
}