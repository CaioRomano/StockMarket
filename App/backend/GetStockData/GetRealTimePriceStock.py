import typing

from App.libs.libs import requests, ray, BeautifulSoup


@ray.remote(num_cpus=6)
class GetRealTimePriceStock:
    """
    Classe Responsável por recuperar dados em tempo real da variação do preço em tempo real da ação especificada
    """

    _USER_AGENT: dict = {'User-Agent': 'Mozilla/5.0'}
    _stock_price: typing.Dict[str, typing.Dict[str, float]] = dict()
    _stock_name: str

    def __init__(self, stock_name: str) -> None:
        """
        Método construtor da classe

        :param stock_name: Nome da ação da qual deseja coletar dados de preço em tempo real.
        """
        self._stock_name = stock_name

    def get_stock_price(self) -> typing.Dict[str, typing.Dict[str, float]]:
        """
        Retorna os dados sobre os preços da ação
        :return: Dados dos preços da ação
        """
        return self._stock_price

    def get_stock_name(self) -> str:
        """
        Retorna o nome da ação

        :return: Retorna nome da ação
        """
        return self._stock_name

    def set_stock_name(self, stock_name: str) -> None:
        """
        Insere nova ação

        :param stock_name: Nome da ação
        """
        self._stock_name = stock_name

    def _is_connected(self) -> typing.Union[bool, typing.Any]:
        """
        Verifica conexão com a internet

        :return: Retorna True se estiver conectado a internet, junto com o conteúdo da página,
        e retorna False se não estiver conectado
        """
        try:
            url = f'https://finance.yahoo.com/quote/{self._stock_name}/history'
            response = requests.get(url, headers=self._USER_AGENT)
            if response.status_code == 200:
                response.raise_for_status()
                return True, response
            return False, 0
        except ConnectionError as e:
            print(e)
            print('Sem conexão da internet!')

    @staticmethod
    def _web_scraping(response: typing.Any) -> typing.Tuple[float, float, float]:
        """
        Realiza web scraping dos dados da internet

        :param response: Conteúdo da página
        :return: Retorna uma tupla com os valores relacionados a ação
        """
        soup = BeautifulSoup(response.content, 'html.parser')
        price_stream = float(soup.find('fin-streamer', class_='livePrice').get('data-value'))
        percent_value_stream = float(
            soup.find('fin-streamer', attrs={'data-field': 'regularMarketChangePercent'}).get('data-value'))
        change_value_stream = float(
            soup.find('fin-streamer', attrs={'data-field': 'regularMarketChange'}).get('data-value'))
        return price_stream, change_value_stream, percent_value_stream

    def get_realtime_price(self) -> None:
        """
        Coleta dados referentes ao preço da ação
        """
        is_connected, response = self._is_connected()
        if is_connected:
            price_stream, change_value_stream, percent_value_stream = self._web_scraping(response)

            self._stock_price[self._stock_name] = {
                'live_price': price_stream,
                'change-price': change_value_stream,
                'pct-change-price': percent_value_stream
            }

    def run(self) -> None:
        """
        Executa a ação de captura dos preços das ações
        """
        self.get_realtime_price()


if __name__ == '__main__':
    """
    Determinar o futuro dessa classe
    """
    sd = GetRealTimePriceStock.remote(stock_name='TSLA')
    sd.run.remote()
    print(ray.get(sd.get_stock_price.remote()))
