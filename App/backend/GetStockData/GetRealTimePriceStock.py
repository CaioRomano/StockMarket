from App.libs.libs import BeautifulSoup, requests, PoolManager, Timeout, re


class GetRealTimePriceStock:
    _USER_AGENT: dict = {'User-Agent': 'Mozilla/5.0', 'Accept-Encoding': 'gzip'}
    _http: PoolManager

    def __init__(self):
        self._http = PoolManager(headers=self._USER_AGENT, timeout=Timeout(connect=2.0, read=7.0))

    @staticmethod
    def _web_content_div(web_content, class_path):
        web_content_div = web_content.find_all('div', {'class': re.compile(class_path)})
        try:
            spans = web_content_div[0].find_all('span')
            texts = [span.get_text() for span in spans]
        except IndexError:
            texts = []

        return texts

    def real_time_price(self, stock_code: str, class_path: str = 'yf-mgkamr'):
        url = f'https://finance.yahoo.com/quote/{stock_code}/history'
        try:
            response = self._http.request('GET', url, headers=self._USER_AGENT)
            web_content = BeautifulSoup(response.data, 'lxml')
            texts = self._web_content_div(web_content, class_path)
            if texts:
                price, change, pct_change = texts[0], texts[1], texts[2]
            else:
                price, change, pct_change = [], [], []
        except requests.ConnectionError:
            price, change, pct_change = [], [], []

        return price, change, pct_change
