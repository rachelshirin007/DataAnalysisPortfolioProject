from bs4 import BeautifulSoup
import requests
import pandas as pd

url = 'https://en.wikipedia.org/wiki/List_of_largest_companies_in_the_United_States_by_revenue'

page = requests.get(url)

soup = BeautifulSoup(page.text, 'html')

#print(soup.prettify()) #brings the entire hmtl of the page

#print(soup.find('table')) #prints a randon box of table at the beginning of the page

#print(soup.find_all('table')[1]) #prints the table

#print(soup.find('table', class_ = 'wikitable sortable')) #another way to print the table we want

table = soup.find_all('table')[1]

#print(table)

table_titles = table.find_all('th')

#print(table_titles)

world_table_titles = [title.text.strip() for title in table_titles]

#print(world_table_titles)

df = pd.DataFrame(columns= world_table_titles)

print(df)

column_data = table.find_all('tr')

for row in column_data[1:]:
    row_data = row.find_all('td')
    individual_row_data = [data.text.strip() for data in row_data]

    length = len(df)
    df.loc[length]=individual_row_data

print(df)

df.to_csv(r'C:\Users\kotav\OneDrive\Documents\Data Analysis Project\WebScraping.csv', index= False)
