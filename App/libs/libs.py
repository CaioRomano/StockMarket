
# Arquivo responsável por armazenar as bibliotecas sendo usadas pelo programa


# Conexão de APIs e internet
import yfinance as yf
import requests
from bs4 import BeautifulSoup
from urllib3 import PoolManager, Timeout

# Manipulação de tabelas
import polars as pl

# Documentação e atribuição de variáveis
import typing
from pathlib import Path

# Modelagem Front-End
import dash
from dash import dcc, callback, Input, Output, State, html, callback_context as ctx
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Uso diverso
import os
from datetime import date
import time
import re
import numpy as np
from abc import ABC, abstractmethod

# Machine Learning
