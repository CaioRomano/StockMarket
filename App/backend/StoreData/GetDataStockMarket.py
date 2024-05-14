from App.libs.libs import yf, os, DataFrame, pd, typing
from App.backend.StoreData.constants import PATH_DATA, Path, LIST_ACEPTABLE_INTERVAL


class GetDataStockMarket:
    """
    Classe responsável por coletar os dados do mercado de ações usando a API do Yahoo Finance
    """

    _CHECK_LIST_INTERVALS: list
    _PATH_DATA: Path

    _stock_name: typing.Union[str, list]
    _stock_data: DataFrame
    _interval: typing.Union[str, list]
    _name_csv: str

    def __init__(self, stock_name: typing.Union[str, list], interval: typing.Union[str, list] = '1d') -> None:
        """
        Método construtor da classe

        :param stock_name: Nome da ação a ser coletada
        :param interval: Intervalo dos dados a serem obtidos
        """
        self._PATH_DATA = PATH_DATA
        self._CHECK_LIST_INTERVALS = LIST_ACEPTABLE_INTERVAL
        self._stock_name = stock_name
        self._interval = self._check_intervals(interval) if interval != 'all' else LIST_ACEPTABLE_INTERVAL

    def _check_intervals(self, interval: typing.Union[str, list]) -> typing.Union[str, list]:
        """
        Realiza uma checagem de validade dos valores de intervalos recebidos

        :param interval: Intervalo dos dados das ações
        :return: retorna os intervalos das ações
        """
        if isinstance(interval, list):
            for i in interval:
                if i in self._CHECK_LIST_INTERVALS:
                    pass
                else:
                    raise ValueError(f'Intervalo {i} inválido!\n\tIntervalos aceitáveis: {self._CHECK_LIST_INTERVALS}')
        elif isinstance(interval, str):
            if not (interval in self._CHECK_LIST_INTERVALS):
                raise ValueError(f'Intervalo {interval} inválido!\n\tIntervalos aceitáveis: {self._CHECK_LIST_INTERVALS}')
        return interval

    def _determine_period(self) -> str:
        """
        Determina o período adequado para um dado intervalo

        :return: Retorna o período adequado para um dado intervalo
        """
        period = 'max'
        if self._interval == '1m':
            period = '7d'
        elif self._interval in ['2m', '5m', '15m', '90m']:
            period = '60d'
        elif self._interval in ['60m', '1h']:
            period = '730d'
        return period

    def collect_data(self) -> DataFrame:
        """
        Recupera os dados da API do Yahoo Finance

        :return: Retorna os dados da API no formato dataframe do pandas
        """
        try:
            stock_ticker = yf.Ticker(self._stock_name)
            period = self._determine_period()
            self._stock_data = stock_ticker.history(period=period, interval=self._interval)
            # print(period, self._stock_data.columns, self._stock_data.index)
        except Exception as e:
            print(e)
        else:
            return self._stock_data

    def _create_dir_stock_data(self) -> Path:
        """
        Cria a pasta onde os dados serão inseridos

        :return: Retorna o caminho de armazenamento dos dados
        """
        try:
            path = self._PATH_DATA / f"{self._stock_name}"
            if not os.path.exists(path):
                os.mkdir(path)
            return path
        except FileExistsError as e:
            print(e)

    def _exists_new_stock_data(self, name_csv: str) -> bool:
        """
        Compara os dados novos com os já existentes, sem precisar criar um novo arquivo usando todos os dados.

        :param name_csv: Nome do arquivo csv junto com o caminho do mesmo arquivo
        :return: Retorna o True se existir novos dados, caso contrário, retorna False
        """
        try:
            df = pd.read_csv(name_csv)
            df = df.rename(columns={'Datetime': 'Date'}, errors='ignore')
            df['Date'] = pd.to_datetime(df['Date'], utc=True)
            news_data = self._stock_data[self._stock_data.index > df['Date'].max()]
            if not len(news_data) == 0:
                self._update_stock_data(news_data=news_data, name_csv=name_csv)
                return True
            else:
                return False
        except ValueError as e:
            print('bebe, algo deu errado')
            print(e)

    def _update_stock_data(self, news_data: DataFrame, name_csv: str) -> None:
        """
        Atualiza os dados das ações com os valores das novas datas

        :param news_data: Novos dados das ações já armazenadas
        :param name_csv: Nome do arquivo csv junto com o caminho do mesmo arquivo
        """
        new_df = pd.concat([self._stock_data, news_data], ignore_index=False)
        new_df.to_csv(name_csv)

    def store_data(self) -> None:
        """
        Armazena os dados numa pasta específica
        """
        try:
            path = self._create_dir_stock_data()
            name_csv = str(path) + '/' + f'{self._stock_name}_{self._interval}.csv'

            if os.path.exists(name_csv):
                response = self._exists_new_stock_data(name_csv=name_csv)
                if not response:
                    self._stock_data.to_csv(name_csv)
            else:
                self._stock_data.to_csv(name_csv)
        except FileExistsError:
            print('Arquivo já existe!')

    def get_stock_data(self) -> DataFrame:
        """
        Retorna o valor dos dados coletados

        :return: Dados coletados
        """
        return self._stock_data

    def run(self) -> None:
        """
        Executa as tarefas de coleta e armazenamento de dados
        """
        list_intervals = self._interval
        list_stock_names = self._stock_name
        if isinstance(list_intervals, list):
            print('é lista de intervalos')
            for interval in list_intervals:
                self._interval = interval
                if isinstance(list_stock_names, list):
                    print('é lista\n')
                    for stock in list_stock_names:
                        self._stock_name = stock
                        self.collect_data()
                        self.store_data()
                else:
                    print('é string\n')
                    self.collect_data()
                    self.store_data()
        else:
            if isinstance(self._stock_name, list):
                print('é lista\n')
                stock_name_list = self._stock_name
                for stock in stock_name_list:
                    self._stock_name = stock
                    self.collect_data()
                    self.store_data()
            else:
                print('é string\n')
                self.collect_data()
                self.store_data()


if __name__ == '__main__':
    """
    Deve permitir que visualize primeiro o dia para não ter de fazer uma requisição atoa.
    """
    getdata = GetDataStockMarket(stock_name=['AAPL', 'PETR4.SA', 'TSLA'], interval='all')
    # getdata.collect_data()
    # getdata.store_data()
    getdata.run()
