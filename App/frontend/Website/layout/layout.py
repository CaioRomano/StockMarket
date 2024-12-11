from App.libs.libs import dbc, dcc, html
from App.constants import LIST_ACEPTABLE_INTERVAL


def layout():
    """
    Função responsável por criar o layout da página web

    :return: Retorna o layout da página
    """
    design = dbc.Tabs([
        dbc.Tab([
            html.Div(id='output-div'),
            html.Div(id='input-div'),
            html.Div([
                dcc.Interval(
                    id='interval-component',
                    interval=2 * 1000,
                    n_intervals=0
                )]),
            html.Div(children=[
                dbc.Row(children=[
                    dbc.Col(children=[
                        dbc.Card(
                            dbc.CardBody([
                                dbc.Row(children=[
                                    dbc.Col(children=[
                                        dcc.Dropdown(id='dropdown-menu-stocks', searchable=False, style={
                                            "background-color": "rgb(48, 48, 48)",
                                            "width": "75%",
                                            'margin-right': '1%'
                                        })
                                    ], width=6),
                                    dbc.Col(children=[
                                        dcc.Input(placeholder='Stock Name (ex: TSLA)', id='get-stock',
                                                  style={
                                                      'background-color': 'rgb(255, 255, 255, .35)',
                                                      'color': 'rgb(255, 255, 255, .7)',
                                                      'width': '55%',
                                                      'border-radius': '5px',
                                                      'border': '2px',
                                                      'display': 'inline-block',
                                                      'padding-left': '10px',
                                                      'padding-top': '5px',
                                                      'padding-bottom': '5px',
                                                      'padding-right': '5px'
                                                  }),
                                        dbc.Button('Add', id='add-stock', style={
                                            'margin-left': '2%'
                                        })
                                    ], width=6)
                                ]),
                                dbc.Row(children=[
                                    dbc.Alert(
                                        children=[''],
                                        color='success',
                                        dismissable=True,
                                        duration=5 * 1000,
                                        is_open=False,
                                        id='alert-completed-download', style={'width': '25%', 'margin-top': '20px'})
                                ])
                            ]), style={
                                'display': 'inline-block',
                                'margin-top': '2%',
                                'margin-left': '1.5%',
                                "font-family": "sans-serif",
                                "font-size": "large",
                                'width': '85%'
                            }, id='first-card')
                    ], width=8)
                ], id='row-1'),
                dbc.Row(children=[
                    dbc.Col(children=[
                        dbc.Card([
                            dbc.CardHeader(children=[
                                html.H3(id='stock-name'),
                                html.Hr(),
                                html.Div(children=[
                                    html.H3(id='price-stock', style={
                                        'margin-left': '1%'}),
                                    html.H5(id='change-price-stock', style={
                                        'margin-left': '1%'}),
                                    html.H5(id='pct-change-price-stock', style={
                                        'margin-left': '1%'}),
                                ], style={'display': 'flex'})
                            ]),
                            dbc.CardBody(children=[
                                html.Div(children=[
                                    dbc.ButtonGroup(children=[
                                        dbc.Button(
                                            [period], color='sucess', id=period) for period in LIST_ACEPTABLE_INTERVAL],
                                        id='button-group',
                                        size='me-1',
                                        style={'display': 'inline-block'}),
                                ], className='radio-group', style={'display': 'inline-block'}),
                                html.Div(children=[
                                    dcc.Dropdown(value='Candlestick', options=['Candlestick', 'Line'], id='graph-type',
                                                 searchable=False, clearable=False, style={
                                            'margin-left': '25px',
                                            'backgroundColor': 'transparent',
                                            'color': 'white',
                                            'width': '200px'
                                        })
                                ], style={
                                    'display': 'inline-block',
                                    'border-left': '1px solid #ffffff',
                                    'margin-left': '25px',
                                }),
                                dcc.Loading(html.Div(id='output-graph'))
                            ]),
                        ], color='dark', inverse=True, style={
                            'margin-right': '1.5%', 'margin-left': '1.75%', 'margin-top': '1.5%'})
                    ], style={'border-right': '1px solid #ffffff'}),
                ])
            ], id='main-div'),
        ], id='first-tab', label='Dashboard'),
        dbc.Tab([
            dbc.Card(
                dbc.CardBody([
                    dbc.Button(['Shutdown Server'], color='danger', id='shutdown-btn', outline=True),
                    dbc.Alert(
                        children=['Server is offline!\nYou can close the page!'],
                        color='success',
                        dismissable=True,
                        duration=5 * 1000,
                        is_open=False,
                        id='alert-shutdown-server', style={'width': '25%', 'margin-top': '20px'})
                ])
            )
        ], id='shutdown-server', label='shutdown server')
    ])
    return design
