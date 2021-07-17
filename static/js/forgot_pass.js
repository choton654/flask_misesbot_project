const email_error = $("#email_error")
const mail_sent = $("#mail_sent")
const wrong_email = $("#wrong_email")
const valid_email = $("#valid_email")
const forgot_pass = (e) => {
    e.preventDefault()
    const forgot_pass = $("#in_email_forgot_pass").val()
    const data = {
        email: forgot_pass,
    }
    if (forgot_pass === "") {
        console.log("Please enter email");
        email_error.removeClass("hidden")
    } else if (forgot_pass.indexOf("@") === -1) {
        console.log("enter a valid email");
        valid_email.removeClass("hidden")
    } else {
        fetch("http://localhost:8000/forgot_pass", {
            body: JSON.stringify(data),
            headers: {
                "Content-Type": "application/json"
            },
            method: "POST"
        })
            .then((res) => res.json())
            .then((res_data) => {
                console.log(res_data);
                const { not_user, email_sent } = res_data
                if (not_user) {
                    console.log("Enter valid email");
                    wrong_email.removeClass("hidden")
                } else if (email_sent) {
                    console.log("A mail sent to your email");
                    mail_sent.removeClass("hidden")
                }
                // window.location.assign("http://localhost:8000/signup")
            })
            .catch((err) => {
                console.log(err)
            })
    }
}
const handleChange = () => {
    email_error.addClass("hidden")
    mail_sent.addClass("hidden")
    wrong_email.addClass("hidden")
    valid_email.addClass("hidden")

}