Adapted from https://gist.github.com/randyklein/9602cb01e1d9a58b52c9b4e162eef76c

Queries the nicehash API every 30 seconds to check profitability. If profitability is 0 or
falls below a configurable threshold, trigger an IFTTT webhook. IFTTT webhook can be 
configured however you like.

The the script uses the IFTTT Maker/Webhook channel to do the alerting.  To configure and run:

1. Configure an IFTTT Maker/Webhook applet. Try https://platform.ifttt.com/maker/
   Set the trigger as a webhook with event name "nicehash".
2. Setup the config.py settings. Add your BTC address and IFTTT key. See an example at config.py.example.
3. Run `python nicehash.py`
