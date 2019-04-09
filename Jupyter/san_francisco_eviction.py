#%% [markdown]
# # Data Analysis of San Francisco Evictions
#%% [markdown]
# Currently, San Francisco and the Bay Area are struggling with a difficult housing crisis. We've all heard the stories of people living out of their RVs, people paying extorbitant rents to live in tiny apartments, and the growing prevalence of homeless people. While news outlets have covered the housing crisis extensively, San Francisco's Eviction Data may hold clues to aspects that have not yet been deeply reported in the news. 
# 
# Within the San Francisco Evictions data set, there are a number of data points we can examine. Most of the data points revolve around a reason for eviction, and our group decided to tackle the reasons in hopes of encountering interesting findings that could either challenge our assumptions about the housing crisis or affirm information we already had. 
# 
# The original source of data can be found here: https://data.sfgov.org/Housing-and-Buildings/Eviction-Notices/5cei-gny5/data
#%% [markdown]
# <font color=blue>Lines 4-5 allow us to import the eviction data and read it into Jupyter Notebook</font>

#%%
# Change directory to VSCode workspace root so that relative path loads work correctly. Turn this addition off with the DataScience.changeDirOnImportExport setting
import os
try:
	os.chdir(os.path.join(os.getcwd(), '..'))
	print(os.getcwd())
except:
	pass


#%%
#importing the file and datetime and pandas
from datetime import datetime as dt
import pandas as pd
get_ipython().run_line_magic('matplotlib', 'inline')
url = "https://data.sfgov.org/api/views/5cei-gny5/rows.csv?accessType=DOWNLOAD"
evictions = pd.read_csv(url, parse_dates=['File Date'])

#%% [markdown]
# <font color=blue>Before looking at our data, the code below cleans it by changing all of the columns to snake_case and deleting trailing white space.</font>

#%%
#making the column names look pretty
evictions.columns = evictions.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('(', '').str.replace(')', '').str.replace('-', '')

#%% [markdown]
# <font color=blue>In this step we confirm the changes made above and make an assessment of the dataset, in addition to checking for missing values.</font>

#%%
#look at the names and the values
evictions.info()

#%% [markdown]
# ## Get Acquainted with the Data
#%% [markdown]
# In looking at all of the column headers of our data, we can see the full picture of all the information the San Francisco Government has collected. Here, we can look at reasons for evictions, we can also do analysis by neighborhood or location. Notice that the first column is 'eviction_id'. We can identify this value as unique, and it will help us down the line when we need to identify how many evictions, along with other analysis moving forward.  
#%% [markdown]
# <font color=blue>This code serves to group by 'eviction_id' and filter duplicates. The category of 'eviction_id' is supposed to uniquely identify each eviction. Therefore, if any records have the same number, it reveals there are duplicates within the data set.</font>

#%%
#check if there are duplicate values 
evictions.groupby(by='eviction_id').filter(lambda x: len(x)>1)


#%%
#check if the nunique matches the row count - nunique is # of unique values
evictions.eviction_id.nunique()


#%%
#check the zipcodes
evictions['eviction_notice_source_zipcode'].describe()


#%%
#check the unique values in the zipcodes, data needs standardization
evictions['eviction_notice_source_zipcode'].unique()


#%%
#fix zipcode one
evictions[evictions['eviction_notice_source_zipcode'] == '941 1']
evictions.at[35204, 'eviction_notice_source_zipcode'] = '941'


#%%
#fix zipcode two
evictions[evictions['eviction_notice_source_zipcode'] == '941??']
evictions.at[35414, 'eviction_notice_source_zipcode'] = '941'


#%%
#convert the zipcode field into a float and then an integer
evictions['eviction_notice_source_zipcode'] = evictions['eviction_notice_source_zipcode'].astype(float).fillna(0.0)
evictions['eviction_notice_source_zipcode'] = evictions['eviction_notice_source_zipcode'].astype(int)

#%% [markdown]
# <font color=blue>Lines 10-14 isolated zipcode information and then cleaned it by eliminating white space and finally converted them from floats to integers.</font>

#%%
#check what the zipcode field looks like
evictions.eviction_notice_source_zipcode.head(10)


#%%
#get all the values that are lower than 94101 which is the lowest real zipcode

