%matplotlib notebook

import matplotlib.pyplot as plt
import mplleaflet
import pandas as pd
import numpy as np
from matplotlib.ticker import FuncFormatter

def extract_day(row):
    return row.Date.replace(year=2016)

def leaflet_plot_stations(binsize, hashid):

    df = pd.read_csv('data/C2A2_data/BinnedCsvs_d{}/{}.csv'.format(binsize, hashid), parse_dates=['Date'])
    df['Day'] = df.apply(extract_day, axis=1)
    df.set_index('Day')

    first_df = df.where((df['Date'] >= pd.Timestamp('2005-01-01 00:00:00Z')) & (df['Date'] < pd.Timestamp('2015-01-01 00:00:00Z')))
    df_2015 = df[df['Date'] >= pd.Timestamp('2015-01-01 00:00:00Z')]


    min_df = first_df.where(first_df['Element'] == 'TMIN').groupby('Day').min()
    max_df = first_df.where(first_df['Element'] == 'TMAX').groupby('Day').max()

    min_2015 = df_2015[df_2015['Element'] == 'TMIN']
    max_2015 = df_2015[df_2015['Element'] == 'TMAX']

    min_2015 = min_2015.groupby('Day').min().join(min_df, rsuffix='_min', how='inner').dropna()
    max_2015 = max_2015.groupby('Day').max().join(max_df, rsuffix='_max', how='inner').dropna()

    broken_min = min_2015[min_2015['Data_Value'] < min_2015['Data_Value_min']].reset_index()[['Day', 'Data_Value']].set_index('Day')
    broken_max = max_2015[max_2015['Data_Value'] > max_2015['Data_Value_max']].reset_index()[['Day', 'Data_Value']].set_index('Day')

    broken_min['Data_Value'] /= 10.0
    broken_max['Data_Value'] /= 10.0

    broken_records = pd.concat([broken_min, broken_max])

    min_df['Data_Value'] /= 10.0
    max_df['Data_Value'] /= 10.0

    plt.figure()
    plt.plot(min_df['Data_Value'], label='Record low', color='blue')
    plt.plot(max_df['Data_Value'], label='Record high', color='red')

    plt.xlabel('Day', alpha=0.8)
    plt.ylabel('Temperature in °C', alpha=0.8)
    plt.title('Record breaking temperatures in 2015, around Paris (Fr)')

    plt.scatter(broken_records.index, broken_records['Data_Value'], s = 15, color = 'black', label = 'broken record')

    ax = plt.gca()
    ax.fill_between(min_df.index, min_df['Data_Value'], max_df['Data_Value'], facecolor='grey', alpha=0.15, interpolate=True)
    plt.legend()

    dates = np.array(['2016-01-01', '2016-02-01', '2016-03-01','2016-04-01', '2016-05-01', '2016-06-01', '2016-07-01', '2016-08-01', '2016-09-01','2016-10-01', '2016-11-01', '2016-12-01'], dtype='datetime64')
    plt.xticks(dates, ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], rotation=20, alpha=0.8)

leaflet_plot_stations(100,'1b10750994e98f9fe5828966bf365e6f39293ca7b239de2bfadfaa56')
