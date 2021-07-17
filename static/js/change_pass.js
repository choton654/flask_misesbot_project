const pass_error = $("#pass_error")
const confirm_error = $("#conf_error")
const handleChangePass = () => {
    const user_id = window.location.href.split("/")[4]
    const password = $("#new_pass").val()
    const conf_pass = $("#conf_pass").val()
    console.log(password, conf_pass);
    let data = {password}
    if (password === "" || conf_pass === "") {
        console.log("Please enter both password");
        pass_error.removeClass("hidden")
    } else if (password !== conf_pass) {
        console.log("Please confirm your password");
        confirm_error.removeClass("hidden")
    } else {
        fetch(`http://localhost:8000/change_pass/${user_id}`, {
            body: JSON.stringify(data),
            headers: {
                "Content-Type": "application/json"
            },
            method: "POST"
        })
            .then(res => res.json())
            .then(data => {
                console.log(data);
                const {msg} = data
                if (msg === "Password has successfully changed"){
                    window.location.assign("http://localhost:8000/")
                }
            })
            .catch(err => {
                console.log(err);
            })
    }
}
const handleConfirm = () => {
    pass_error.addClass("hidden")
    confirm_error.addClass("hidden")
}
const handlePass = () => {
    pass_error.addClass("hidden")
    confirm_error.addClass("hidden")
}