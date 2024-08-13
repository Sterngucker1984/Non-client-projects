#!/usr/bin/env python
# coding: utf-8

# In[18]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# In[46]:


pwd


# In[47]:


df_film = pd.read_csv('fandango_scrape.csv')


# In[48]:


df_film.head(3)


# In[49]:


df_film.info()


# In[50]:


df_film.describe().transpose()


# In[51]:


df_film.shape


# In[52]:


df_film.columns


# In[58]:


(df_film ['VOTES']==0).sum()


# In[ ]:


#Removing movies with no votes


# In[63]:


df_film = df_film [df_film ['VOTES']>0]


# In[117]:


plt.figure(figsize = (10,4), dpi = 200)
plt.title('RATING vs VOTES')
sns.scatterplot(data = df_film ,x = 'RATING', y ='VOTES', color = 'red', alpha = 0.5)


# In[129]:


plt.figure(figsize = (6,3), dpi = 100)
sns.heatmap(df_film.corr(), annot = True, cmap = 'viridis', lw = 1)


# In[180]:


df_film ['FILM'][0].split('(')[-1].replace(')','')


# In[181]:


df_film ['YEAR'] = df_film ['FILM'].apply(lambda x: x.split('(')[-1].replace(')',''))


# In[169]:


df_film.columns


# In[174]:


#df_film. drop('YEAR', axis = 1)


# In[182]:


df_film.head(3)


# In[ ]:


#Number of movies by year


# In[183]:


df_film ["YEAR"].value_counts()


# In[185]:


df_film.head()


# In[207]:


orderY = list(df_film .sort_values('YEAR')['YEAR'].unique())


# In[218]:


sns.set_style('dark')
plt.figure(figsize = (8,4), dpi = 200)
sns.countplot(data = df_film, x = "YEAR" , palette = "Set2",order= orderY)
plt.ylabel ('Number of movies by year', fontsize = 10)
plt.xlabel ('Year', fontsize = 10)
plt.title ('Number of films by year')


# In[219]:


#Defining the most popular films


# In[220]:


df_film.nlargest(5,"VOTES")[["FILM",'VOTES']]


# In[255]:


plt.figure (figsize = (10,4), dpi = 200)
sns.kdeplot(data = df_film, x = 'RATING', clip = [0, 5], shade = True, alpha = 0.2, label = 'True Rating', color = 'green' )
sns.kdeplot(data = df_film, x = 'STARS', clip = [0, 5], shade = True, alpha = 0.1, label = 'Stars Displayed', color = 'red' )
plt.legend(loc= [1.02,0.5],fontsize = 12)
plt.xlabel('Rating / Stars', fontsize = 12)
plt.ylabel('Density', fontsize = 12)
plt.title ('True Rating vs Stars Displayed', fontsize = 15)
plt.show()


# In[256]:


df_film.columns


# In[ ]:


#Calculating the difference between Stars Displayed and True Rating


# In[257]:


df_film ['STARS_DIFF'] = round(df_film ['STARS'] - df_film ['RATING'],2)


# In[258]:


df_film


# In[263]:


df_film['STARS_DIFF'].value_counts()


# In[271]:


plt.figure (figsize = (10,4), dpi = 200)
sns.countplot(data = df_film , x = 'STARS_DIFF', palette = 'magma', alpha = 0.7)
plt.show()


# In[274]:


df_film [df_film ['STARS_DIFF'] == df_film ['STARS_DIFF'].max()]


# In[289]:


No_Diff = len (df_film [df_film ['STARS_DIFF'] ==0])


# In[290]:


Small_Diff = len (df_film [df_film ['STARS_DIFF'].between (0.1,0.5)])


# In[291]:


Big_Diff = len (df_film [df_film ['STARS_DIFF'].between (0.5,df_film ['STARS_DIFF'].max())])


# In[296]:


