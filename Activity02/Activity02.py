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
#print('\nSummary statistics:')
#print(df.describe())

# data types of columns
print('\nColumn Data Types:')
print(df.dtypes)

#narrow down the dataset for plotting
df_plot = df.loc[:,('OBSERVATION COUNT','COUNTRY','STATE_PROVINCE','LATITUDE','LONGITUDE','OBSERVATION DATE')]
#[['OBSERVATION COUNT','COUNTRY','STATE_PROVINCE','LATITUDE','LONGITUDE','OBSERVATION DATE']] #<< got error when I did it this way, then tried to convert slice column to int below
# #[0:2000]
#replace the X with 1 (or should we remove those values?)
df_plot['OBSERVATION COUNT'] = df_plot['OBSERVATION COUNT'].replace(to_replace='X', value='1').astype(int)
df_plot['OBS MONTH'] = df_plot['OBSERVATION DATE'].str[5:7].astype(int)
print('\nSummary statistics of subset for plotting:')
print(df_plot.describe())

#seaborn scatterplot matrix
import seaborn as sns
sns.pairplot(df_plot[['OBSERVATION COUNT','LATITUDE','LONGITUDE','OBS MONTH']])
sns.plt.show()

#seaborn histogram/distribution of observation count
sns.distplot(df_plot['OBSERVATION COUNT'][df_plot['OBSERVATION COUNT'] < 30],bins=100)
sns.plt.show()

#seaborn boxplots for mexico, US, canada
#.isin(['UNITED STATES','MEXICO','CANADA'])], col="COUNTRY")
#sns.boxplot(x="OBS MONTH", y="LATITUDE", data=df_plot[df_plot['COUNTRY'] == 'UNITED STATES'], palette="Blues_d")
#sns.plt.show()
#how do you show it?? oh, shows up after you close the prior one....

