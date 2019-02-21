#%%
print("Hello world")

#%%
import pandas as pd
url = "https://data.sfgov.org/api/views/5cei-gny5/rows.csv?accessType=DOWNLOAD"
evictions = pd.read_csv(url)

#%%
evictions.info()

#%%
evictions.Address()

#%%
evictions.eviction_ID()

#%%
evictions.Address

#%%
evictions.columns = evictions.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('(', '').str.replace(')', '').str.replace('-', '')

#%%
evictions.columns

#%%
evictions.info()

#%%
evictions.breach

#%%
evictions.eviction_notice_source_zipcode.value_counts()

#%%
evictions.owner_move_in.value_counts()


#%%
evictions.eviction_notice_source_zipcode == '94110'
#%%
evictions[evictions.eviction_notice_source_zipcode == '94110']

#%%
evictions[evictions.eviction_notice_source_zipcode == '94117']

#%%
evictions.eviction_notice_source_zipcode.value_counts()

#%%
evictions.columns

#%%
evictions.neighborhoods__analysis_boundaries

#%%
evictions.info()

#%%
evictions.eviction_notice_source_zipcode.count()

#%%
evictions.count()

#%%
evictions.neighborhoods__analysis_boundaries.count()

#%%
evictions.address.value_counts()

#%%
evictions[evictions.eviction_notice_source_zipcode == '94110']

#%%
