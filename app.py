import pandas as pd
from datetime import datetime
from collections import defaultdict
from flask import Flask, session, render_template, redirect, request, url_for 
from utils.rebalancing import rebalance


def get_start_date(name):
    idx = ks_df[ks_df['name']==name].index
    return ks_df['start_date'][idx].values[0]

def get_ticker(name):
    idx = ks_df[ks_df['name']==name].index
    return ks_df['ticker'][idx].values[0]


application = Flask(__name__)

@application.route("/")
def main():
    return render_template("index.html")


@application.route("/quant", methods=['GET', 'POST'])
def quant():
    if request.method == "POST":
        return render_template("backtesting/quant.html", info=info)
    else:
        return render_template("backtesting/quant.html")


@application.route("/rebalancing-korea", methods=['GET', 'POST'])
def rebalancing_korea():
    if request.method == "POST":
        # json 형식의 input value 생성
        info = defaultdict(list)
        for k, v in request.form.lists():
            info[k] = v
        # print(info)
        daily_df, monthly_df, annual_df, total_balance, total_invest_money, metrics = rebalance(info)
        annual_df = round(annual_df*100, 2)
        monthly_df = round(monthly_df*100, 2)
        
        # 일별 정보
        d_label = list(t.strftime("%Y-%m-%d") for t in list(daily_df.index))
        d_port = list(daily_df['backtest'])
        
        # 월별 정보
        m_label = list(t.strftime("%Y-%m") for t in list(monthly_df.index))
        month_dict = defaultdict()
        month_dict['연월'] = m_label
        month_dict['포트폴리오'] = list(monthly_df['backtest'])
        for t in info['ticker']:
            month_dict[t] = list(monthly_df[t])
        
        # 연별 정보
        y_label = list(t.strftime("%Y") for t in list(annual_df.index))
        year_dict = defaultdict()
        year_dict['연도'] = y_label
        year_dict['포트폴리오'] = list(annual_df['backtest'])
        for t in info['ticker']:
            year_dict[t] = list(annual_df[t])
        
        #포트폴리오 개요
        outline = defaultdict(
            ticker = list(get_ticker(name) for name in info['ticker']),
            name = info['ticker'],
            start_date = list(get_start_date(name) for name in info['ticker']),
            ratio = info['ratio']
        )
            
        # 포트폴리오 성과 요약
        annual_result = list(annual_df['backtest'])
        summary = [
            f"{int(info['moneyToStart'][0])}만원",
            f"{int(info['monthlySave'][0])}만원",
            f"{int(total_invest_money)//10000}만원",
            f"{format(int(total_balance), ',')}원",
            f"{max(annual_result)}%",
            f"{min(annual_result)}%",
            metrics['연평균성장률'],
            metrics['최대 손실 낙폭'],
            metrics['샤프 비율']
        ]
        
        return render_template(
            "backtesting/rebalancing-korea.html", 
            daily_port=d_port, 
            daily_label=d_label,
            monthly_port=month_dict,
            monthly_label=m_label,
            annual_port=year_dict,
            annual_label=y_label,
            outline=outline,
            summary=summary,
            metrics=metrics
        )
    else:
        return render_template("backtesting/rebalancing-korea.html")


@application.route("/rebalancing-usa", methods=['GET', 'POST'])
def rebalancing_usa():
    if request.method == "POST":
        info = dict(request.form)
        return render_template("backtesting/rebalancing-usa.html", info=info)
    else:
        return render_template("backtesting/rebalancing-usa.html")

'''
@application.route("/portfolio-guru")
def guru():
    return render_template("portfolio/guru.html")
'''

@application.route("/ray-dalio")
def ray():
    return render_template("portfolio/guru-result.html")


@application.route("/harry-browne")
def harry():
    return render_template("portfolio/guru-result.html")


@application.route("/sixty-forty")
def sixty_forty():
    return render_template("portfolio/guru-result.html")


@application.route("/forty-sixty")
def forty_sixty():
    return render_template("portfolio/guru-result.html")


@application.route("/portfolio-kis")
def kis():
    return render_template("portfolio/sec.html")


@application.route("/portfolio-kb")
def kb():
    return render_template("portfolio/sec.html")


@application.route("/portfolio-samsung")
def samsung():
    return render_template("portfolio/sec.html")


@application.route("/metrics")
def metrics():
    return render_template("utilities/metrics.html")


@application.route("/support")
def support():
    return render_template("utilities/support.html")


@application.route("/search", methods=['GET'])
def search():
    if request.method == 'GET':
        name = request.args.get('company')
        # ks_df = pd.read_csv('utils/data/korea_stock.csv')
        ticker = get_ticker(name)
        return render_template("utilities/search.html", name=name, ticker=ticker)
    
    
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


@application.errorhandler(404)
def page_not_found(error):
    return render_template('utilities/404.html')


@application.errorhandler(500)
def page_not_found(error):
    return render_template('utilities/404.html')

if __name__ == "__main__":
    ks_df = pd.read_csv('utils/data/korea_stock.csv')
    application.run(host='0.0.0.0', port="8080")