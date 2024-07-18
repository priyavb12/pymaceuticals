#!/usr/bin/env python
# coding: utf-8

# # Pymaceuticals Inc.
# ---
# 
# ### Analysis
# 
# - Add your analysis here.
#  

# In[ ]:


OBSERVATIONS:

Analyzing trends over time allows us to recognize patterns, or fluctuations in the data.

Planning and implementing strategies based on this information can assist in making more informed decisions.

Correlation Analysis: Examining the relationships between variables in the data can provide insight into how they are related. 

Observing outliers and unusual patterns in the data can help us identify potential errors, fraud, or unique occurrences.


# In[52]:


# Dependencies and Setup
import matplotlib.pyplot as plt
import pandas as pd
import scipy.stats as st

# Study data files
mouse_metadata_path = "./data/Mouse_metadata.csv"
study_results_path = "./data/Study_results.csv"

# Read the mouse data and the study results
mouse_metadata = pd.read_csv(mouse_metadata_path)
study_results = pd.read_csv(study_results_path)

# Combine the data into a single DataFrame
study_mouse_df = pd.merge(study_results,mouse_metadata, how='left',on='Mouse ID')
science_study_data_complete_df = pd.merge(study_results,mouse_metadata,how='left',on='Mouse ID')

# Display the data table for preview
study_mouse_df

science_study_data_complete_df


# In[54]:


mouse_metadata


# In[ ]:





# In[57]:


# Checking the number of mice.
#len(study_mouse_df['Mouse ID'].unique())
len(science_study_data_complete_df['Mouse ID'].unique())


# In[59]:


# Our data should be uniquely identified by Mouse ID and Timepoint
# Get the duplicate mice by ID number that shows up for Mouse ID and Timepoint.
# study_mouse_id = study_mouse_df[study_mouse_df.duplicated(subset=['Mouse ID','Timepoint'])]['Mouse ID'].unique()
# study_mouse_id

duplicated_mouse_ids = science_study_data_complete_df[science_study_data_complete_df.duplicated(subset=['Mouse ID','Timepoint'])]['Mouse ID'].unique()
duplicated_mouse_ids


# In[61]:


# Optional: Get all the data for the duplicate mouse ID.
# duplicate_mouse_id = study_mouse_df[study_mouse_df['Mouse ID']=='g989']
# duplicate_mouse_id

duplicated_mouse_dataset =science_study_data_complete_df[science_study_data_complete_df['Mouse ID'] == 'g989']
duplicated_mouse_dataset


# In[63]:


# Create a clean DataFrame by dropping the duplicate mouse by its ID.
# clean_study_mouse = study_mouse_df[study_mouse_df['Mouse ID'].isin(study_mouse_id) == False]
# clean_study_mouse

clean_study_data_complete = science_study_data_complete_df[science_study_data_complete_df['Mouse ID'].isin(duplicated_mouse_ids) == False]
clean_study_data_complete


# In[65]:


science_study_data_complete_df.dtypes


# In[67]:


# Checking the number of mice in the clean DataFrame.
#len(clean_study_mouse['Mouse ID'].unique())

len(clean_study_data_complete['Mouse ID'].unique())


# ## Summary Statistics

# In[70]:


# Generate a summary statistics table of mean, median, variance, standard deviation, and SEM of the tumor volume for each regimen

# Use groupby and summary statistical methods to calculate the following properties of each drug regimen:
# mean, median, variance, standard deviation, and SEM of the tumor volume.
# Assemble the resulting series into a single summary DataFrame.

means = clean_study_data_complete.groupby('Drug Regimen')['Tumor Volume (mm3)'].mean()

median = clean_study_data_complete.groupby('Drug Regimen')['Tumor Volume (mm3)'].median()
variances = clean_study_data_complete.groupby('Drug Regimen')['Tumor Volume (mm3)'].var()
standard_deviation = clean_study_data_complete.groupby('Drug Regimen')['Tumor Volume (mm3)'].std()
sems = clean_study_data_complete.groupby('Drug Regimen')['Tumor Volume (mm3)'].sem()



summary_table = pd.DataFrame({
          'Mean Tumor Volume' : means,
         'Median Tumor Volume' : median,
         'Tumor Volume Variance' : variances,
          'Tumor Volume Std.Dev': standard_deviation,
          'Tumor Volume Std.Err' : sems             
             
})

summary_table



# In[72]:


# A more advanced method to generate a summary statistics table of mean, median, variance, standard deviation,
# and SEM of the tumor volume for each regimen (only one method is required in the solution)

# Using the aggregation method, produce the same summary statistics in a single line

summary_table = clean_study_data_complete.groupby('Drug Regimen').agg({'Tumor Volume (mm3)':['mean','median','var','std','sem']})
summary_table


# ## Bar and Pie Charts

# In[75]:


# Generate a bar plot showing the total number of rows (Mouse ID/Timepoints) for each drug regimen using Pandas.

counts = clean_study_data_complete['Drug Regimen'].value_counts()
counts.plot(kind='bar')
plt.xlabel('Drug Regimen')
plt.ylabel('Number of Mice')
plt.xticks(rotation=90)
plt.show()


# In[76]:


# Generate a bar plot showing the total number of rows (Mouse ID/Timepoints) for each drug regimen using pyplot.


counts = clean_study_data_complete['Drug Regimen'].value_counts()
plt.bar(counts.index.values, counts.values)
plt.xticks(rotation=90)
plt.xlabel('Drug Regimen')
plt.ylabel('Number of Mice')
plt.show()


