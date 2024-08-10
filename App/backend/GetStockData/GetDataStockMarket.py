from App.libs.libs import yf, os, pl, typing, date, time
from App.constants import Path, LIST_ACEPTABLE_INTERVAL
from App.constants import PATH_DATA


class GetDataStockMarket:
    """
    Classe responsável por coletar os dados do mercado de ações usando a API do Yahoo Finance
    """

    _CHECK_LIST_INTERVALS: list
    _PATH_DATA: Path

    _stock_name: typing.Union[str, list]
    _stock_data: pl.DataFrame
    _interval: typing.Union[str, list]
    _stock_file: str

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

    def _need_collect_stock_data(self) -> bool:
        """
        Avalia necessidade de requisitar dados das ações, caso comparando a data atual com a última data de modificação
        no formato %Y/%m/%d

        :return: Retorna True, se houver necessidade de requisitar novos dados, e retorna False se não houver.
        """
        try:
            dir_path = self._PATH_DATA / self._stock_name
            stock_file = str(dir_path) + '/' + f'{self._stock_name}_{self._interval}.csv'
            if not os.path.exists(dir_path):
                return True
            else:
                if not os.path.exists(stock_file):
                    return True

            date_today = date.today().strftime('%d/%m/%Y')
            last_modified_data_file = time.strptime(time.ctime(os.path.getmtime(dir_path / stock_file)))
            last_modified_data_file = time.strftime('%d/%m/%Y', last_modified_data_file)

            if last_modified_data_file != date_today:
                return True
            return False

        except Exception as e:
            print(e, '\n\tErro na avaliação!')

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
                raise ValueError(
                    f'Intervalo {interval} inválido!\n\tIntervalos aceitáveis: {self._CHECK_LIST_INTERVALS}'
                )
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

    def collect_data(self) -> pl.DataFrame:
        """
        Recupera os dados da API do Yahoo Finance

        :return: Retorna os dados da API no formato dataframe do pandas
        """
        try:
            stock_ticker = yf.Ticker(self._stock_name)
            period = self._determine_period()
            data_pd = stock_ticker.history(period=period, interval=self._interval)
            data_pd.reset_index(inplace=True)
            self._stock_data = pl.from_pandas(data_pd)
            self._stock_data = self._stock_data.rename({'Datetime': 'Date'})
        except pl.exceptions.SchemaFieldNotFoundError:
            pass
        except Exception as e:
            print(e, '\n\tErro ao coletar os dados da API do Yahoo Finance!')
        else:
            return self._stock_data

    def _create_dir_stock_data(self) -> Path:
        """
        Cria a pasta onde os dados serão inseridos

        :return: Retorna o caminho de armazenamento dos dados
        """
        try:
            dir_path = self._PATH_DATA / f"{self._stock_name}"
            if not os.path.exists(dir_path):
                os.makedirs(dir_path, exist_ok=True)
            return dir_path
        except FileExistsError as e:
            print(e, '\n\tErro na criação do caminho de armazenamento dos dados!')

    def _exists_new_stock_data(self, stock_file: str) -> bool:
        """
        Compara os dados novos com os já existentes, sem precisar criar um novo arquivo usando todos os dados.

        :param stock_file: Nome do arquivo csv junto com o caminho do mesmo arquivo
        :return: Retorna o True se existir novos dados, caso contrário, retorna False
        """
        try:
            df = pl.read_csv(stock_file)
            df = df.rename({'Datetime': 'Date'})
            max_date = df.select(pl.max('Date')).item()
            news_data = self._stock_data.filter(pl.col('index') > max_date)
            if not len(news_data) == 0:
                self._update_stock_data(news_data=news_data, stock_file=stock_file)
                return True
            else:
                return False
        except pl.exceptions.SchemaFieldNotFoundError:
            pass
        except Exception as e:
            print(e, '\n\tErro na comparação de dados!')

    def _update_stock_data(self, news_data: pl.DataFrame, stock_file: str) -> None:
        """
        Atualiza os dados das ações com os valores das novas datas

        :param news_data: Novos dados das ações já armazenadas
        :param stock_file: Nome do arquivo csv junto com o caminho do mesmo arquivo
        """
        new_df = pl.concat([self._stock_data, news_data], how='vertical')
        new_df.write_csv(file=stock_file)

    def store_data(self) -> None:
        """
        Armazena os dados numa pasta específica
        """
        try:
            dir_path = self._create_dir_stock_data()
            stock_file = str(dir_path) + '/' + f'{self._stock_name}_{self._interval}.csv'

            if os.path.exists(stock_file):
                response = self._exists_new_stock_data(stock_file=stock_file)
                if not response:
                    self._stock_data.write_csv(file=stock_file)
            else:
                self._stock_data.write_csv(file=stock_file)
        except FileExistsError:
            print('Arquivo já existe!')

    def get_stock_data(self) -> pl.DataFrame:
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
            for interval in list_intervals:
                self._interval = interval
                if isinstance(list_stock_names, list):
                    for stock in list_stock_names:
                        self._stock_name = stock
                        need_collect_data = self._need_collect_stock_data()
                        if need_collect_data:
                            self.collect_data()
                            self.store_data()
                else:
                    need_collect_data = self._need_collect_stock_data()
                    if need_collect_data:
                        self.collect_data()
                        self.store_data()
        else:
            if isinstance(self._stock_name, list):
                stock_name_list = self._stock_name
                for stock in stock_name_list:
                    self._stock_name = stock
                    need_collect_data = self._need_collect_stock_data()
                    if need_collect_data:
                        self.collect_data()
                        self.store_data()
            else:
                need_collect_data = self._need_collect_stock_data()
                if need_collect_data:
                    self.collect_data()
                    self.store_data()


if __name__ == '__main__':
    getdata = GetDataStockMarket(stock_name=['AAPL'], interval='all')
    getdata.run()
