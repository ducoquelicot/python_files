#%%
import pandas

#%%
committees = pandas.read_csv("https://first-python-notebook.readthedocs.io/_static/committees.csv")

#%%
committees.info()

#%%
committees.head(30)

#%%
committees.tail()

#%%
contributions = pandas.read_csv("https://first-python-notebook.readthedocs.io/_static/contributions.csv")

#%%
contributions.info()

#%%
contributions.head()

#%%
committees.head()

#%%
committees.prop_name

#%%
committees.prop_name.value_counts()

#%%
committees.prop_name.value_counts().reset_index()

#%%
prop_64 = committees[committees.prop_name == 'PROPOSITION 064- MARIJUANA LEGALIZATION. INITIATIVE STATUTE.']
#%%
prop_64.info

#%%
prop_64.info()

#%%
contributions.info()

#%%
merged = prop_64.merge(contributions, on='calaccess_committee_id', how='inner')

#%%
merged.info()

#%%
merged.committee_position.value_counts()

#%%
merged.amount.sum()

#%%
merged.groupby('committee_position').amount.sum()

#%%
merged[merged.committee_position == 'OPPOSE'].sort_values("amount", ascending = False)

#%%