import requests
import pandas as pd
import time

questions = []
df = pd.read_csv('qa.csv')
try:
    for i in range(100000):
        try:
            r = requests.get('https://isafeevent.moe.edu.tw/api/questions/C', headers={'UserToken': 'd896sf7as89d6f74896'})
        except requests.exceptions.RequestException as e:
            print(e)
        print(r)
        if r.status_code == 200:
            df = pd.concat([df, pd.json_normalize(r.json()['questions'])])
            df = df[~df.examId.duplicated()]
        time.sleep(5)
except KeyboardInterrupt as e:
    print(e)
df.sort_values('examId').to_csv('./qa.csv', index=False)
