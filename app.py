from flask import Flask, request, session, redirect, url_for, render_template_string
from auth import authenticate

app = Flask(__name__)
app.secret_key = "rbac_secret_key"

login_page = """
<h2>Login</h2>
<form method="POST">
  Username: <input name="username"><br><br>
  Password: <input name="password" type="password"><br><br>
  <button type="submit">Login</button>
</form>
"""

home_page = """
<h2>Welcome {{user}}</h2>
<p>Role: {{role}}</p>

<a href="/admin">Admin Page</a><br>
<a href="/user">User Page</a><br>
<a href="/logout">Logout</a>
"""

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = authenticate(request.form["username"], request.form["password"])
        if user:
            session["user"] = request.form["username"]
            session["role"] = user["role"]
            return redirect(url_for("home"))
        return "Invalid login credentials"

    return login_page


@app.route("/home")
def home():
    if "user" not in session:
        return redirect(url_for("login"))

    return render_template_string(
        home_page,
        user=session["user"],
        role=session["role"]
    )


@app.route("/admin")
def admin():
    if session.get("role") != "admin":
        return "Access Denied 🚫"
    return "Welcome Admin Panel 🔐"


@app.route("/user")
def user():
    if "user" not in session:
        return redirect(url_for("login"))
    return "Welcome User Dashboard 👤"


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)
