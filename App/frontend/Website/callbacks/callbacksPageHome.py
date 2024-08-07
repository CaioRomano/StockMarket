from App.libs.libs import Input, Output, State, html, go, dcc, ctx, dbc, make_subplots
from App.frontend.Website.callbacks.helpers import get_list_stock_names, format_graph, get_data_stock
from App.backend.GetStockData.execute import execute_get_price_stock, execute_get_data_stock
from App.constants import LIST_ACEPTABLE_INTERVAL


def callbacks(app) -> None:
    @app.callback(
        Output(component_id='dropdown-menu-stocks', component_property='options'),
        Input(component_id='input-div', component_property='children'),
        Input(component_id='interval-component', component_property='n_intervals')
    )
    def get_stock_names(_, __):
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
    def set_stock_name(sel_stock, cur_stock):
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
    def update_prices(_, cur_stock):
        if cur_stock:
            info_stock = execute_get_price_stock(stock_code=cur_stock)
            price, change, pct_change = info_stock
            green, red = '#90EE90', '#FF7F7F'
            change_color = green if '+' in change else red
            pct_change_color = green if '+' in pct_change else red
            change_text = html.H5(f'{change}', style={'color': change_color})
            pct_change_text = html.H5(f'{pct_change}', style={'color': pct_change_color})

            return price, change_text, pct_change_text
        else:
            return [''] * 3

    @app.callback(
        Output(component_id='output-graph', component_property='children'),
        State(component_id='stock-name', component_property='children'),
        [Input(component_id=period, component_property='n_clicks') for period in LIST_ACEPTABLE_INTERVAL]
    )
    def graph_candlestick(cur_stock, *_):
        # Quero mostrar os

        # fig = go.Figure(layout=go.Layout(
        #     paper_bgcolor='rgba(0,0,0,0)',
        #     plot_bgcolor='rgba(0,0,0,0)')
        # )
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        if cur_stock:
            triggered = ctx.triggered
            if triggered:
                period = triggered[0]['prop_id'].split('.')[0]
                if any(char.isdigit() for char in period):
                    df = get_data_stock(cur_stock=cur_stock, period=period)
                    fig.add_trace(go.Candlestick(
                        x=df['Date'],
                        open=df['Open'],
                        high=df['High'],
                        low=df['Low'],
                        close=df['Close']
                    ))
                    fig = format_graph(fig)
        return dcc.Graph(figure=fig)

    @app.callback(
        Output(component_id='periods-stock', component_property='options'),
        Input(component_id='periods-stock', component_property='id')
    )
    def create_radio_items(_):
        options_periods = []
        for period in LIST_ACEPTABLE_INTERVAL:
            options_periods.append({'label': period, 'value': period})
        return options_periods

    @app.callback(
        Output(component_id='button-group', component_property='children'),
        Input(component_id='button-group', component_property='id')
    )
    def create_period_buttons(_):
        button_group = []
        for period in LIST_ACEPTABLE_INTERVAL:
            button_group.append(
                dbc.Button([period], color='sucess', id=period)
            )
        return button_group

    @app.callback(
        Input(component_id='get-stock', component_property='value'),
        Input(component_id='add-stock', component_property='n_clicks')
    )
    def get_stock(stock_code, n_clicks):
        if n_clicks is not None:
            execute_get_data_stock(stock_code=stock_code)