missing = evictions.loc[evictions['eviction_notice_source_zipcode'] < 94101, ['address']]


#%%
#check the number of missing values
#Here we check the count of the 'missing' values - which means we check the count of all of the incomplete zipcodes
missing.count()

#%% [markdown]
# <font color=blue>Steps 16-17 gather the zipcodes that are incomplete. Some zipcodes have 4 or less numbers and are not full zip codes - and finding those values helps us identify the dirty data.</font>
# 
# Despite the attempts to standardize and clean the zip code data, after we ran 'count()' on the number of missing zip codes, we learned that there are 822 records with incomplete or missing zip codes.
# We were hoping to do some analysis by zip code - but after vetting this data and seeing that it was incomplete, any analysis on that particular category would be incomplete.
# 

#%%
#check the info field for the names of the reason fields
#With this piece of code, we searched through the reason column to ensure all rows had data in them. 
evictions.info()


#%%
#group by the reason fields, get the frequency for every combination and sort high to low 
evictions.groupby(['non_payment', 'breach', 'nuisance', 'illegal_use', 'failure_to_sign_renewal', 'access_denial', 'unapproved_subtenant', 'owner_move_in', 'demolition', 'capital_improvement', 'substantial_rehab', 'ellis_act_withdrawal', 'condo_conversion', 'roommate_same_unit', 'other_cause', 'late_payments', 'lead_remediation', 'development', 'good_samaritan_ends']).size().reset_index().sort_values(0, ascending=False).head(10)


#%%
#get it into a variable
#The reasons data extracted above is now created into a variable. 
reasons = evictions.groupby(['non_payment', 'breach', 'nuisance', 'illegal_use', 'failure_to_sign_renewal', 'access_denial', 'unapproved_subtenant', 'owner_move_in', 'demolition', 'capital_improvement', 'substantial_rehab', 'ellis_act_withdrawal', 'condo_conversion', 'roommate_same_unit', 'other_cause', 'late_payments', 'lead_remediation', 'development', 'good_samaritan_ends'], as_index=False).size().reset_index().sort_values(0, ascending=False)

#%% [markdown]
# <font color=blue>The code above displays the data by the reason categories, then it computes how often the sequence of False/True/etc comes up in a data set. We then use reset index to create a dataframe which allows for more data manipulation than a series does. It then sorts the count by descending and are looking at the top 10 pieces of data. For further analysis, we will only take into account these unique combinations. That means that if we talk about 'owner move in occurs 10018 times', that means we are talking about records which cite owner move in as the sole reason for eviction.</font>

#%%
#rename the frequency column to 'frequency'
reasons.rename(columns={0 : 'frequency'}, inplace=True)


#%%
#add a true_count field that shows how many reasons are listed for the eviction
reasons['true_count'] = (reasons[['non_payment', 'breach', 'nuisance', 'illegal_use', 'failure_to_sign_renewal', 'access_denial', 'unapproved_subtenant', 'owner_move_in', 'demolition', 'capital_improvement', 'substantial_rehab', 'ellis_act_withdrawal', 'condo_conversion', 'roommate_same_unit', 'other_cause', 'late_payments', 'lead_remediation', 'development', 'good_samaritan_ends']] == True).sum(axis=1)

#%% [markdown]
# <font color=blue>In this line above, we create a variable called 'true_count'  which checks all the boolean values in each column specified for each row and checks how often the 'true' value occurs and counts it. 
# When a value comes back as true, that means that under that specific column, in that row, it affirms the reason for that eviction. A false value means that reason was flagged as false for the eviction.In rows with 0 in 'true_count' there was no reason given for the eviction.</font>

#%%
#sort on the true_count for the lowest values to see how many missing values there are
reasons.sort_values('true_count').head(10)

#%% [markdown]
# <font color=blue>Sorting on 'true_count' shows you - in ascending order - if there are any rows with a '0' count, which turn out to be evictions with no reason given. The frequency tells you how many of those rows come up in the data.</font>  
# 
# ## Analysis
# 
# If a row returns false for every eviction reason, it means they gave no eviction reason. For the table above, the only row with no eviction reasons is the first row. From this information we can reasonably conclude that in 321 evictions, the records cite no reason.
# To take that a step further, 321 evictions might have happened for no reason at all. In the context of a housing crisis, that number is unsettling. It is important to remember that this number is of all evictions from 1997 to 2017 - so the number of evictions per year with no reason given will be much less. It is also possible that within the eviction process, someone forgot to file the paper work and no reason was assigned to that particular case.

