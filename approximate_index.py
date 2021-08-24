#Name: Rob Bulman
#Submission Date: July 2nd 

import numpy # to run pandas
import pandas as pd # to open csv file and perform data analysis
import sys # parse passed inputs

n = int(sys.argv[1]) # number of symbols
index_approx = str(sys.argv[2])
df = pd.read_csv(str(sys.argv[3])) # takes input of csv file, converts input to string and turns it into a dataframe

output = str(sys.argv[4])

df_2 = df.pivot(index = 'Date', columns = 'Symbol', values = 'Close') # pivot table by ticker symbol

pct_df = df_2.pct_change() # show percentage change day by day

pct_df.dropna(inplace = True) # drop null value

corr = pct_df.corr() # correlation table accross all symbols

corr = corr[index_approx] # correlation table of index to constituants

sorted_corr = corr.sort_values(ascending = False) # reorder so top correlation is on top

sorted_corr.drop([index_approx], inplace = True) # since index correlates to index 100%, drop that

top_corrdf = sorted_corr.head(n = n) # find top "n" number of correlations

lst = []
lst.append(index_approx)
for index, value in top_corrdf.items():
    lst.append(index) # create list of top 4 symbol names and index name for weighted values calculation


eval_df = df_2.reset_index(drop = True) # reset so that index of data frame is by number, not date

eval_df = eval_df[lst] # pull from pivoted dataframe, top symbols only

eval_df = eval_df.iloc[0] # find first entries of all tickers

symbol_lst = []
weight_lst = []
for key, value in eval_df.items(): # this loop is to calculate the weights of each ticker
    try:
        weight = round(total / value / n)
        symbol_lst.append(key)
        weight_lst.append(weight)
    except:    
        if key == index_approx:
            total = value

df = pd.DataFrame({'symbol': symbol_lst, 'weight': weight_lst}) #create data frame to write to csv file in next 2 lines of code


compression_opts = dict(method='zip', archive_name=output)  

df.to_csv('out.zip', index=False, compression=compression_opts)

    