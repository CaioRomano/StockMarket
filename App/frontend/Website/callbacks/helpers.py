import os
from App.constants import PATH_DATA
from App.libs.libs import dash, pl, np, go


def get_list_stock_names() -> list:
    list_stock_names = []
    for stock_name in os.listdir(PATH_DATA):
        list_stock_names.append({
            'value': stock_name,
            'label': dash.html.Span([stock_name])
        })
    return list_stock_names


def gen_graph(df, fig, graph_type):
    if graph_type == 'Candlestick':
        fig.add_trace(go.Candlestick(x=df['Date'],
                                     open=df['Open'],
                                     high=df['High'],
                                     low=df['Low'],
                                     close=df['Close'],
                                     showlegend=False,
                                     hoverinfo='x+y',
                                     name='candle_graph'),
                      secondary_y=True)
    elif graph_type == 'Line':
        fig.add_trace(go.Scatter(x=df['Date'],
                                 y=df['Close'],
                                 line=dict(color='rgba(255, 255, 255, 0.9)', width=1),
                                 mode='lines',
                                 connectgaps=True,
                                 hovertemplate='price: %{y}<extra></extra>',
                                 showlegend=False,
                                 name='line_graph'),
                      secondary_y=True)

    fig.add_trace(go.Bar(x=df['Date'],
                         y=df['Volume'],
                         showlegend=False,
                         marker={
                             'color': 'rgba(128, 128, 128, 0.5)',
                             'line': {'width': 0}},
                         customdata=format_big_numbers(df['Volume']),
                         hovertemplate='volume: %{customdata}<extra></extra>'),
                  secondary_y=False)
    fig.update_yaxes(secondary_y=True, showgrid=True)
    fig.update_yaxes(secondary_y=False, showgrid=False, showticklabels=False)

    return fig


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
        hovermode='x'
    )
    fig.update_xaxes(showgrid=False, zeroline=False, showline=False)
    fig.update_yaxes(zeroline=False, showline=False, gridcolor='rgba(255, 255, 255, 0.05)')
    return fig


def get_data_stock(cur_stock: str, period: str) -> pl.DataFrame:
    path_data = PATH_DATA / f'{cur_stock}/{cur_stock}_{period}.csv'
    df = pl.read_csv(path_data, try_parse_dates=True)
    return df


def format_big_numbers(nums):
    nums = np.array(nums)
    suffixes = ['', 'K', 'M', 'B', 'T']
    result = []
    for num in nums:
        if num == 0:
            result.append('0')
        else:
            magnitude = min(int(np.floor(np.log10(abs(num)) / 3)), 4)
            formatted_num = num / (1000 ** magnitude)
            result.append(f'{formatted_num:.2f}{suffixes[magnitude]}')
    return result


# if __name__ == '__main__':
# print(gen_table('AAPL'))
# format_graph('BTC-USD', '1d')
