run = True


def timedFunc():
    import requests
    import json
    import schedule, time
    from main_app.models import Stock


    stock_data_raw_obj = requests.get(f'https://api.polygon.io/v2/aggs/grouped/locale/us/market/stocks/2022-05-13?adjusted=true&apiKey=ISRFyZyx4zGrz0Pzy3veu6ou4pPUYQjU').json()['results']

    for tckr in stock_data_raw_obj:
        currStock = Stock.objects.filter(ticker=(tckr['T']))

        if (len(currStock) == 0 and tckr['v'] >= 10000000):
            currStock = Stock.objects.create(
                ticker=tckr['T'],
                mr_close=tckr['c'],
                mr_volume=tckr['v'],
                industry='na',
                logo='na',
                description='na',
                market_cap=1
            )
        elif (len(currStock) > 0):
            currStock = Stock.objects.get(ticker=(tckr['T']))
            currStock.mr_close = tckr['c']
            currStock.mr_volume = tckr['v']
            print(f'1 - {currStock}')
            currStock[0].save()
        else:
            pass
        print(f'2 - {currStock}')
    

def runFunc():
    import requests
    import json

    import schedule, time

    # from background_task import background

    from main_app.models import Stock



    idx = 0
    schedule.every(20).seconds.do(timedFunc)

    while run:
        schedule.run_pending()
        time.sleep(1)



