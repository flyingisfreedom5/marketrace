run = False


def timedFunc():
    import requests
    import json
    import schedule, time
    from main_app.models import Stock


    stock_data_raw_obj = requests.get(f'https://api.polygon.io/v2/aggs/grouped/locale/us/market/stocks/2022-05-13?adjusted=true&apiKey=ISRFyZyx4zGrz0Pzy3veu6ou4pPUYQjU').json()['results']

    for tckr in stock_data_raw_obj:
        currStock = Stock.objects.filter(ticker=(tckr['T']))

        if (len(currStock) == 0):
            currStock = Stock.objects.create(
                ticker=tckr['T'],
                mr_close=tckr['c'],
                mr_volume=tckr['v'],
                industry='na',
                logo='na',
                description='na',
                market_cap=1
            )
        else:
            currStock.mr_close = tckr['c']
            currStock.mr_volume = tckr['v']
            currStock.save()
        print(currStock)
    



