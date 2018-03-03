import pandas as pd
from matplotlib import pyplot as plt
from scipy.stats import chi2_contingency

# Loading the Data
species = pd.read_csv('species_info.csv')

print(species.head())

species_count = species.scientific_name.nunique()

species_type = species.category.unique()

conservation_statuses = species.conservation_status.unique()

conservation_counts = species.groupby('conservation_status').scientific_name.nunique().reset_index()

print(conservation_counts )

species.fillna('No Intervention', inplace = True)

conservation_counts_fixed=species.groupby('conservation_status').scientific_name.nunique().reset_index()

print(conservation_counts_fixed)


protection_counts = species.groupby('conservation_status')\
    .scientific_name.nunique().reset_index()\
    .sort_values(by='scientific_name')
    
plt.figure(figsize=(10, 4))
ax = plt.subplot()
plt.bar(range(len(protection_counts)),protection_counts.scientific_name.values)
ax.set_xticks(range(len(protection_counts)))
ax.set_xticklabels(protection_counts.conservation_status.values)
plt.ylabel('Number of Species')
plt.title('Conservation Status by Species')
labels = [e.get_text() for e in ax.get_xticklabels()]
plt.show()

species['is_protected'] = species.conservation_status != 'No Intervention'

category_counts = species.groupby(['category', 'is_protected']).scientific_name.nunique().reset_index()

print(category_counts.head())

category_pivot = category_counts.pivot(columns='is_protected',
                      index='category',
                      values='scientific_name')\
                      .reset_index()
  
print(category_pivot)

category_pivot.columns=["category","not_protected","protected"]
print(category_pivot)
category_pivot["percent_protected"]=category_pivot["protected"]/(category_pivot["protected"]+category_pivot["not_protected"])
print(category_pivot)

contingency=[[30,146],[75,413]]
print(contingency)
chi2, pval, dof, expected = chi2_contingency(contingency)
print(pval)
contingency_reptile_mammal=[[5,73],[30,146]]
chi2, pval_reptile_mammal, dof, expected = chi2_contingency(contingency_reptile_mammal)
print(pval_reptile_mammal)


observations= pd.read_csv('observations.csv')
print(observations.head())

species['is_sheep'] = species.common_names.apply(lambda x: 'Sheep' in x)

species_is_sheep = species[species.is_sheep]

print(species_is_sheep)

sheep_species = species[(species.is_sheep) & (species.category == 'Mammal')]

print(sheep_species)

sheep_observations=pd.merge(sheep_species,observations,how='outer')
print(sheep_observations.head())
obs_by_park=sheep_observations.groupby("park_name").observations.sum().reset_index()
print(obs_by_park)


plt.figure(figsize=(16, 4))
ax = plt.subplot()
plt.bar(range(len(obs_by_park)),obs_by_park.observations.values)
ax.set_xticks(range(len(obs_by_park)))
ax.set_xticklabels(obs_by_park.park_name.values)
plt.ylabel('Number of Observations')
plt.title('Observations of Sheep per Week')
labels = [e.get_text() for e in ax.get_xticklabels()]
plt.show()

baseline=15
minimum_detectable_effect=100*5/baseline
print(minimum_detectable_effect)
sample_size_per_variant=39000