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
answer_one()

def answer_two():
    return print(len(newdf.index) - len(q1df.index))
answer_two()

def answer_three():
    col = q1df.loc[:,'2006':'2015']
    q1df['Average'] = col.mean(axis=1)
    avgGDP = q1df['Average']
    return print(avgGDP.sort_values(ascending=False))
answer_three()

def answer_four():
    avgGDP = q1df.sort_values('Average', ascending=False)
    avgsix = avgGDP.iloc[[5]]
    max = avgsix.loc[:,'2006':'2015'].max(axis=1)
    min = avgsix.loc[:,'2006':'2015'].min(axis=1)
    return print(int(max-min))
answer_four()

def answer_five():
    return print(q1df['Energy Supply per Capita'].mean())
answer_five()

def answer_six():
    Top15 = answer_one()
    return "ANSWER"
answer_six()