import alpha_vantage
import time
from alpha_vantage.timeseries import TimeSeries
import pandas as pd
from datetime import datetime,timedelta
class data_pulling:
    def __init__(self):
        self.api_key = 'MNTZV7K3L1FTVL7C'
        self.ts = TimeSeries(key=self.api_key,output_format='Pandas')
        now = datetime.now()
        yest_day = now + timedelta(days=-1)
        yest_day = yest_day.strftime('%Y-%m-%d')
        self.date1 = yest_day

    def calculation(self):
        for name in ['AAPL','ABT','AMD','FB','IBM','INFY','KODK','MSFT','SBUX','TSLA','TTM','TWTR']:
            if name ==  'IBM' or name == "SBUX":
                time.sleep(60)
            data,metadata = self.ts.get_monthly_adjusted(symbol=name)
            data.rename(columns={'5. adjusted close':'adjusted_close','1. open':'open','2. high':'high','3. low':'low','4. close':'close','6. volume':'volume'},inplace=True,errors="raise")
            data['date']=data.index
            data  =  data[data['date']>=self.date1]
            data['date']  = pd.to_datetime(data['date'])
            df1 = pd.read_excel(f"D:\\python_files\\stock\\datasets\\{name}.xlsx")
            df1.sort_values(by=['date'],ascending=[True],inplace=True)
            df1 =df1.append(data)
            df1.sort_values(by=['date'],ascending=[True],inplace=True)
            df1['date'] = df1['date'].dt.date
            df1.to_excel(f"D:\\python_files\\stock\\datasets\\{name}.xlsx",index  = False)
            print(df1)

if __name__ == '__main__':
    a1 = data_pulling()
    a1.calculation()
