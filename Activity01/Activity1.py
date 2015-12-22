# import pandas and numpy libraries
import pandas as pd
import numpy as np

# read in text file, which is tab delimited, and set global unique indentifier as the index column
df = pd.read_csv('sample_ebird_data.txt', sep='\t', index_col='GLOBAL UNIQUE IDENTIFIER')

#force it to display wider in the console instead of wrapping so narrowly
pd.set_option('display.width', 250)
# display the first 5 rows to view example data
print(df.head(n=10))

# display summary stats (at least for numeric columns)
print(df.describe)
# check to make sure unique identifier is unique
print('\nIndex unique? ' + str(df.index.is_unique))

# get the count for each bird species' sightings (by common name),
# and filter out those that have been seen less than 3 times
cn = pd.Series(df['COMMON NAME']).value_counts()
cn = cn[cn > 2]
# display the list of species seen 3 or more times
print('\nSpecies seen in more than 2 sightings, by common name:')
print(cn)

# calculate the total of these birds counted and display
# print('\n Count of birds sighed by common name:')
# print(df.pivot_table('OBSERVATION COUNT',index='COMMON NAME', aggfunc='sum'))
# what are those Xs messing up the sums?
# (it's the 2nd most common value)
# print(df['OBSERVATION COUNT'].value_counts())
# data dictionary says X indicates uncounted presence, so let's call them 1s for now
# (note: may be bad for analysis, just exploring now)
df_counting = pd.DataFrame(df['OBSERVATION COUNT'].replace(to_replace='X', value='1'))
# rename the column so it will have a different name than original column after merge
df_counting.rename(columns={'OBSERVATION COUNT': 'OBS COUNT MODIFIED'}, inplace=True)
df = pd.concat([df, df_counting], axis=1)

# calculate the total of birds counted, using a pivottable
df_pivot = pd.DataFrame(df.pivot_table('OBS COUNT MODIFIED', index='COMMON NAME', aggfunc='sum'))
df_pivot.rename(columns={'OBS COUNT MODIFIED': 'PIVOTED COUNT'}, inplace=True)
#print(df_pivot)
# compare pivot to groupby
df_grouped = pd.DataFrame(df.groupby(['COMMON NAME'])['OBS COUNT MODIFIED'].sum())
df_grouped.rename(columns={'OBS COUNT MODIFIED': 'GROUPED COUNT'}, inplace=True)
#print(df_grouped)
#combine so you can see side by side and display the list
#print('\nCount of birds sighted by common name:')
#pivot_group_compare = pd.concat([df_pivot, df_grouped], axis=1)
#print(pivot_group_compare)

#print common names where more than 2000 birds were sighted
print('\nCount of species with over 2000 birds sighted:')
print(df_grouped[df_grouped['GROUPED COUNT'].astype('int') > 2000])

#i want to know how many sightings are represented
#df_sum_count = pd.concat([cn,df_grouped], axis=1, join='inner', keys=['COMMON NAME'])
#print(df_sum_count)
#not working yet

#get counting df in same format
df_counting = pd.DataFrame(df.pivot_table('OBS COUNT MODIFIED', index='COMMON NAME', aggfunc='count'))
df_counting.rename(columns={'OBS COUNT MODIFIED': 'OBSERVATIONS'}, inplace=True)
df_grouped.rename(columns={'GROUPED COUNT': 'BIRDS COUNTED'}, inplace=True)

#determine min latitude for any bird sighting in dataset
print('\nOverall Min Latitude: ' + str(df.min()['LATITUDE']) )

#get min latitude per species and combine the dataframes
#and rename the columns before recombining so we can tell what summarization is in each
df_min_lats =  pd.DataFrame(df.pivot_table('LATITUDE', index='COMMON NAME', aggfunc='min'))
df_min_lats.rename(columns={'LATITUDE': 'MIN LATITUDE'}, inplace=True)
df_max_lats =  pd.DataFrame(df.pivot_table('LATITUDE', index='COMMON NAME', aggfunc='max'))
df_max_lats.rename(columns={'LATITUDE': 'MAX LATITUDE'}, inplace=True)
#print(df_min_lats,df_max_lats)
df_min_max = pd.concat([df_min_lats, df_max_lats, df_counting, df_grouped], axis=1)
print('\nSummary: latitude ranges and counts:')
print(df_min_max)