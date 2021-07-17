// const login_btn = $("#btn_login")
const handleLogin = () => {
    window.location.assign("http://localhost:8000/login")
}

const handleLogout = () => {
    fetch("http://localhost:8000/logout", {
        method: "POST"
    }).then(res => {
        console.log(res.data);
        window.location.assign("http://localhost:8000/")
    })
        .catch(err => {
            console.log(err);
        })
}