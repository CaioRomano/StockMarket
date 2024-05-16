from App.libs.libs import os
from pathlib import Path

PATH_DATA = Path(os.path.dirname(os.getcwd())).parent.parent / 'StockData'
LIST_ACEPTABLE_INTERVAL = ['1m', '2m', '5m', '15m', '60m', '90m', '1h', '1d', '5d', '1wk', '1mo', '3mo']
