from App.libs.libs import BeautifulSoup, requests, PoolManager, Timeout, re


class GetRealTimePriceStock:
    """
    Classe responsável por capturar, em tempo real, o preço de uma ação
    """

    _USER_AGENT: dict = {'User-Agent': 'Mozilla/5.0', 'Accept-Encoding': 'gzip'}
    _http: PoolManager
    _NAMECLASS_WEBSCRAPING: str = 'yf-1tejb6'

    def __init__(self) -> None:
        """
        Método construtor da classe
        """
        self._http = PoolManager(headers=self._USER_AGENT, timeout=Timeout(connect=2.0, read=7.0))

    @staticmethod
    def _web_content_div(web_content: BeautifulSoup, class_path: str) -> list:
        """
        Método estático que realiza a busca e retorna o conteúdo encontrado num  elemento html "div" da página

        :param web_content: Conteúdo da página
        :param class_path: classe de um elemento html usado para busca do conteúdo desejado
        :return: retorna o texto encontrado
        """
        web_content_div = web_content.find_all('div', {'class': re.compile(class_path)})
        try:
            spans = web_content_div[0].find_all('span')
            texts = [span.get_text() for span in spans]
        except IndexError:
            texts = []

        return texts

    def real_time_price(self, stock_code: str) -> tuple:
        """
        Captura o preço de uma ação em tempo real

        :param stock_code: Código da ação (ex: BTC)
        :param class_path: classe de um elemento html usado para busca do conteúdo desejado
        :return: retorna as informações da ação, em tempo real
        """
        url = f'https://finance.yahoo.com/quote/{stock_code}/history'
        try:
            response = self._http.request('GET', url, headers=self._USER_AGENT)
            web_content = BeautifulSoup(response.data, 'lxml')
            texts = self._web_content_div(web_content, self._NAMECLASS_WEBSCRAPING)
            if texts:
                price, change, pct_change = texts[0], texts[1], texts[2]
            else:
                price, change, pct_change = [], [], []
        except requests.ConnectionError:
            price, change, pct_change = [], [], []

        return price, change, pct_change
