import os
from App.constants import PATH_DATA
from App.libs.libs import dash, pl


def get_list_stock_names() -> list:
    list_stock_names = []
    for stock_name in os.listdir(PATH_DATA):
        list_stock_names.append({
            'value': stock_name,
            'label': dash.html.Span([stock_name])
        })
    return list_stock_names


def format_graph(fig):
    fig.update_layout(
        title='Gráfico de Candlesticks',
        xaxis_title='Data',
        yaxis_title='Preço',
        xaxis_rangeslider_visible=False
    )
    return fig


def get_data_stock(cur_stock: str, period: str) -> pl.DataFrame:
    path_data = PATH_DATA / f'{cur_stock}/{cur_stock}_{period}.csv'
    df = pl.read_csv(path_data, try_parse_dates=True)
    return df


# if __name__ == '__main__':
    # print(gen_table('AAPL'))
    # format_graph('BTC-USD', '1d')