difference_table = pd.Series(data = [No_Diff,Small_Diff,Big_Diff], index = ['Diff = 0','0 < Diff <0.5', '0.5 > Diff >= 1.0' ])


# In[297]:


difference_table


# In[ ]:


#Read the data from the second source


# In[298]:


all_sites_score = pd.read_csv('all_sites_scores.csv')


# In[299]:


all_sites_score.head()


# In[300]:


all_sites_score.info()


# In[301]:


#Exploring the relationship between RT Critic reviews and RT User reviews


# In[303]:


all_sites_score.columns


# In[313]:


plt.figure (figsize = (6,4), dpi = 150)
sns.scatterplot(data = all_sites_score, x = 'RottenTomatoes', y = 'RottenTomatoes_User' )
plt.xlim(0,100)
plt.ylim(0,100)
plt.title('Relationship between RT Critic reviews and RT User reviews', fontsize = 10)
plt.show()


# In[314]:


#New column based off the difference between critics ratings and users ratings for Rotten Tomatoes


# In[315]:


all_sites_score ['Diff_RT'] = all_sites_score ['RottenTomatoes'] - all_sites_score ['RottenTomatoes_User']


# In[320]:


all_sites_score.head(3)


# In[321]:


#Mean Absolute Difference between RT scores and RT User scores


# In[322]:


mad = all_sites_score ['Diff_RT'].apply(abs)


# In[332]:


np.round(mad.mean(),2)


# In[333]:


#Distribution of the differences between RT Critics Score and RT User Score


# In[344]:


plt.figure (figsize = (6,3), dpi = 150)
sns.histplot(data = all_sites_score, x = 'Diff_RT', bins = 25, kde = True, color = '#25DB6A')
plt.show()


# In[345]:


#Distribution showing the absolute value difference between Critics and Users on Rotten Tomatoes


# In[348]:


#mad = all_sites_score ['Diff_RT'].apply(abs)


# In[354]:


plt.figure (figsize = (6,3), dpi = 150)
sns.histplot(data = all_sites_score, x = mad, bins = 25, kde = True, color = '#25DB6A')
plt.xlabel('Diff_abs_RT')
plt.show()


# In[355]:


# Top 5 movies users rated higher than critics on average


# In[358]:


all_sites_score.nsmallest(5, 'Diff_RT')[['FILM','Diff_RT']]


# In[359]:


# Top 5 movies critics rated higher than users on average


# In[360]:


all_sites_score.nlargest(5, 'Diff_RT')[['FILM','Diff_RT']]


# In[361]:


#Metacritic Rating versus the Metacritic User rating


# In[377]:


sns.set_style('ticks')
plt.figure (figsize = (6,4), dpi = 150)
sns.scatterplot(data = all_sites_score, x = 'Metacritic', y = 'Metacritic_User', s = 50 )
plt.xlim(0,100)
plt.ylim(0,10)
plt.title('Metacritic Rating versus the Metacritic User rating', fontsize = 10)
plt.show()


# In[378]:


#Relationship between vote counts on MetaCritic versus vote counts on IMDB


# In[379]:


all_sites_score.columns


# In[386]:


sns.set_style('ticks')
plt.figure (figsize = (8,4), dpi = 150)
sns.scatterplot(data = all_sites_score, x = 'Metacritic_user_vote_count', y = 'IMDB_user_vote_count', s = 50 )
plt.title('Vote counts on MetaCritic vs Vote counts on IMDB', fontsize = 12)
plt.tight_layout()
plt.show()


# In[387]:


#Outliers


# In[395]:


#Outlier 1
all_sites_score [all_sites_score ['IMDB_user_vote_count'] == all_sites_score ['IMDB_user_vote_count'].max()][['FILM','Metacritic_user_vote_count','IMDB_user_vote_count']]


# In[398]:


