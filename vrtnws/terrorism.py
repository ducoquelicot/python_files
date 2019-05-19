#%%
import pandas as pd
%matplotlib inline
terrorism = pd.read_csv('vrtnws/vrtnws.csv')

#%%
# Make the column names look better and easier to search through
terrorism.columns = terrorism.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('(', '').str.replace(')', '').str.replace('-', '')

#%%
# Get a list of all the column names
list(terrorism)

#%%
# Check for duplicate values (0 rows means no duplicates)
terrorism.groupby(by='eventid').filter(lambda x: len(x)>1)

#%%
# First question: what were the ten deadliest terrorist attacks between 1970 and 2017?
# In order to know this we need the date, the number of deaths, and the location so that we know where it happened.
# We may also want the terrorist group. 
terrorism[['nkill', 'iyear', 'imonth', 'iday', 'country_txt', 'city', 'gname']].sort_values('nkill', ascending=False).reset_index().head(10)

#%%
# Second question. Which years had the most casualties and how does this develop over time?
# To answer the first part, we need to know the total of casualties per year.
most_casualties = terrorism[['iyear', 'nkill']].fillna(0)

#%%
# This tells us which years had the most casualties, but we can also plot this. Therefore, we need to create
# a new dataframe.
most_casualties.groupby('iyear').nkill.sum().reset_index().sort_values('nkill', ascending=False).head(10)

#%%
total_per_year = most_casualties.groupby('iyear').nkill.sum().reset_index()

#%%
# As a sanity check, we can run it against the values we created in the PivotTable in Excel. Everything seems fine. 
total_per_year.sort_values('iyear', ascending=False).head()

#%%
total_per_year = total_per_year.set_index('iyear')

#%%
# And here is the simple plot we created. We can see there's a serious spike in the more recent years,
# which we already knew from the table, but this displays it better.
total_per_year.plot()

#%%
# Question three: which countries suffered the most terrorist attacks between 1970 and 2017?
# In order to answer this question, we need to count how often each country appears in the list.
terrorism.country_txt.value_counts().head(10)

#%%
# Sanity check for missing values: luckily, there are none.
terrorism.country_txt.isna().sum()

#%%
# Question four: which terrorist groups committed the most attacks between 1970 and 2017?
# In order to answer this question, we need to count how often each terrorist group appears in the list.
terrorism.gname.isna().sum()

#%%
# As we can see, most terrorist attacks aren't claimed by any specific group - but when they're claimed, the Taliban and ISIL are the 
# two most prominent groups.
terrorism.gname.value_counts().head(10)

#%%
# A side question we can answer is: in which countries do these groups commit the most attacks? 
# We'll have to combine the group with the mode for the country that is most frequent.
country_group = terrorism[['gname', 'country_txt']]

#%%
country_group.groupby('gname')['country_txt'].agg(pd.Series.mode)

#%%
country_group.groupby('gname').head()

#%%
# We can merge the two to see the combined result.
cg = country_group.groupby('gname')['country_txt'].agg(pd.Series.mode).to_frame()

#%%
df = terrorism.gname.value_counts().rename_axis('gname').reset_index(name='count')

#%%
merged = pd.merge(cg, df, on='gname')

#%%
# Now, we can see where these terrorist organizations attack most frequently. 
merged.sort_values('count', ascending=False).head(10)

#%%
# Question five: which type of terrorist attack occurs most frequently between 1970 and 2017?
# In order to answer this question, we need the value count of the different types of terrorist attacks.
terrorism.attacktype1_txt.isna().sum()

#%%
terrorism.attacktype1_txt.value_counts().head(10)

#%%
# Question six: which target type is most common?
# In order to answer this question, we need the value count of the target types.
terrorism.targtype1_txt.isna().sum()

#%%
terrorism.targtype1_txt.value_counts().head(10)

#%%
# Question seven: to which country to terrorist attack victims most often belong?
# In order to answer this question, we need the value count of the nationality.
# We see here that there are +1500 records that have no nationality. This is only a small percentage 
# of the total, but we should keep it in mind nonetheless. 
terrorism.natlty1_txt.isna().sum()

#%%
terrorism.natlty1_txt.value_counts().head(10)

#%%
# We can compare these results to our earlier question of which countries had the most terrorist attacks and
# see how they relate.
ct = terrorism.country_txt.value_counts().rename_axis('country_txt').reset_index(name='no_attacks')

#%%
nt = terrorism.natlty1_txt.value_counts().rename_axis('country_txt').reset_index(name='when_victims')

#%%
dataframe = pd.merge(ct, nt, on='country_txt')

#%%
dataframe.sort_values('when_victims', ascending=False).head(10)

#%%
# What we can see when we sort in the two different ways is that while victims of terrorism attacks are more often Indian,
# there are more attacks in Afghanistan. We also see that US citizens are in the top 10 of victims of terrorist attacks,
# but the US loses its spot in the top ten to the UK when it comes to the frequency of attacks. 
dataframe.sort_values('no_attacks', ascending=False).head(10)

#%%
# We can now revisit our first question and look at the top ten deadliest attacks more broadly:
# what was the target type? Where did the primary victims come from? 
terrorism[['nkill', 'iyear', 'imonth', 'iday', 'country_txt', 'city' ,'gname', 'targtype1_txt', 'natlty1_txt']].sort_values('nkill', ascending=False).reset_index().head(10)

#%%
# Let's zoom in more closely on Belgium. What were the most deadly terrorist attacks in Belgium and
# when were they committed, and by which group?
belgium_attacks = terrorism[['country_txt', 'city', 'iyear', 'imonth', 'iday', 'nkill', 'gname']]

#%%
# Here we can see that the deadliest terrorist attacks in Belgium were committed very recently, in 2016. They were also
# committed by a terrorist group in the top ten of most 'active' terrorist groups: ISIL. 
belgium_attacks[belgium_attacks['country_txt'] == 'Belgium'].sort_values('nkill', ascending=False).reset_index().head(10)

#%%
