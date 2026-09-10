(function () {
  function render(data) {
    var nav = document.querySelector(".main-nav ul");
    if (!nav) return;

    if (!data || !data.authenticated) {
      var loginLi = document.createElement("li");
      var loginA = document.createElement("a");
      loginA.href = "/login.html?next=" + encodeURIComponent(window.location.pathname);
      loginA.textContent = "Log In";
      loginLi.appendChild(loginA);
      nav.appendChild(loginLi);
      return;
    }

    if (data.role === "admin") {
      var adminLi = document.createElement("li");
      adminLi.innerHTML = '<a href="/admin" class="admin-dashboard-link">Admin Dashboard</a>';
      nav.appendChild(adminLi);
    }

    var accountLi = document.createElement("li");
    accountLi.innerHTML = '<a href="/account.html">My Account</a>';
    nav.appendChild(accountLi);

    var li = document.createElement("li");
    var a = document.createElement("a");
    a.href = "#";
    a.textContent = "Log Out (" + data.username + ")";
    a.addEventListener("click", function (e) {
      e.preventDefault();
      fetch("/.netlify/functions/logout", { method: "POST" }).then(function () {
        window.location.href = "/index.html";
      });
    });
    li.appendChild(a);
    nav.appendChild(li);
  }

  fetch("/.netlify/functions/session")
    .then(function (res) { return res.json(); })
    .then(function (data) { render(data); })
    .catch(function () { render(null); });
})();
