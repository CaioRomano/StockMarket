from App.frontend.Website.PageHome import PageHome
from App.frontend.Website.layout.layout import layout


def execute_server() -> None:
    page_home = PageHome(layout=layout())
    page_home.run()


if __name__ == '__main__':
    execute_server()
