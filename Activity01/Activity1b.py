# import pandas and numpy libraries
import pandas as pd
import numpy as np

# read in text file, which is tab delimited, and set global unique indentifier as the index column
df = pd.read_csv('ebird_rubythroated_Jan2013_Aug2015.txt', sep='\t', index_col='GLOBAL UNIQUE IDENTIFIER', error_bad_lines=False, warn_bad_lines=True)
#error on row 36575
#pandas.parser.CParserError: Error tokenizing data. C error: Expected 44 fields in line 36575, saw 45
#set error_bad_lines to false so it would just skip that line and keep going

#force it to display wider in the console instead of wrapping so narrowly
pd.set_option('display.width', 250)
# display the columns of data
print(df.columns)
# display the first 5 rows to view example data
#print(df.head(n=10))
#not all of the columns are visible in the head print, set pandas to output all of the columns
pd.options.display.max_columns = 50
# display the first 5 rows to view example data (this time all columns)
print(df.head(n=10))

# display summary stats (at least for numeric columns)
print('\nSummary statistics:')
print(df.describe())

# check to make sure unique identifier is unique
print('\nIndex unique? ' + str(df.index.is_unique))

#data types of columns
print('\nColumn Data Types:')
print(df.dtypes)

#how many empty/null values in each column?
print('\nCount of null values by column: ')
#display the oolumns with blank values (skip others)
print(df.isnull().sum()[df.isnull().sum() > 0])
#print that one row with a null locality
print('\n1 Row with null Locality: ')
print(df.loc[df['LOCALITY'].isnull()].transpose())

#row-col indexing - print the 1000th row, 13th column
print('\n1000th Row, 12th column (State/Province): ' + df.ix[1000][11])

# get the count for each bird species' sightings (by common name)
cn = pd.Series(df['COMMON NAME']).value_counts()
print('\nRuby-Throated Hummingbird sightings in dataset:')
print(cn)

# data dictionary says X indicates uncounted presence, so let's call them 1s for now
# (note: may be bad for analysis, just exploring now)
df_counting = pd.DataFrame(df['OBSERVATION COUNT'].replace(to_replace='X', value='1'))
# rename the column so it will have a different name than original column after merge
df_counting.rename(columns={'OBSERVATION COUNT': 'OBS COUNT MODIFIED'}, inplace=True)
df = pd.concat([df, df_counting], axis=1)
#print(df)

#see how many different observation count values there are. getting error below, want to make sure Xs are gone
#df_obs = pd.DataFrame(df.groupby(['OBS COUNT MODIFIED'])['OBSERVATION COUNT'].count())
#print('\n\n')
#print(df_obs.sort_values(['OBSERVATION COUNT'],ascending=False))

#to fix below: http://stackoverflow.com/questions/17432944/python-pandas-error-when-doing-groupby-counts
# # calculate the total number of birds counted by state (note - same single bird can be re-counted), using groupby sum
# df_grouped = pd.DataFrame(df.groupby(['STATE_PROVINCE'])['OBS COUNT MODIFIED'].sum())
# df_grouped.rename(columns={'OBS COUNT MODIFIED': 'GROUPED COUNT'}, inplace=True)
# #print(df_grouped)
# #print states where more than 20000 birds were sighted
# print('\nStates with over 20000 birds sighted (same bird can be recounted):')
# print(df_grouped[df_grouped['GROUPED COUNT'].astype('int') > 20000])
# # #error when grouped by common name (all ruby throated) - python int too large to convert to C long (overflow)

#view the earliest and latest observation date in the dataset
#note to check when wider date range available - determining minimum string? does it know this is a date?
print('\nDate range of observations: ' + str(df['OBSERVATION DATE'].min()) + ' - ' + str(df['OBSERVATION DATE'].max()))

#determine min latitude for any bird sighting in dataset
print('\nOverall Min Latitude: ' + str(df.min()['LATITUDE']))

#get min latitude per species and combine the dataframes
#and rename the columns before recombining so we can tell what summarization is in each
df_min_lats =  pd.DataFrame(df.pivot_table('LATITUDE', index='COMMON NAME', aggfunc='min'))
df_min_lats.rename(columns={'LATITUDE': 'MIN LATITUDE'}, inplace=True)
df_max_lats =  pd.DataFrame(df.pivot_table('LATITUDE', index='COMMON NAME', aggfunc='max'))
df_max_lats.rename(columns={'LATITUDE': 'MAX LATITUDE'}, inplace=True)
#print(df_min_lats,df_max_lats)
df_min_max = pd.concat([df_min_lats, df_max_lats], axis=1) #removed df_grouped
print('\nSummary: latitude ranges and counts:')
print(df_min_max)
#note - it looks like in some cases, the unique identifier is being confused for the common name -need to fix
#fixed by removing df_count from concatenated dataframe

#show min max latitude for Ruby-Throated Hummingbird by month
#calculate month from observation date (forget year)
df['OBS MONTH'] = df['OBSERVATION DATE'].str[5:7]
#and rename the columns before recombining so we can tell what summarization is in each
df_min_lats =  pd.DataFrame(df.pivot_table('LATITUDE', index='OBS MONTH', aggfunc='min'))
df_min_lats.rename(columns={'LATITUDE': 'MIN LATITUDE'}, inplace=True)
df_max_lats =  pd.DataFrame(df.pivot_table('LATITUDE', index='OBS MONTH', aggfunc='max'))
df_max_lats.rename(columns={'LATITUDE': 'MAX LATITUDE'}, inplace=True)
#print(df_min_lats,df_max_lats)
df_min_max = pd.concat([df_min_lats, df_max_lats], axis=1) #removed df_grouped
print('\nSummary: latitude ranges and counts:')
print(df_min_max)
