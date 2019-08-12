import matplotlib
import numpy as np
import pandas as pd


energy = pd.read_excel('Energy Indicators.xls', header=17, skipfooter=38, usecols="C:F",
                           names=['Country', 'Energy Supply', 'Energy Supply per Capita', '% Renewable'])
energy['Energy Supply'] = energy['Energy Supply'].replace(["..."], np.nan)
energy['Energy Supply per Capita'] = energy['Energy Supply per Capita'].replace(["..."], np.nan)
energy['% Renewable'] = energy['% Renewable'].replace(["..."], np.nan)
energy['Energy Supply'] = energy['Energy Supply'].apply(lambda x: x*1000000)
replace_name = {"Republic of Korea": "South Korea",
                  "United States of America": "United States",
                  "United Kingdom of Great Britain and Northern Ireland": "United Kingdom",
                  "China, Hong Kong Special Administrative Region": "Hong Kong"}
energy['Country'] = energy['Country'].replace(replace_name, regex=True)
energy['Country'] = energy['Country'].str.replace(r"\(.*\)","").str.strip()
energy['Country'] = energy['Country'].str.replace(r"\d+","").str.strip()
energy = energy.set_index('Country')


#usecols = [*range(0,4), *range(50,60)]
GDP = pd.read_csv('world_bank.csv', skiprows=4) #, usecols=usecols#
newcountries = {"Korea, Rep.": "South Korea",
                "Iran, Islamic Rep.": "Iran",
                "Hong Kong SAR, China": "Hong Kong"}
GDP['Country Name'] = GDP['Country Name'].replace(newcountries, regex=True)
GDP = GDP.set_index('Country Name')

ScimEn = pd.read_excel("scimagojr-3.xlsx")

firstdf = pd.merge(ScimEn, energy, how='outer', left_on='Country', right_index=True)
newdf = pd.merge(firstdf, GDP, how='outer', left_on='Country', right_index=True)
newdf = newdf.set_index(['Country'])
dropcols = [*range(10,59)]
newdf = newdf.drop(newdf.columns[dropcols], axis=1)
q1df = newdf.copy()
q1df = q1df[q1df['Rank'] <= 15]

'''
ScimEn = pd.read_excel("scimagojr-3.xlsx", nrows=15)
firstdf = pd.merge(ScimEn, energy, how='left', left_on='Country', right_index=True)
newdf = pd.merge(firstdf, GDP, how='left', left_on='Country', right_index=True)
newdf = newdf.set_index(['Country'])
newdf = newdf.drop(['Country Code', 'Indicator Name', 'Indicator Code'], axis=1)
'''

def answer_one():
    return print(q1df)

def answer_two():
    return print(len(newdf.index) - len(q1df.index))

def answer_three():
    col = q1df.loc[:,'2006':'2015']
    q1df['Average'] = col.mean(axis=1)
    avgGDP = q1df['Average']
    return print(avgGDP.sort_values(ascending=False))

def answer_four():
    avgGDP = q1df.sort_values('Average', ascending=False)
    avgsix = avgGDP.iloc[[5]]
    max = avgsix.loc[:,'2006':'2015'].max(axis=1)
    min = avgsix.loc[:,'2006':'2015'].min(axis=1)
    return print(int(max-min))

def answer_five():
    return print(q1df['Energy Supply per Capita'].mean())

def answer_six():
    q6country = q1df['% Renewable'].idxmax()
    q6df = q1df.loc[[q6country]]
    q6df = q6df['% Renewable']
    q6df = q6df.reset_index()
    return print(tuple(q6df.iloc[0]))

def answer_seven():
    q1df['citations ratio'] = q1df['Self-citations'] / q1df['Citations']
    q7country = q1df['citations ratio'].idxmax()
    q7df = q1df.loc[[q7country]]
    q7df = q7df['citations ratio']
    q7df = q7df.reset_index()
    return print(tuple(q7df.iloc[0]))

def answer_eight():
    q1df['est pop'] = q1df['Energy Supply'] / q1df['Energy Supply per Capita']
    q8df = q1df.sort_values('est pop', ascending=False)
    q8df = q8df.iloc[[2]]
    return print(str(q8df.head().index[0]))

def answer_nine():
    q1df['est cit per cap'] = q1df['est pop'] / q1df['Citations']
    return print(q1df['est cit per cap'].corr(q1df['Energy Supply per Capita']))


'''def plot9():
    import matplotlib as plt
   # %matplotlib inline

    Top15 = answer_one()
    Top15['PopEst'] = Top15['Energy Supply'] / Top15['Energy Supply per Capita']
    Top15['Citable docs per Capita'] = Top15['Citable documents'] / Top15['PopEst']
    Top15.plot(x='Citable docs per Capita', y='Energy Supply per Capita', kind='scatter', xlim=[0, 0.0006])
    plt.show()
plot9()'''

def answer_ten():
    q1df['renewbool'] = q1df['% Renewable'] >= q1df['% Renewable'].median(axis=0)
    HighRenew = q1df[q1df['renewbool'] == 1]
    HighRenew = HighRenew.sort_values('Rank', ascending=True)
    return HighRenew.iloc[:,0]

def answer_eleven():
    Top15 = answer_one()
    return "ANSWER"