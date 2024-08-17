from App.libs.libs import typing
from App.backend.GetStockData.GetRealTimePriceStock import GetRealTimePriceStock
from App.backend.GetStockData.GetDataStockMarket import GetDataStockMarket


def execute_get_price_stock(stock_code: str, class_path: typing.Any = None) -> tuple:
    """
    Recupera informações de uma ação de uma página web

    :param stock_code: Código da ação (ex: BTC)
    :param class_path: classe de um elemento html usado para busca do conteúdo desejado
    :return: retorna valores das ações (Preço real, variação do preço e variação do preço em porcentagem)
    """
    if class_path:
        info_stock = GetRealTimePriceStock().real_time_price(stock_code=stock_code, class_path=class_path)
    else:
        info_stock = GetRealTimePriceStock().real_time_price(stock_code=stock_code)
    return info_stock


def execute_get_data_stock(stock_code: str) -> None:
    """
    Recupera os dados históricos de uma ação

    :param stock_code: Código da ação (ex: BTC)
    """
    stock_code = ''.join(stock_code.upper().split(',')).split()
    getdata = GetDataStockMarket(stock_name=stock_code, interval='all')
    getdata.run()
