import pandas as pd
import os
import time


# file to described the function used to save the data from the client at certain moments


def connectionStatus(status, start_time):
    ''' 
    if the status is True then the connection was successfull, if it is False there was no connection
    the first column is the current time, the second the number of successfull connection, the third the number of successless connection
    take the current time from the first column (or create it) and increment the successfull connections or the successless connections
    '''
    # get the current time
    currentTime = int(time.time())
    # create a new file (increment the name if already exists) with panda
    data = pd.DataFrame(
        columns=['time', 'successfull', 'successless', 'elapsedTime'])
    # if the file already exists
    if os.path.exists('data/connectionStatus.csv'):
        # read the file
        data = pd.read_csv('data/connectionStatus.csv')
        # add a new line with the current time and increment the successfull or successless connections
        if status:
            data = pd.concat([data,
                              pd.DataFrame({'time': [currentTime], 'successfull': [1], 'successless': [0], 'elapsedTime': int(currentTime - start_time)})], ignore_index=True)
        else:
            data = pd.concat([data,
                              pd.DataFrame({'time': [currentTime], 'successfull': [0], 'successless': [1], 'elapsedTime': int(currentTime - start_time)})], ignore_index=True)
    # if the file does not exist
    else:
        # add a new line with the current time and increment the successfull or successless connections
        if status:
            data = pd.concat([data,
                              pd.DataFrame({'time': [currentTime], 'successfull': [1], 'successless': [0], 'elapsedTime': int(currentTime - start_time)})], ignore_index=True)
        else:
            data = pd.concat([data,
                              pd.DataFrame({'time': [currentTime], 'successfull': [0], 'successless': [1], 'elapsedTime': int(currentTime - start_time)})], ignore_index=True)
    # save the file
    data.to_csv('data/connectionStatus.csv', index=False)