# In[78]:


# Generate a pie chart, using Pandas, showing the distribution of unique female versus male mice used in the study
counts = clean_study_data_complete.Sex.value_counts()
counts.plot(kind='pie', autopct = '%1.1f%%')

# Get the unique mice with their gender



# Make the pie chart


# In[102]:


# Generate a pie chart, using pyplot, showing the distribution of unique female versus male mice used in the study

counts = clean_study_data_complete.Sex.value_counts()
plt.pie(counts.values, labels=counts.index.values, autopct='%1.1f%%')
plt.title('distribution of unique female versus male mice')
plt.ylabel('sex')
plt.show()

# Get the unique mice with their gender


# Make the pie chart


# ## Quartiles, Outliers and Boxplots

# In[84]:


# Calculate the final tumor volume of each mouse across four of the treatment regimens:
# Capomulin, Ramicane, Infubinol, and Ceftamin

# Start by getting the last (greatest) timepoint for each mouse
max_tumor = clean_study_data_complete.groupby(['Mouse ID'])['Timepoint'].max()
max_tumor = max_tumor.reset_index()


# Merge this group df with the original DataFrame to get the tumor volume at the last timepoint
merged_data = max_tumor.merge(clean_study_data_complete,on=['Mouse ID','Timepoint'],how='left')
merged_data


# In[86]:


#print(merged_data['Mouse ID'].dtype)
#df['column_name'] = df['column_name'].astype(float)
#merged_data['Mouse ID'] = merged_data['Mouse ID'].astype(float)


# In[88]:


# Put treatments into a list for for loop (and later for plot labels)
treatment_list = ['Capomulin','Ramicane','Infubinol','Ceftamin']

# Create empty list to fill with tumor vol data (for plotting)

tumor_vol_list = []
# Calculate the IQR and quantitatively determine if there are any potential outliers.
for drug in treatment_list:

    # Locate the rows which contain mice on each drug and get the tumor volumes
    final_tumor_vol =  merged_data.loc[merged_data['Drug Regimen'] ==drug, 'Tumor Volume (mm3)']

    # add subset
    tumor_vol_list.append(final_tumor_vol) 

    # Determine outliers using upper and lower bounds
    quartiles = final_tumor_vol.quantile([.25, .5, .75])
    lowerq = quartiles[0.25]
    upperq = quartiles[0.75] 
    iqr = upperq-lowerq
    lower_bound = lowerq - (1.5 * iqr) 
    upper_bound = upperq + (1.5 * iqr)

    outliers = final_tumor_vol.loc[(final_tumor_vol < lower_bound) | (final_tumor_vol > upper_bound)]
    print(f"{drug}'s potential outliers{outliers}") 


# In[100]:


# Generate a box plot that shows the distribution of the tumor volume for each treatment group.

orange_out = dict(markerfacecolor = 'r',markersize = 20)
plt.boxplot(tumor_vol_list, labels = treatment_list, flierprops = orange_out)
plt.title('distribution of the tumor volume')
plt.ylabel('final tumor vol (mm3)')
plt.show()



# ## Line and Scatter Plots

# In[93]:


# Generate a line plot of tumor volume vs. time point for a single mouse treated with Capomulin

capomulin_table = clean_study_data_complete[clean_study_data_complete['Drug Regimen'] == 'Capomulin']
mousedata = capomulin_table[capomulin_table['Mouse ID']=='l509']
plt.plot(mousedata['Timepoint'], mousedata['Tumor Volume (mm3)'])
plt.title('Capomulin treatment of mouse l509')
plt.xlabel('Timeplot')
plt.ylabel('Tumor vol(mm3)')
plt.show()


# In[98]:


# Generate a scatter plot of mouse weight vs. the average observed tumor volume for the entire Capomulin regimen

capomulin_table = clean_study_data_complete[clean_study_data_complete['Drug Regimen'] == 'Capomulin']
capomulin_average = capomulin_table.groupby(["Mouse ID"])[['Tumor Volume (mm3)','Weight (g)']].mean()

plt.scatter(capomulin_average['Weight (g)'], capomulin_average['Tumor Volume (mm3)'])
plt.xlabel('Weight (g)')
plt.ylabel('Average Tumor Volume (mm3)')
plt.title(' mouse weight vs. the average observed tumor volume for Capomulin regimen')
plt.show()


#print(capomulin_average['Mouse ID'].dtype)


# ## Correlation and Regression

# In[27]:


# Calculate the correlation coefficient and a linear regression model
# for mouse weight and average observed tumor volume for the entire Capomulin regimen

corr = st.pearsonr(capomulin_average['Weight (g)'], capomulin_average['Tumor Volume (mm3)']) 
print(f"The correlation between mouse weight and the average tumor volume is {round(corr[0],2)}")

model = st.linregress(capomulin_average['Weight (g)'], capomulin_average['Tumor Volume (mm3)'])
slope = model[0]
b = model[1]

y_values = capomulin_average['Weight (g)'] * slope + b
plt.scatter(capomulin_average['Weight (g)'], capomulin_average['Tumor Volume (mm3)'])
plt.plot(capomulin_average['Weight (g)'],y_values, color = 'r',alpha=0.5)
plt.xlabel('Weight (g)')
plt.ylabel('Average tumor volume (mm3)')
plt.show()


# In[ ]:





# In[ ]:




