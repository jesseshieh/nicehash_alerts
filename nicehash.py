from config import *
import time
import logging  
import logging.handlers
import json, requests

def getProf():
    logger = logging.getLogger(__name__)  

    url = 'https://api.nicehash.com/api'

    params = dict(
            method='stats.provider.ex',
            addr= btcAddress
    )

    resp = requests.get(url=url, params=params)
    stats = json.loads(resp.text)

    totalProf = 0
    for i in stats["result"]["current"]:
            algoProf = float(i["profitability"])
            if "a" in i["data"][0]:
                    # There is activity for this algo.
                    # To get the profitibility per day in BTC, multiply "a" rate by algo profitibility and add to total prof.
                    totalProf = totalProf + algoProf * float(i["data"][0]["a"])
    logger.debug("Current total profitibility in BTC/day is %f." % totalProf)
    return totalProf

def sendAlert(message, alert):
    logger = logging.getLogger(__name__)  
    logger.debug("Sending alert.")

    # Trigger IFTTT event
    report = {}
    report["value1"] = message
    requests.post("https://maker.ifttt.com/trigger/" + alert + "/with/key/" + iftttKey, data=report)

def main():
    LEVEL = logging.DEBUG 
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)  
    logger.setLevel(LEVEL)
    handler = logging.handlers.RotatingFileHandler('debug.log', maxBytes=2000000, backupCount=10)  
    handler.setLevel(LEVEL)  
    handler.setFormatter(formatter)
    logger.addHandler(handler)  

    logger.debug("Starting app")
    while True:
        profitability = getProf()
        if profitability == 0:
            logger.info("The miner is off")
            sendAlert("NiceHash miner is off. Go fix it.","nicehash")
        elif profitability < minProf:
            #currently making less that min profitability setting
            #Check again every 30 seconds for 5 minutes
            sendAlert("NiceHash is running slow.  Current rate is %f BTC/Day" % profitability,"nicehash")
            logger.info("The miner is slow.  Current speed is %f BTC/Day" % profitability)
        else:
            logger.info("The miner is at a normal speed.  Current speed is %f BTC/Day" % profitability)
        time.sleep(30)


if __name__ == "__main__":
    main()