#%%
#sort on the highest values to see which records have the most reasons
reasons.sort_values('true_count', ascending=False).head(10)


#%%
#check the top reasons to see how many true counts they have
reasons.head(10)


#%%
#add the true_count to the evictions field as well
evictions['true_count'] = (evictions[['non_payment', 'breach', 'nuisance', 'illegal_use', 'failure_to_sign_renewal', 'access_denial', 'unapproved_subtenant', 'owner_move_in', 'demolition', 'capital_improvement', 'substantial_rehab', 'ellis_act_withdrawal', 'condo_conversion', 'roommate_same_unit', 'other_cause', 'late_payments', 'lead_remediation', 'development', 'good_samaritan_ends']] == True).sum(axis=1)


#%%
#check the records with no reasons
evictions[evictions.true_count == 0].reset_index().sort_values('true_count', ascending=False).head(10)

#%% [markdown]
# <font color=blue>The code above created the table we see now. We have 'true-count' for reasons - which is a subset of the full dataset. Evictions is the full data set - in this line, we are adding the 'true-count' column to the original dataset. This allows us to create a variable with all the complete records that have no reason given for evictions, which is potentially helpful in future analysis.</font>

#%%
#put it into a variable
no_reason = evictions[evictions.true_count == 0].reset_index().sort_values('true_count', ascending=False)

#%% [markdown]
# <font color=blue>This line creates a variable called no reason - which isolates eviction records that have a true count of 0, then the values are sorted - althought all values are 0.</font>
# 
# Before, we checked evictions with no given reason within the 'reasons' variable. Now we are double-checking the evictions with no given reason within the entire data set. We get the same 321 count that we did when we did the initial check.
# This is another way of vetting the data, making sure that information is consistent across different variables as we illustrated above. 
# 

#%%
#check how many empty records there are
no_reason.eviction_id.nunique()


#%%
#function to get the name of the column where the reason is true
def get_name(row):
    b = reasons.loc[row.name] == True
    item = []
    for key, value in b.items():
        if key != 'frequency' and key != 'true_count':
            if value == True:
                item.append(key)

    b['value'] = item
    return b['value']


#%%
#same but for the evictions dataframe
def evic_name(row):
    b = evictions.loc[row.name] == True
    item = []
    for key, value in b.items():
        if key != 'frequency' and key != 'true_count':
            if value == True:
                item.append(key)

    b['value'] = item
    return b['value']

#%% [markdown]
# <font color=blue>The piece of code above isolates the row name, where the boolean value is true. It returns that information for the reasons dataframe and then for the evictions dataframe as well.</font>
# 
# The two lines of code below then add the reason name to every record - then it allows you to see side by side with the 'true_count' what the reason was for that particular eviction record. Technically you could find this same information by going through each reason column until you find 'True' but this way saves you a whole lot of time and allows you to analyze the data more intuitively. 
# 

#%%
#add the reason to the dataframe reasons
reasons['reason'] = reasons.apply(get_name, axis=1)


#%%
#add the reason to the dataframe evictions
evictions['reason'] = evictions.apply(evic_name, axis=1)


#%%
#clean the reason column, standardize
reasons['reason'] = reasons['reason'].astype(str)
reasons.reason = reasons.reason.str.strip('[').str.strip(']').str.replace("'", "").str.strip()


#%%
#clean the reason column, standardize
evictions['reason'] = evictions['reason'].astype(str)
evictions.reason = evictions.reason.str.strip('[').str.strip(']').str.replace("'", "").str.strip()


#%%
#check what it looks like
reasons.head()

#%% [markdown]
# ## Analysis
# 
# The table above shows the results of the code from a few lines ago. By scrolling all the way to the right, you can find the most important information in this data set. The frequency of records that have a true count for 'owner_move_in' is 10,018. Automatically, we learn that owner moveins are one of the highest reasons for eviction in San Francisco. This is interesting to think about because this piece of information brings up so many questions. Are the owners just moving in temporarily to fix up the place and then rent at higher rates? Are owners themselves having a hard time finding housing and thus have to resort to moving out their tenants? And, who are all those loud neighbors that made so much noise the owners had to move them out?
# Good data creates questions to investigate - and within each of these questions there is a potential story. 

