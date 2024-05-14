from App.libs.libs import requests, ray, BeautifulSoup


# @ray.remote(num_cpus=6)
class StoreDataByRequests:
    def __init__(self):
        self.stockname='AAPL'
        self.data = None
        self.user_agent = {'user_agent': None}

    def get_user_agent(self):
        url = 'https://finance.yahoo.com/quote/BTC-USD/history'
        user_agent = {'User-agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=user_agent)
        soup = BeautifulSoup(response.content, 'html.parser')
        fin_streamer = soup.find('fin-streamer', class_='livePrice').get('data-value')
        # print(fin_streamer.get('data-value'))
        # print(response.status_code)
        # print(response.content)
        return fin_streamer


if __name__ == '__main__':
    # sd = StoreDataByRequests.remote()
    # data = ray.get(sd.get_user_agent.remote())
    sd = StoreDataByRequests()
    data = sd.get_user_agent()
    print(data)