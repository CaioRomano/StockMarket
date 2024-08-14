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
                                 line=dict(color='rgba(255, 255, 255, 1)', width=2),
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
    rolling_mean_df = calculate_rolling_mean(df)
    fig = gen_rolling_mean_graphs(rolling_mean_df=rolling_mean_df, fig=fig)

    return fig


def gen_rolling_mean_graphs(rolling_mean_df, fig):
    period_list = (15, 25, 72)
    alpha = 0.9
    colors_lines = (f'rgba(255, 130, 0, {alpha})', f'rgba(0, 0, 255, {alpha})', f'rgba(255, 0, 255, {alpha})')
    term_list = ('Short', 'Medium', 'Long')
    for i in range(len(period_list)):
        hovertemplate_str = f'{term_list[i]} Term: '
        fig.add_trace(go.Scatter(x=rolling_mean_df['Date'],
                                 y=rolling_mean_df[f'{period_list[i]}_days_RM'],
                                 connectgaps=True,
                                 hovertemplate=hovertemplate_str + '%{y}<extra></extra>',
                                 mode='lines',
                                 line=dict(color=colors_lines[i], width=1),
                                 name=f'{term_list[i]} ({period_list[i]} days)'),
                      secondary_y=True)
    fig.update_layout(legend_title_text='Rolling Mean Term')
    return fig


def calculate_rolling_mean(df):
    periods_list = (15, 25, 72)
    new_columns = [pl.col('Date')]
    for period in periods_list:
        new_columns.append(pl.col('Close').rolling_mean(window_size=period).alias(f'{period}_days_RM'))
    rolling_mean_df = df.select(new_columns)
    return rolling_mean_df


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
