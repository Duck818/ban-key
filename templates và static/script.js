function showSection(sectionId) {
    document.querySelectorAll("main section").forEach(section => {
        section.style.display = "none";
    });
    document.getElementById(sectionId).style.display = "block";
}

// Lưu thông tin tài khoản
function saveUserData(email, password) {
    localStorage.setItem("user", JSON.stringify({ email, password, coin: 0, keys: [] }));
}

function getUserData() {
    return JSON.parse(localStorage.getItem("user"));
}

// Đăng ký tài khoản
function register() {
    let email = document.getElementById("register-email").value;
    let password = document.getElementById("register-password").value;

    if (!email || !password) {
        alert("Vui lòng nhập đầy đủ thông tin!");
        return;
    }

    if (getUserData()) {
        alert("Email đã tồn tại!");
        return;
    }

    saveUserData(email, password);
    alert("Đăng ký thành công! Hãy đăng nhập.");
}

// Đăng nhập tài khoản
function login() {
    let email = document.getElementById("login-email").value;
    let password = document.getElementById("login-password").value;
    let userData = getUserData();

    if (userData && userData.email === email && userData.password === password) {
        alert("Đăng nhập thành công!");
        document.getElementById("user-info").textContent = `Xin chào, ${email}! Số coin: ${userData.coin}`;
    } else {
        alert("Sai email hoặc mật khẩu!");
    }
}

// Mua key
function buyKey(days) {
    let userData = getUserData();
    if (!userData) {
        alert("Bạn cần đăng nhập trước khi mua key!");
        return;
    }

    let price = { 1: 5000, 3: 15000 }[days];

    if (userData.coin >= price) {
        userData.coin -= price;
        userData.keys.push(`Key ${days} ngày`);
        localStorage.setItem("user", JSON.stringify(userData));
        alert("Mua key thành công!");
    } else {
        alert("Bạn không đủ coin!");
    }
}

// Cập nhật số coin khi nạp tiền
function depositCoins(amount) {
    let userData = getUserData();
    if (userData) {
        userData.coin += amount;
        localStorage.setItem("user", JSON.stringify(userData));
        alert(`Bạn đã nạp ${amount} coin thành công!`);
    } else {
        alert("Bạn cần đăng nhập để nạp tiền.");
    }
}
