from App.libs.libs import Path, os


PATH_DATA = Path(os.path.dirname(__file__)).parent / 'StockData'
PATH_MODEL = Path(os.path.dirname(__file__)).parent / 'SavedModel'
LIST_ACEPTABLE_INTERVAL = ['1m', '2m', '5m', '15m', '60m', '90m', '1h', '1d', '5d', '1wk', '1mo', '3mo']
