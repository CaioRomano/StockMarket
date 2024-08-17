from App.constants import PATH_DATA
from App.libs.libs import dash, pl, np, go, os, typing


def get_list_stock_names() -> list:
    """
    Recupera o código de todas as ações existentes e salvas no dispositivo

    :return: retorna lista das ações existentes e salvas no dispositivo
    """
    list_stock_names = []
    for stock_name in os.listdir(PATH_DATA):
        list_stock_names.append({
            'value': stock_name,
            'label': dash.html.Span([stock_name])
        })
    return list_stock_names


def gen_graph(df: pl.DataFrame, fig: go.Figure, graph_type: str) -> go.Figure:
    """
    Cria o gráfico, de acordo com o tipo passado

    :param df: Dados históricos da ação
    :param fig: Figure do plotly que armazenará os gráficos
    :param graph_type: tipo de gráfico que será criado
    :return: retorna uma Figure do dash que contém os gráficos pertinentes
    """
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
                         customdata=format_big_numbers_of_volume(df['Volume']),
                         hovertemplate='volume: %{customdata}<extra></extra>'),
                  secondary_y=False)
    fig.update_yaxes(secondary_y=True, showgrid=True)
    fig.update_yaxes(secondary_y=False, showgrid=False, showticklabels=False)

    fig = gen_rolling_mean_graphs(df=df, fig=fig)

    return fig


def gen_rolling_mean_graphs(df: pl.DataFrame, fig: go.Figure) -> go.Figure:
    """
    Gera gráficos de linha com as médias móveis

    :param df: Dados históricos de uma ação
    :param fig: Figure do plotly que armazenará os gráficos
    :return: Retorna uma figure do dash com as médias móveis
    """
    period_list = (15, 25, 72)
    alpha = 0.9
    colors_lines = (f'rgba(255, 130, 0, {alpha})', f'rgba(0, 0, 255, {alpha})', f'rgba(255, 0, 255, {alpha})')
    term_list = ('Short', 'Medium', 'Long')

    rolling_mean_df = calculate_rolling_mean(df)
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


def calculate_rolling_mean(df: pl.DataFrame) -> pl.DataFrame:
    """
    Calcula a média móvel dos dados históricos de uma ação

    :param df: Dados históricos de uma ação
    :return: Retorna um Dataframe com as médias móveis dos dados da ação
    """
    periods_list = (15, 25, 72)
    new_columns = [pl.col('Date')]
    for period in periods_list:
        new_columns.append(pl.col('Close').rolling_mean(window_size=period).alias(f'{period}_days_RM'))
    rolling_mean_df = df.select(new_columns)
    return rolling_mean_df


def format_graph(fig: go.Figure) -> go.Figure:
    """
    Realiza formatação da Figure

    :param fig: Figure 'crua' na qual receberá a formatação adequada
    :return: Retorna uma Figure formatada e pronta para receber os gráficos
    """
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


def get_data_stock(stock_code: str, period: str) -> pl.DataFrame:
    """
    Função responsável por recuperar os dados históricos de uma ação

    :param stock_code: Código da ação (ex: BTC)
    :param period: intervalo de datas dos dados históricos para sua recuperação
    :return: Retorna um Dataframe com os dados históricos
    """
    path_data = PATH_DATA / f'{stock_code}/{stock_code}_{period}.csv'
    df = pl.read_csv(path_data, try_parse_dates=True)
    return df


def format_big_numbers_of_volume(nums: pl.Series) -> typing.List[str]:
    """
    Formata os números referentes ao volume das ações para a inserção posterior no gráfico

    :param nums: Uma Series com os volumes das ações
    :return: Retorna uma lista de números formatados
    """
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
