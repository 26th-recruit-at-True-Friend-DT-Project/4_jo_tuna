from flask import Flask, session, render_template, redirect, request, url_for 

application = Flask(__name__)

@application.route("/")
def main():
    return render_template("index.html")


@application.route("/quant-korea")
def quant_korea():
    return render_template("backtesting/quant-korea.html", ticker=ticker)


@application.route("/quant-usa")
def quant_usa():
    return render_template("backtesting/quant-usa.html")


@application.route("/rebalancing-korea", methods=['GET', 'POST'])
def rebalancing_korea():
    if request.method == "POST":
        info = dict(request.form)
        return render_template("backtesting/rebalancing-korea.html", info=info)
    else:
        return render_template("backtesting/rebalancing-korea.html")


@application.route("/rebalancing-usa", methods=['GET', 'POST'])
def rebalancing_usa():
    if request.method == "POST":
        info = dict(request.form)
        return render_template("backtesting/rebalancing-usa.html", info=info)
    else:
        return render_template("backtesting/rebalancing-usa.html")


@application.route("/portfolio-guru")
def guru():
    return render_template("portfolio/guru.html")


@application.route("/portfolio-kis")
def kis():
    return render_template("portfolio/kis.html")


@application.route("/portfolio-kb")
def kb():
    return render_template("portfolio/kb.html")


@application.route("/metrics")
def metrics():
    return render_template("utilities/metrics.html")


@application.route("/support")
def support():
    return render_template("utilities/support.html")


@application.route("/search", methods=['GET'])
def search():
    if request.method == 'GET':
        # ticker = request.form['ticker'] --> POST용임
        ticker = request.args.get('ticker')
        return render_template("utilities/search.html", name=ticker)
    
    
@application.route("/profile")
def profile():
    return render_template("users/user-profile.html")


@application.route("/holdings")
def holdings():
    return render_template("users/user-holdings.html")


@application.route("/login")
def login():
    return render_template("users/before-login.html")


@application.route("/register")
def register():
    return render_template("users/before-register.html")


@application.route("/profile/modify")
def user_modify():
    return render_template("users/user-modify.html")


@application.route("/forgot-password")
def forgot_password():
    return render_template("users/before-password.html")


@application.route("/404")
def page_not_found():
    return render_template("utilities/404.html")


@application.route("/blank")
def blank():
    return render_template("utilities/blank.html")


@application.route("/reference")
def reference():
    return render_template("reference.html")


if __name__ == "__main__":
    application.run(host='0.0.0.0', port="8080")