#Outlier 2
all_sites_score [all_sites_score ['Metacritic_user_vote_count'] == all_sites_score ['Metacritic_user_vote_count'].max()][['FILM','Metacritic_user_vote_count','IMDB_user_vote_count']]


# In[399]:


#Combining the Fandango Table with the All Sites table
df = pd.merge(left = df_film, right = all_sites_score, left_on = 'FILM', right_on = 'FILM', how = 'inner' )


# In[401]:


df.head()


# In[402]:


df.info()


# In[408]:


df.describe().transpose()['max']


# In[ ]:


#Normalization all rating columns so that they match within the 0-5 star range shown on Fandango


# In[411]:


df['RottenTomatoes_Norm'] = np.round(df['RottenTomatoes'] / 20,1)

df['RottenTomatoes_User_Norm'] = np.round(df['RottenTomatoes_User'] / 20,1)
df['Metacritic_Norm'] = np.round(df['Metacritic'] / 20,1)


# In[412]:


df['Metacritic_User_Norm'] = np.round(df['Metacritic_User'] / 2,1)


# In[413]:


df['IMDB_Norm'] = np.round(df['IMDB'] / 2,1)


# In[416]:


df.columns


# In[417]:


norm_scores = df[['FILM','STARS','RottenTomatoes_Norm',
       'RottenTomatoes_User_Norm', 'Metacritic_Norm', 'Metacritic_User_Norm',
       'IMDB_Norm']]


# In[420]:


#norm_scores DataFrame contains only  the normalizes ratings
norm_scores.head()


# In[429]:


def move_legend(ax, new_loc, **kws):
    old_legend = ax.legend_
    handles = old_legend.legendHandles
    labels = [t.get_text() for t in old_legend.get_texts()]
    title = old_legend.get_title().get_text()
    ax.legend(handles, labels, loc=new_loc, title=title, **kws)


# In[434]:


fig, ax = plt.subplots(figsize = (8,4), dpi = 200)
sns.kdeplot(data = norm_scores, clip = (0,5), shade = True, palette = 'Set1', alpha = 0.2)
move_legend(ax, "upper left")
plt.title('STARS vs All Ratings')


# In[439]:


fig, ax = plt.subplots(figsize = (8,4), dpi = 200)
sns.kdeplot(data = norm_scores[['RottenTomatoes_Norm', 'STARS']], clip = (0,5), shade = True, palette = 'Set1', alpha = 0.2)
move_legend(ax, "upper left")
plt.title('STARS vs RT_Norm')
plt.show()


# In[451]:


#The worst films


# In[452]:


norm_scores.columns


# In[458]:


norm_scores_w_film = norm_scores.drop('FILM', axis = 1)


# In[461]:


norm_scores_w_film.head(3)


# In[468]:


plt.figure (figsize = (8,5), dpi = 180)
sns.clustermap(data = norm_scores_w_film,cmap = 'magma', col_cluster = False)
plt.show()


# In[469]:


#The worst films
worst_films = norm_scores.nsmallest(10,'RottenTomatoes_Norm')


# In[478]:


fig, ax = plt.subplots(figsize = (8,4), dpi = 200)
sns.kdeplot(data = worst_films, clip = (0,5), shade = True, palette = 'Set1', alpha = 0.2)
move_legend(ax, "upper right")
plt.title('STARS vs All Ratings for the 10 worst films')
plt.show()


# In[480]:


worst_films.head()


# In[485]:


worst_films_copy = worst_films.copy()


# In[488]:


worst_films_copy['Average Total Score'] = ((worst_films_copy ['RottenTomatoes_Norm'] + worst_films_copy ['RottenTomatoes_User_Norm'] + worst_films_copy ['Metacritic_Norm'] + worst_films_copy ['Metacritic_User_Norm'] + worst_films_copy ['IMDB_Norm'])/5)


# In[495]:


#The 5 worst films
worst_films_copy.nsmallest(5,'Average Total Score')[['FILM','STARS','Average Total Score']]

