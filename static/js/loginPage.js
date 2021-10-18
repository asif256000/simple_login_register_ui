
let x = document.getElementById("login")
let y = document.getElementById("register")
let z = document.getElementById("btn")

function register_shadow_shift() {
    x.style.left = "-420px";
    y.style.left = "30px";
    z.style.left = "100px";
}

function login_shadow_shift() {
    x.style.left = "30px";
    y.style.left = "430px";
    z.style.left = "0px";
}

function validate_password(userPassword) {
    var res;
    var str = document.getElementById("t1").value;
    if (str.match(/[a-z]/g) && str.match(
        /[A-Z]/g) && str.match(
        /[0-9]/g) && str.match(
        /[^a-zA-Z\d]/g) && str.length >= 8)
        res = "TRUE";
    else
        res = "FALSE";
    document.getElementById("t2").value = res;
}

function validate_username(userId) {
    var res;
    var str = document.getElementById("t1").value;
    if (str.match(/[a-z]/g) && str.match(
        /[A-Z]/g) && str.match(
        /[0-9]/g) && str.match(
        /[^a-zA-Z\d]/g) && str.length >= 8)
        res = "TRUE";
    else
        res = "FALSE";
    document.getElementById("t2").value = res;
}

function togglePw(toggleId, pwId) {
    const togglepw = document.getElementById(toggleId)
    let password = document.getElementById(pwId)

    togglepw.addEventListener('click', function (e) {
        // toggle the type attribute
        const type = password.getAttribute('type') === 'password' ? 'text' : 'password';
        password.setAttribute('type', type);
        // toggle the eye / eye slash icon
        this.classList.toggle('bi-eye');
    });
}

togglePw('togglePasswordLogin', 'passwordLogin')
togglePw('togglePasswordRegn', 'passwordRegn')