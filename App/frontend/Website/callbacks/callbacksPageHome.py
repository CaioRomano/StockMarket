from App.libs.libs import Input, Output, State, html, dcc, ctx, make_subplots
from App.frontend.Website.callbacks.helpers import *
from App.backend.GetStockData.execute import execute_get_price_stock, execute_get_data_stock
from App.constants import LIST_ACEPTABLE_INTERVAL


def callbacks(app: dash.Dash) -> None:
    """
    Função que agraga todos os callbacks da página dash
    :param app: App responsável por rodar o site web
    """
    @app.callback(
        Output(component_id='dropdown-menu-stocks', component_property='options'),
        Input(component_id='input-div', component_property='children'),
        Input(component_id='interval-component', component_property='n_intervals')
    )
    def get_stock_names(_, __) -> list:
        """
        Callback responsável por recuperar o código das ações já salvas

        :return: Retorna a lista das ações salvas
        """
        return get_list_stock_names()

    # @app.callback(
    #     Output(component_id='output-div', component_property='children'),
    #     Input(component_id='dropdown-menu-stocks', component_property='value')
    # )
    # def output_demo(_):
    #     return _

    @app.callback(
        Output(component_id='stock-name', component_property='children'),
        Input(component_id='dropdown-menu-stocks', component_property='value'),
        State(component_id='stock-name', component_property='children')
    )
    def set_stock_name(sel_stock: str, cur_stock: str) -> str:
        """
        Callback responsável por manter o código da ação no elemento html até selecionar outra ação pelo elemento dropdown

        :param sel_stock: Referencia a ação selecionada
        :param cur_stock: Referencia a última ação selecionada
        :return: retorna o código da ação
        """
        if sel_stock:
            return sel_stock
        return cur_stock

    @app.callback(
        Output(component_id='price-stock', component_property='children'),
        Output(component_id='change-price-stock', component_property='children'),
        Output(component_id='pct-change-price-stock', component_property='children'),
        Input(component_id='interval-component', component_property='n_intervals'),
        State(component_id='stock-name', component_property='children')
    )
    def update_prices(_, cur_stock: str) -> list:
        """
        Callback responsável por mostrar as informações referentes ao preço da ação
        :param cur_stock: Referencia a última ação selecionada
        :return: Retorna as informações da ação
        """
        if cur_stock:
            info_stock = execute_get_price_stock(stock_code=cur_stock)
            price, change, pct_change = info_stock
            green, red = '#90EE90', '#FF7F7F'
            change_color = green if '+' in change else red
            pct_change_color = green if '+' in pct_change else red
            change_text = html.H5(f'{change}', style={'color': change_color})
            pct_change_text = html.H5(f'{pct_change}', style={'color': pct_change_color})

            return [price, change_text, pct_change_text]
        else:
            return [''] * 3

    @app.callback(
        Output(component_id='output-graph', component_property='children'),
        State(component_id='stock-name', component_property='children'),
        Input(component_id='graph-type', component_property='value'),
        [Input(component_id=period, component_property='n_clicks') for period in LIST_ACEPTABLE_INTERVAL]
    )
    def generate_graphs(cur_stock: str, graph_type: str, *_) -> dcc.Loading:
        """
        Callback responsável por gerar e mostrar o grafico dos dados históricos de uma ação ao usuário

        :param cur_stock: Referencia a última ação selecionada
        :param graph_type: valor que dirá qual gráfico será mostrado ao usuário
        :return: Retorna o gráfico com um efeito de loading
        """
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig = format_graph(fig)
        if cur_stock:
            triggered = ctx.triggered
            if triggered:
                period = triggered[0]['prop_id'].split('.')[0]
                if any(char.isdigit() for char in period):
                    df = get_data_stock(cur_stock=cur_stock, period=period)
                    fig = gen_graph(df=df, fig=fig, graph_type=graph_type)

        return dcc.Loading(dcc.Graph(figure=fig))

    @app.callback(
        Input(component_id='get-stock', component_property='value'),
        Input(component_id='add-stock', component_property='n_clicks')
    )
    def get_stock(stock_code: str, n_clicks: int) -> None:
        """
        Callback responsável por capturar os dados históricos de uma ação através de uma chamada API

        :param stock_code: Código da ação (ex: BTC)
        :param n_clicks: necessário para identificar que o botão foi clicado pelo usuário
        """
        if n_clicks is not None:
            execute_get_data_stock(stock_code=stock_code)
