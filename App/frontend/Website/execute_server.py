from App.frontend.Website.PageHome import PageHome
from App.frontend.Website.layout.layout import layout


def execute_server() -> None:
    """
    Executa o server
    """
    page_home = PageHome(layout=layout())
    page_home.run()
