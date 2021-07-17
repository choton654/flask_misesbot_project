const username = $("#in_signup_username")
const email = $("#in_signup_email")
const phone = $("#in_signup_phone")
const password = $("#in_signup_password")
const errorText = $("#error")
const emailError = $("#email_error")
const phoneError = $("#phone_error")


const handleSignup = (e) => {
    e.preventDefault();
    let usernameVal = username.val()
    let emailVal = email.val()
    let phoneVal = phone.val()
    let passwordVal = password.val()
    const data = {
        username: usernameVal,
        email: emailVal,
        phone: phoneVal,
        password: passwordVal
    }
    console.log(data)
    if (usernameVal === "" || emailVal === "" || phoneVal === "" || passwordVal === "") {
        errorText.removeClass("hidden");
        console.log("please fill up all fields");
    } else if (emailVal.indexOf("@") === -1 || emailVal.indexOf(".") === -1) {
        emailError.removeClass("hidden");
        console.log("enter a valid email");
    } else if (phoneVal.length !== 10 || isNaN(parseInt(phoneVal))) {
        phoneError.removeClass("hidden");
        console.log("PLease enter a 10 digit phone number");
    } else {
        fetch("http://localhost:8000/signup", {
            body: JSON.stringify(data),
            headers: {
                "Content-Type": "application/json"
            },
            method: "POST"
        })
            .then((res) => res.json())
            .then((res_data) => {
                const { user, duplicate } = res_data
                if (user !== undefined) {
                    console.log(JSON.parse(user))
                    username.val("")
                    email.val("")
                    phone.val("")
                    password.val("")
                    window.location.assign("http://localhost:8000/login")
                } else if (duplicate !== undefined) {
                    console.log(duplicate);
                    if (duplicate.indexOf["@"] !== -1) {
                        email.val("Email already exists")
                        email.css("background-color", "#eeeeee")
                    }
                }
                console.log(res_data);
            })
            .catch((err) => {
                console.log(err)
            })
    }
}

const handleEmailChange = (e) => {
    console.log(e);
    errorText.addClass("hidden");
    emailError.addClass("hidden");
    phoneError.addClass("hidden");
}