#%%
#check what it looks like
#This line illustrates the reason variable - and it shows what eviction records with multiple reasons looks like
reasons.tail()

#%% [markdown]
# ## Analysis
# 
# Now at the tail end of the same table we looked at previously, we learn that there are evictions with multiple true counts, meaning there was more than one reason driving the eviction. Apparently, some of the eviction records have four reasons. Most of the records for San Francisco evictions only have one reason, so the finding that some eviction records have multiple reasons driving the eviction is a neat finding. Again, these data points just bring more questions that can turn into potential stories. It seems that the eviction records with more than one reason show that in some ways, allowances might have been given by some owners. Perhaps it shows an owner's willingness to try and work with their tenants. On the other hand, the fact that there are so few records with multiple reasons might actually give the opposite impression. Lastly, that data was not explicitly collected, and so there is no way to tell (except with further investigation, of course!)

#%%
#get a new variable with just the reason and the frequency
top_reasons = reasons[['reason', 'frequency']]


#%%
#check what it looks like
top_reasons.head(10)


#%%
#make a chart of the top ten reasons of all time
chart = top_reasons.head(10).frequency.plot.barh(title='Top Eviction Reasons Of All Time')
chart.set_yticklabels(top_reasons.reason)

#%% [markdown]
# In the bar graph above, the results of the table with eviction reasons and the frequency is displayed in ascending order. By looking at this chart, you can read the top eviction reason and you can see how far ahead that reason is compared to the one that comes next in line. The top 5 reasons have sizeable gaps in between each other, but the bottom 5 reasons are not that different from each other in frequency. All of this information is readable on the table above, but it is more quickly understood through this data visualization. 

#%%
#check the date field in the evictions dataframe
evictions.file_date.describe()


#%%
#setting the year column by extracting the year
evictions['year'] = pd.to_datetime(evictions['file_date'], format = '%Y,%m,%d').dt.year

#%% [markdown]
# Creating this column will allow us to make more detailed analysis of the data - seeing the top reasons behind evictions in San Francisco over time can reveal trends about the data that are not decipherable by looking at all the data grouped together.

#%%
#check if we have all the values from 1997-2019
evictions.year.unique()


#%%
#clean up the reason column again because I got a weird error here
evictions['reason'] = evictions['reason'].astype(str)
evictions.reason = evictions.reason.str.strip('[').str.strip(']').str.replace("'", "").str.strip()


#%%
#make a new variable grouped by the reason and the year
reason_year = evictions.groupby(['reason', 'year']).size().reset_index().sort_values(0, ascending=False)


#%%
#check the head, the first 10 values to determine which reason for eviction in descending order by frequency, with the year added
reason_year.head(10)


#%%
#rename frequency column
reason_year.rename(columns={0 : 'frequency'}, inplace=True)


#%%
#get the sorted values, first by year then frequency
top_year = reason_year.sort_values(['year', 'frequency'], ascending=False)


#%%
#top for 2018
top_2018 = top_year[top_year.year == 2018]

#%% [markdown]
# While it is great to look at specific eviction reasons over time, it is valuable to hone in on a particular year, especially if it is the year that just passed. The code above will allow us to make more detailed analysis of the data. This step can help  reveal trends about the data that are not decipherable by looking at all the data grouped together.

#%%
#set reason as index
top_2018 = top_2018.set_index('reason')


#%%
#check the head
top_2018.head()


#%%
#drop the year column
top_2018 = top_2018.drop(['year'], axis=1)


#%%
#plot
top_2018.head(10).plot.barh(title='Top Reasons for Eviction in 2018')

#%% [markdown]
# ## Analysis
# 
# This chart illustrates the reasons for eviction by frequency in ascending order. It allows you to visualize immediately how much more breaches cause evictions over any other category and also shows that 'nuisance' while being a close second, is not necessarily that close behind. Although 'owner_move_in' is the highest reason for evictions overall, in 2018, it came in fourth. Also, 'breach' the reason with the most evictions was far ahead in driving evictions in 2018. This specific data points brings up many questions, such as: What is causing all of these breaches in renting contracts? Are there different breaches of contract that can be broken down into subcategories? And if so, what can those categories be? The reason the question of subcategories comes up for us is because the breaches in contract far outpaced any other reason for eviction in 2018, and it would be helpful to see what is actually behind those numbers.  

