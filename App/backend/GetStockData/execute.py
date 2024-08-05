from App.libs.libs import typing
from App.backend.GetStockData.GetRealTimePriceStock import GetRealTimePriceStock
from App.backend.GetStockData.GetDataStockMarket import GetDataStockMarket


def execute_get_price_stock(stock_code: str, class_path: typing.Any = None) -> dict:
    if class_path:
        info_stock = GetRealTimePriceStock().real_time_price(stock_code=stock_code, class_path=class_path)
    else:
        info_stock = GetRealTimePriceStock().real_time_price(stock_code=stock_code)
    return info_stock


def execute_get_data_stock(stock_code):
    stock_code = ''.join(stock_code.upper().split(',')).split()
    getdata = GetDataStockMarket(stock_name=stock_code, interval='all')
    getdata.run()


# if __name__ == '__main__':
#     execute_get_data_stock('AAPL, tsla, gc=f')