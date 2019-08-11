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


usecols = [*range(0,4), *range(50,60)]
GDP = pd.read_csv('world_bank.csv', skiprows=4, usecols=usecols)
newcountries = {"Korea, Rep.": "South Korea",
                "Iran, Islamic Rep.": "Iran",
                "Hong Kong SAR, China": "Hong Kong"}
GDP['Country Name'] = GDP['Country Name'].replace(newcountries, regex=True)
GDP = GDP.set_index('Country Name')

ScimEn = pd.read_excel("scimagojr-3.xlsx", nrows=15)

#firstdf = pd.merge(energy, GDP, how='outer', left_index=True, right_index=True)
#newdf = pd.merge(firstdf, ScimEn, how='outer', left_index=True, right_on="Country")