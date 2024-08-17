from App.libs.libs import dash, typing, dbc
from App.frontend.Website.callbacks.callbacksPageHome import callbacks


class PageHome:
    """
    Classe responsável por carregar a página web
    """
    _app: dash.Dash
    _layout: list

    def __init__(self, layout: typing.Any) -> None:
        """
        Método construtor da classe PageHome

        :param layout: Layout da página web
        """
        self._layout = layout
    
    def _build_app(self) -> None:
        """
        Método responsável por criar o app Dash
        """
        self._app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.DARKLY], meta_tags=[
            {"name": "viewport", "content": "width=device-width, initial-scale=1"},
        ])

    def run(self, debug: bool = True) -> None:
        """
        Executa o servidor

        :param debug: parâmetro para debuggar o código e encontrar notificações de erros
        """
        self._build_app()
        self._app.css.config.serve_locally = True
        self._app.scripts.config.serve_locally = True
        self._app.layout = self._layout
        callbacks(self._app)
        self._app.run(debug=debug)
