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
        font={'color': 'rgba(255, 255, 255, 1)', 'size': 14},
        margin=dict(l=20, r=20, t=20, b=20),
        height=400,
        title=None,
        xaxis_title=None,
        yaxis_title=None,
        xaxis_rangeslider_visible=False,
        yaxis=dict(side='right'),
        paper_bgcolor='rgba(0, 0, 0, 0)',
        plot_bgcolor='rgba(0, 0, 0, 0)',
    )
    fig.update_xaxes(showgrid=False, zeroline=False, showline=False)
    fig.update_yaxes(zeroline=False, showline=False, gridcolor='rgba(255, 255, 255, 0.05)')
    return fig


def get_data_stock(cur_stock: str, period: str) -> pl.DataFrame:
    path_data = PATH_DATA / f'{cur_stock}/{cur_stock}_{period}.csv'
    df = pl.read_csv(path_data, try_parse_dates=True)
    return df


# if __name__ == '__main__':
    # print(gen_table('AAPL'))
    # format_graph('BTC-USD', '1d')
