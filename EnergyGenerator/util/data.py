import pandas as pd
import time
import os


def numberOfBidsAtAuction(bids):
    currentTime = int(time.time())
    # create file if not exists, name=data/numberOfBids.csv
    if not os.path.exists('data/numberOfBids.csv'):
        # using pandas dataframe
        df = pd.DataFrame(columns=['time', 'nb_bids'])
        df.to_csv('data/numberOfBids.csv', index=False)
    # read file
    df = pd.read_csv('data/numberOfBids.csv')
    # add new line
    df = pd.concat([df, pd.DataFrame(
        {'time': [currentTime], 'nb_bids': [len(bids)]})], ignore_index=True)
    # save file
    df.to_csv('data/numberOfBids.csv', index=False)
