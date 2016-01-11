# import pandas and numpy libraries
import pandas as pd

# read in text file, which is tab delimited, and set global unique indentifier as the index column
df = pd.read_csv('ebird_rubythroated_Jan2013_Aug2015.txt', sep='\t', index_col='GLOBAL UNIQUE IDENTIFIER',
                 error_bad_lines=False, warn_bad_lines=True)
# error on row 36575
# pandas.parser.CParserError: Error tokenizing data. C error: Expected 44 fields in line 36575, saw 45
# set error_bad_lines to false so it would just skip that line and keep going

# force it to display wider in the console instead of wrapping so narrowly
pd.set_option('display.width', 250)
# set pandas to output all of the columns in output (was truncating)
pd.options.display.max_columns = 50
# display the list of data columns
print(df.columns)
# display the first 10 rows to view example data (this time all columns)
print(df.head(n=10))

# display summary stats (at least for numeric columns)
print('\nSummary statistics:')
print(df.describe())

# check to make sure unique identifier is unique
print('\nIndex unique? ' + str(df.index.is_unique))

# data types of columns
print('\nColumn Data Types:')
print(df.dtypes)

# how many empty/null values in each column?
print('\nCount of null values by column (columns with no nulls not displayed): ')
# display the columns with blank values (skip others)
print(df.isnull().sum()[df.isnull().sum() > 0])
# find/print that one row with a null locality value
print('\n1 Row with null Locality: ')
print(df.loc[df['LOCALITY'].isnull()].transpose())

# pandas dataframe row-col indexing - print the 1000th row, 13th column
print('\n1000th Row, 12th column (State/Province): ' + df.ix[1000][11])

# get the count for each bird species' sightings (by common name)
cn = pd.Series(df['COMMON NAME']).value_counts()
print('\nNumber of Ruby-Throated Hummingbird sightings (rows) in dataset:')
print(cn)

# data dictionary says X indicates uncounted presence, so let's call them 1s for now
# (note: may be bad for analysis, just exploring now)
df_counting = pd.DataFrame(df['OBSERVATION COUNT'].replace(to_replace='X', value='1'))
# rename the column so it will have a different name than original column after merge
df_counting.rename(columns={'OBSERVATION COUNT': 'OBS COUNT MODIFIED'}, inplace=True)
df = pd.concat([df, df_counting], axis=1)
# print(df)

# view the earliest and latest observation date in the dataset
print('\nDate range of observations: ' + str(df['OBSERVATION DATE'].min()) + ' - ' + str(df['OBSERVATION DATE'].max()))

# get min latitude per species and combine the dataframes (made more sense in sample dataset with multiple species)
# and rename the columns before recombining so we can tell what summarization is in each
df_min_lats = pd.DataFrame(df.pivot_table('LATITUDE', index='COMMON NAME', aggfunc='min'))
df_min_lats.rename(columns={'LATITUDE': 'MIN LATITUDE'}, inplace=True)
df_max_lats = pd.DataFrame(df.pivot_table('LATITUDE', index='COMMON NAME', aggfunc='max'))
df_max_lats.rename(columns={'LATITUDE': 'MAX LATITUDE'}, inplace=True)
# print(df_min_lats,df_max_lats)
df_min_max = pd.concat([df_min_lats, df_max_lats], axis=1)  # removed df_grouped
print('\nSummary: latitude ranges and counts:')
print(df_min_max)

# show min max latitude for Ruby-Throated Hummingbird by month
# calculate month from observation date (forget year)
df['OBS MONTH'] = df['OBSERVATION DATE'].str[5:7]
# and rename the columns before recombining so we can tell what summarization is in each
df_min_lats = pd.DataFrame(df.pivot_table('LATITUDE', index='OBS MONTH', aggfunc='min'))
df_min_lats.rename(columns={'LATITUDE': 'MIN LATITUDE'}, inplace=True)
df_max_lats = pd.DataFrame(df.pivot_table('LATITUDE', index='OBS MONTH', aggfunc='max'))
df_max_lats.rename(columns={'LATITUDE': 'MAX LATITUDE'}, inplace=True)
# print(df_min_lats,df_max_lats)
df_min_max = pd.concat([df_min_lats, df_max_lats], axis=1)  # removed df_grouped
print('\nSummary: latitude ranges by Observation Month (in any year 2013-2015):')
print(df_min_max)
