#%%
#importing the file and datetime and pandas
from datetime import datetime as dt
import pandas as pd
%matplotlib inline
url = "https://data.sfgov.org/api/views/5cei-gny5/rows.csv?accessType=DOWNLOAD"
evictions = pd.read_csv(url, parse_dates=['File Date'])

#%%
#making the column names look pretty
evictions.columns = evictions.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('(', '').str.replace(')', '').str.replace('-', '')

#%%
#look at the names and the values
evictions.info()

#%%
#check if there are duplicate values
evictions.groupby(by='eviction_id').filter(lambda x: len(x)>1)

#%%
#check if the nunique matches the row count
evictions.eviction_id.nunique()

#%%
#check the zipcodes
evictions['eviction_notice_source_zipcode'].describe()

#%%
#check the unique values in the zipcodes
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
#convert the zipcode field into a string and then an integer
evictions['eviction_notice_source_zipcode'] = evictions['eviction_notice_source_zipcode'].astype(float).fillna(0.0)
evictions['eviction_notice_source_zipcode'] = evictions['eviction_notice_source_zipcode'].astype(int)

#%%
#check what the zipcode field looks like
evictions.eviction_notice_source_zipcode.head(10)

#%%
#get all the values that are lower than 94101 which is the lowest real zipcode
missing = evictions.loc[evictions['eviction_notice_source_zipcode'] < 94101, ['address']]

#%%
#check the number of missing values
missing.count()

#%%
#check the info field for the names of the reason fields
evictions.info()

#%%
#group by the reason fields, get the frequency for every combination and sort high to low
evictions.groupby(['non_payment', 'breach', 'nuisance', 'illegal_use', 'failure_to_sign_renewal', 'access_denial', 'unapproved_subtenant', 'owner_move_in', 'demolition', 'capital_improvement', 'substantial_rehab', 'ellis_act_withdrawal', 'condo_conversion', 'roommate_same_unit', 'other_cause', 'late_payments', 'lead_remediation', 'development', 'good_samaritan_ends']).size().reset_index().sort_values(0, ascending=False).head(10)

#%%
#get it into a variable
reasons = evictions.groupby(['non_payment', 'breach', 'nuisance', 'illegal_use', 'failure_to_sign_renewal', 'access_denial', 'unapproved_subtenant', 'owner_move_in', 'demolition', 'capital_improvement', 'substantial_rehab', 'ellis_act_withdrawal', 'condo_conversion', 'roommate_same_unit', 'other_cause', 'late_payments', 'lead_remediation', 'development', 'good_samaritan_ends'], as_index=False).size().reset_index().sort_values(0, ascending=False)

#%%
#rename the frequency column
reasons.rename(columns={0 : 'frequency'}, inplace=True)

#%%
#add a true_count field that shows how many reasons are listed for the eviction
reasons['true_count'] = (reasons[['non_payment', 'breach', 'nuisance', 'illegal_use', 'failure_to_sign_renewal', 'access_denial', 'unapproved_subtenant', 'owner_move_in', 'demolition', 'capital_improvement', 'substantial_rehab', 'ellis_act_withdrawal', 'condo_conversion', 'roommate_same_unit', 'other_cause', 'late_payments', 'lead_remediation', 'development', 'good_samaritan_ends']] == True).sum(axis=1)

#%%
#sort on the true_count for the lowest values to see how many missing values there are
reasons.sort_values('true_count').head(10)

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

#%%
#put it into a variable
no_reason = evictions[evictions.true_count == 0].reset_index().sort_values('true_count', ascending=False)

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

#%%
#add the reason to the dataframe reasons
reasons['reason'] = reasons.apply(get_name, axis=1)

#%%
#add the reason to the dataframe evictions
evictions['reason'] = evictions.apply(evic_name, axis=1)

#%%
#clean the reason column
reasons['reason'] = reasons['reason'].astype(str)
reasons.reason = reasons.reason.str.strip('[').str.strip(']').str.replace("'", "").str.strip()

#%%
#clean the reason column
evictions['reason'] = evictions['reason'].astype(str)
evictions.reason = evictions.reason.str.strip('[').str.strip(']').str.replace("'", "").str.strip()

#%%
#check what it looks like
reasons.head()

#%%
#check what it looks like
reasons.tail()

#%%
#get a new variable with just the reason and the frequency
top_reasons = reasons[['reason', 'frequency']]

#%%
#check what it looks like
top_reasons.head(10)

#%%
#make a chart of the top ten reasons of all time
chart = top_reasons.head(10).frequency.plot.barh()
chart.set_yticklabels(top_reasons.reason)

#%%
#check the date field in the evictions dataframe
evictions.file_date.describe()

#%%
#setting the year column by extracting the year
evictions['year'] = pd.to_datetime(evictions['file_date'], format = '%Y,%m,%d').dt.year

#%%
#check if we have all the values from 1997-2019
evictions.year.unique()

#%%
#clean up the reason column again because I got a weird error here
evictions['reason'] = evictions['reason'].astype(str)
evictions.reason = evictions.reason.str.strip('[').str.strip(']').str.replace("'", "").str.strip()

#%%
#make a new variablegrouped by the reason and the year
reason_year = evictions.groupby(['reason', 'year']).size().reset_index().sort_values(0, ascending=False)

#%%
#check the head
reason_year.head()

#%%
#rename frequency column
reason_year.rename(columns={0 : 'frequency'}, inplace=True)

#%%
#get the sorted values, first by year then frequency
top_year = reason_year.sort_values(['year', 'frequency'], ascending=False)

#%%
#top for 2018
top_2018 = top_year[top_year.year == 2018]

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
top_2018.head(10).plot.barh()

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
#plot
top_nuisance.plot()

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
top_breach.plot()

#%%
#same but for owner
top_owner = top_year[top_year.reason == 'owner_move_in']

#%%
top_owner.sort_values('year')

#%%
top_owner = top_owner.drop(['reason'], axis=1)

#%%
top_owner = top_owner.drop([945])

#%%
top_owner.head()

#%%
top_owner = top_owner.set_index('year')

#%%
top_owner.plot()

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

#%%
#plot
top_pivot.plot()