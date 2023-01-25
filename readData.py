import matplotlib.pyplot as plt
import pandas as pd

files = ['connectionStatus.csv', 'numberOfBids.csv']


# Read the data from the files
connectionStatus = pd.read_csv(f'data/{files[0]}', sep=',', header=0)
numberOfBids = pd.read_csv(f'data/{files[1]}', sep=',', header=0)


# subtract the first value of the column time to all values
connectionStatus['time'] = connectionStatus['time'] - \
    connectionStatus['time'][0]

# Sum all row on equal first value
connectionStatusGrouped = connectionStatus.groupby(
    connectionStatus.columns[0]).sum()


# add two new columns which are the cumulated value of the two last columns
connectionStatusGrouped['successfullCum'] = connectionStatusGrouped['successfull'].cumsum()
connectionStatusGrouped['successlessCum'] = connectionStatusGrouped['successless'].cumsum()

# Plot the data
fig, axs = plt.subplots(2, 1)

axs[0].plot(connectionStatusGrouped.index,
            connectionStatusGrouped['successfull'], label='sucessfully connected')
axs[0].plot(connectionStatusGrouped.index,
            connectionStatusGrouped['successless'], label='not connected')
axs[0].set_title('Evolution of connection status')
axs[0].legend()
axs[0].set_xlabel('time (s)')
axs[0].set_ylabel('number of successfull / successless connection')

axs[1].plot(connectionStatusGrouped.index,
            connectionStatusGrouped['successfullCum'], label='Number of Ev connected')
axs[1].plot(connectionStatusGrouped.index,
            connectionStatusGrouped['successlessCum'], label='Number of Ev not connected')
axs[1].set_title('Cumulated evolution of connection status')
axs[1].legend()
axs[1].set_xlabel('time (s)')
axs[1].set_ylabel('number of successfull / successless connection')


# Time elapsed

connectionStatusAverage = connectionStatus.groupby(
    connectionStatus.columns[0]).mean()

# plot time elapsed for sucessfull connection
fig, axs = plt.subplots(1, 1)
axs.plot(connectionStatusAverage.index,
         connectionStatusAverage['elapsedTime'], label='time elapsed')
# draw average
axs.axhline(connectionStatus['elapsedTime'].mean(),
            color='r', label='average')
axs.set_title('Average time elapsed every second')
axs.legend()
axs.set_xlabel('time (s)')
axs.set_ylabel('time elapsed (s)')


# Number of bids

# subtract the first value of the column time to all values
numberOfBids['time'] = numberOfBids['time'] - numberOfBids['time'][0]

# Sum all row on equal first value
numberOfBidsGrouped = numberOfBids.groupby(
    numberOfBids.columns[0]).sum()

# plot number of bids
fig, axs = plt.subplots(1, 1)
axs.plot(numberOfBidsGrouped.index,
         numberOfBidsGrouped['nb_bids'], label='number of bids')
axs.set_title('Number of bids every second')
axs.legend()
axs.set_xlabel('time (s)')
axs.set_ylabel('number of bids')


plt.show()
