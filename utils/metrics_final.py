# 라이브러리
import numpy as np
import pandas as pd
import pprint
from itertools import groupby, chain
import FinanceDataReader as fdr
from scipy.stats import norm

# 클래스 선언
class Core():
    def __init__(self):
        self.annual=252
    # 산술평균 수익률
    def average(self, returns):
        return returns.mean()*self.annual
    # 기하평균 수익률
    def cagr(self, returns):
        return (1+returns).prod() ** (self.annual/len(returns))-1
    # 표준편차
    def stdev(self, returns):
        return returns.std() * np.sqrt(self.annual)
    # 하방 표준편차
    def downdev(self, returns, target=0.0):
        returns = returns.copy()
        returns.loc[returns>target]=0
        summation = (returns ** 2).sum()
        return np.sqrt(self.annual * summation / len(returns))
    # 상방 표준편차
    def updev(self, returns, target=0.0):
        returns = returns.copy()
        returns.loc[returns < target] = 0
        summation = (returns ** 2).sum()
        return np.sqrt(self.annual * summation / len(returns))
    # 공분산
    def covar(self, returns, benchmark):
        return returns.cov(benchmark) * self.annual
    # 상관계수
    def correl(self, returns, benchmark):
        return returns.corr(benchmark)
    # 베타
    def beta(self, returns, benchmark):
        return returns.cov(benchmark) / returns.std() ** 2
    # 알파 : R펀드실제 －[R무위험 ＋ β펀드 {E(R시장) －R무위험 }]
    def alpha(self, returns, benchmark):
        return (1+returns).prod() - (r_f + (returns.cov(benchmark)/returns.std() ** 2)) * (benchmark.mean() - r_f)
        
    # 한번에 출력
    def print_result(self, returns, benchmark, target=0.0):
        average = self.average(returns)
        cagr = self.cagr(returns)
        stdev = self.stdev(returns)
        downdev = self.downdev(returns, target)
        updev = self.updev(returns, target)
        covar = self.covar(returns, benchmark)
        correl = self.correl(returns, benchmark)
        beta = self.beta(returns, benchmark)
        alpha = self.alpha(returns, benchmark)
        result = {"산술평균" : average,
              "CAGR": cagr,
              "표준편차": stdev,
              "하방 표준편차": downdev,
              "상방 표준편차": updev,
              "공분산": covar,
              "상관계수": correl,
                 "베타": beta,
                 "알파" : alpha}
        return result


def get_product(KEY, STAT_CD, PERIOD, START_DATE, END_DATE):
    # 무위험 금리(CD91) 불러오기
    # 파이썬에서 인터넷을 연결하기 위해 urllib 패키지 사용. urlopen함수는 지정한 url과 소켓 통신을 할 수 있도록 자동 연결해줌
    import requests
    from bs4 import BeautifulSoup
    import pandas as pd
    from lxml import html
    from urllib.request import Request, urlopen
    from urllib.parse import urlencode, quote_plus, unquote
    import pprint

    url = 'http://ecos.bok.or.kr/api/StatisticSearch/{}/xml/kr/1/30000/{}/{}/{}/{}/{}' \
            .format(KEY # 인증키
                   , STAT_CD # 추출할 통계지표의 코드
                   , PERIOD # 기간 단위
                   , START_DATE # 데이터 시작일
                   , END_DATE # 데이터 종료일
                   , ITEM_CODE )# 통계항목 코드

    response = requests.get(url).content.decode('utf-8')
    
    xml_obj = BeautifulSoup(response, 'lxml-xml')
    # xml_obj
    rows = xml_obj.findAll("row")
    return rows


if __name__ == "__main__":
    
    start_date = '2012-01-01'
    end_date = '2023-01-19'

    kospi = fdr.DataReader('KS11', start_date, end_date)
    pf_return=back_test_result3['일변화율'].dropna()    # 함수에 따라서 달라지는 전략
    kospi_ret = kospi['Close'].pct_change().dropna()

    # 1. Core Analytics
    core = Core()
    core_result = core.print_result(pf_return, kospi_ret)
    
    # 2. Tail-Risk Analytics
    tail = Tail()
    tail_result = tail.print_result(pf_return, kospi_ret)
    
    # 3. Performance Evaluation Analytics
    perform = Performance()
    perform_result = perform.print_result(pf_return, kospi_ret)
        
    table = {**core_result, **tail_result, **perform_result}
    
    result = pd.Series(table)
    result = result.to_frame()
    result