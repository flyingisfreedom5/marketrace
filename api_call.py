run = True
from datetime import date
from datetime import timedelta, tzinfo
import pytz
import threading

from datetime import datetime

import pytz

def timedFunc():
    import requests
    import json
    import schedule, time
    from main_app.models import Stock

    
    tz_IN = pytz.timezone('US/Pacific') 

    yesterday = datetime.now(tz_IN) - timedelta(days = 1)
    y = yesterday.strftime("%Y")
    m = yesterday.strftime("%m")
    d = yesterday.strftime("%d")
    ydayDate = f'{y}-{m}-{d}'
    
    stock_data_raw_obj = requests.get(f'https://api.polygon.io/v2/aggs/grouped/locale/us/market/stocks/{ydayDate}?adjusted=true&apiKey=ISRFyZyx4zGrz0Pzy3veu6ou4pPUYQjU').json()['results']


    for tckr in stock_data_raw_obj:
        currStock = Stock.objects.filter(ticker=(tckr['T']))

        if (len(currStock) == 0 and tckr['v'] >= 10000000):
            currStock = Stock.objects.create(
                ticker=tckr['T'],
                mr_close=tckr['c'],
                mr_volume=tckr['v'],
                mr_vol_weighted=tckr['vw'],
                industry='na',
                logo='na',
                description='na',
                market_cap=1
            )
        elif (len(currStock) > 0):
            currStock = Stock.objects.get(ticker=(tckr['T']))
            currStock.mr_close = tckr['c']
            currStock.mr_volume = tckr['v']
            currStock.mr_vol_weighted = tckr['vw']
            currStock.save()
        else:
            pass
        print(currStock)
    

def runFunc():
    import requests
    import json

    import schedule, time

    # from background_task import background

    from main_app.models import Stock
# <<<<<<< HEAD
    timedFunc()
    print('test')
    schedule.every(20).seconds.do(timedFunc)
    
    # while run:
    #     time.sleep(1)

    def run_continuously(interval=1):
        cease_continuous_run = threading.Event()

        class ScheduleThread(threading.Thread):
            @classmethod
            def run(cls):
                while not cease_continuous_run.is_set():
                    schedule.run_pending()
                    time.sleep(interval)

        continuous_thread = ScheduleThread()
        continuous_thread.start()
        return cease_continuous_run

    run_continuously()



