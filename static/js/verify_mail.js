const verify_mail = (e) => {
    e.preventDefault();
    const email = $("#in_verify_email").val()
    const data = { email }
    if (email === "") {
        console.log("Please enter email");
    } else if (email.indexOf("@") === -1) {
        console.log("enter a valid email");
    } else {
        fetch("http://localhost:8000/verify_email", {
            body: JSON.stringify(data),
            headers: {
                "Content-Type": "application/json"
            },
            method: "POST"
        })
            .then((res) => res.json())
            .then((res_data) => {
                const { email_sent, email, user } = res_data
                if (email_sent !== undefined) {
                    console.log(JSON.parse(user));
                    window.location.assign("http://localhost:8000/")
                } else {
                    console.log(email);
                }
            })
            .catch((err) => {
                console.log(err)
            })
    }
}