#%%
#get the values for nuisance over the years
top_nuisance = top_year[top_year.reason == 'nuisance']


#%%
#drop the reason
top_nuisance = top_nuisance.drop(['reason'], axis=1)


#%%
#drop 2019
top_nuisance = top_nuisance.drop([749])


#%%
#set year as index
top_nuisance = top_nuisance.set_index('year')

#%%
import matplotlib.ticker as ticker

#%%
#plot
#Here we plotted how Nuisances as a reason for eviction changed overtime. 
nuisance_chart = top_nuisance.plot(title='Nuisance Evictions 1997-2017')
nuisance_chart.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))

#%% [markdown]
# Nuisance evictions over time, when we imagine a trend line, seem to have gone quite a bit over time. Another interesting point is that there were several huge dips and several huge spikes over the years.
#%%
#all the same but for breach
top_breach = top_year[top_year.reason == 'breach']


#%%
top_breach = top_breach.drop(['reason'], axis=1)


#%%
top_breach = top_breach.drop([75])


#%%
top_breach = top_breach.set_index('year')


#%%
breach_chart = top_breach.plot(title='Breach Evictions 1997-2017')
breach_chart.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))

#%% [markdown]
# Here we have the same as above, a line chart that plots breaches as the reason for eviction over time. This chart reveals a finding that is not easily decipherable by looking at the raw data. Although Breaches are the top reason for eviction in 2018, eviction breaches have been much higher in past years. In 2015, San Francisco had almost double the amount of eviction for breaches that it had for 2018 - Surely there is a story there that can be uncovered with further research.

#%%
#same but for owner
top_owner = top_year[top_year.reason == 'owner_move_in']


#%%
#Sorted owner move in eviction records by year
top_owner.sort_values('year')


#%%
top_owner = top_owner.drop(['reason'], axis=1)


#%%
top_owner = top_owner.drop([945])


#%%
#owner move in evictions frequency in the last 5 years
top_owner.head()


#%%
top_owner = top_owner.set_index('year')


#%%
#plots owner move in evictions over the years
owner_chart = top_owner.plot(title='Owner Move-in Evictions 1997-2017')
owner_chart.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))

#%% [markdown]
# This chart illustrates how 'owner_move_in' reasons for eviction have in some ways trailed off in the 20 year period illustrated by this graph.
# 
# ## Finding: 
# 20 years ago, evictions for owner move-ins peaked at 1400 evictions. In 2017, there's a little over 200. That is a significant drop. Potentially, this can mean that owners had the capital to not sublet or lease out apartments they owned, which in turn can allow them to move in. This could also highlight factors outside of our data such as how affordable it is to live in San Francisco - either way, this line chart shows a huge discrepancy in where owner move-in evictions are and where they were 20 years ago. 

#%%
#get top three reasons of all time
three_reasons = ['owner_move_in', 'breach', 'nuisance']


#%%
#make a list with those values
top_three = top_year[top_year.reason.isin(three_reasons)]


#%%
top_three = top_three.drop([75, 749, 945])


#%%
top_three.head(10)


#%%
#make a pivot table
top_pivot = top_three.pivot(index='year', columns='reason', values='frequency')

#%% [markdown]
# <font color=blue>Making a pivot table that includes each eviction reason, the year and the frequency, helps us look at all 3 reasons side by side.</font>
# 

#%%
#This piece of code plots the pivot table made above
pivot_chart = top_pivot.plot(title='Top 3 Eviction Reasons 1997-2017')
pivot_chart.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))

#%% [markdown]
# ## Analysis
# 
# Another Finding is that Nuisance evictions seem to stay relatively close to the same frequency - while owner move in and breaches are a bit more sporadic. The last interesting finding is that owner move ins for the late 1990s were pretty high - surely with more investigation, one could find an interesting story there. Lastly, looking at the 2007-2010 part of the graph, owner move-ins dipped -I think you can reasonably conclude that the financial crisis had an effect on that and had an effect on breaches of contract - as people likely struggled to pay their rent while facing layoffs and underemployment. 
