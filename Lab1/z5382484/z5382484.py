#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# Third-party libraries
# NOTE: You may **only** use the following third-party libraries:
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd 
from thefuzz import fuzz
from thefuzz import process
# NOTE: It isn't necessary to use all of these to complete the assignment, 
# but you are free to do so, should you choose.

# Standard libraries
# NOTE: You may use **any** of the Python 3.11 or Python 3.12 standard libraries:
# https://docs.python.org/3.11/library/index.html
# https://docs.python.org/3.12/library/index.html
from pathlib import Path
# ... import your standard libraries here ...


######################################################
# NOTE: DO NOT MODIFY THE LINE BELOW ...
######################################################
studentid = Path(__file__).stem

######################################################
# NOTE: DO NOT MODIFY THE FUNCTION BELOW ...
######################################################
def log(question, output_df, other):
    print(f"--------------- {question}----------------")

    if other is not None:
        print(question, other)
    if output_df is not None:
        df = output_df.head(5).copy(True)
        for c in df.columns:
            df[c] = df[c].apply(lambda a: a[:20] if isinstance(a, str) else a)

        df.columns = [a[:10] + "..." for a in df.columns]
        print(df.to_string())


######################################################
# NOTE: YOU MAY ADD ANY HELPER FUNCTIONS BELOW ...
######################################################



######################################################
# QUESTIONS TO COMPLETE BELOW ...
######################################################

######################################################
# NOTE: DO NOT MODIFY THE FUNCTION SIGNATURE BELOW ...
######################################################
def question_1(jobs_csv):
    """Read the data science jobs CSV file into a DataFrame.

    See the assignment spec for more details.

    Args:
        jobs_csv (str): Path to the jobs CSV file.

    Returns:
        DataFrame: The jobs DataFrame.
    """

    ######################################################
    # TODO: Your code goes here ...
    ######################################################
    job_csv=Path(jobs_csv) #path

    df=pd.read_csv(job_csv)
    

    ######################################################
    # NOTE: DO NOT MODIFY THE CODE BELOW ...
    ######################################################
    log("QUESTION 1", output_df=df, other=df.shape)
    return df



######################################################
# NOTE: DO NOT MODIFY THE FUNCTION SIGNATURE BELOW ...
######################################################
def question_2(cost_csv, cost_url):
    """Read the cost of living CSV into a DataFrame.  If the CSV file does not 
    exist, scrape it from the specified URL and save it to the CSV file.

    See the assignment spec for more details.

    Args:
        cost_csv (str): Path to the cost of living CSV file.
        cost_url (str): URL of the cost of living page.

    Returns:
        DataFrame: The cost of living DataFrame.
    """

    ######################################################
    # TODO: Your code goes here ...
    ######################################################
    cost_csv_path = Path(cost_csv)
    # check the csv file is existd
    if cost_csv_path.exists():
        df = pd.read_csv(cost_csv)
    else:
        dfs = pd.read_html(cost_url)  
        df = dfs[0] #use the first table

        # Convert column names to lower case and replace spaces with underscores
        for col in df.columns:
            new_col = col.lower().replace(' ', '_')
            df.rename(columns={col: new_col}, inplace=True)

        # save DataFrame as CSV file
        df.to_csv(cost_csv, index=False)
    

    ######################################################
    # NOTE: DO NOT MODIFY THE CODE BELOW ...
    ######################################################
    log("QUESTION 2", output_df=df, other=df.shape)
    return df


######################################################
# NOTE: DO NOT MODIFY THE FUNCTION SIGNATURE BELOW ...
######################################################
def question_3(currency_csv, currency_url):
    """Read the currency conversion rates CSV into a DataFrame.  If the CSV 
    file does not exist, scrape it from the specified URL and save it to 
    the CSV file.

    See the assignment spec for more details.

    Args:
        cost_csv (str): Path to the currency conversion rates CSV file.
        cost_url (str): URL of the currency conversion rates page.

    Returns:
        DataFrame: The currency conversion rates DataFrame.
    """

    ######################################################
    # TODO: Your code goes here ...
    ######################################################
    currency_csv_path = Path(currency_csv)

    
    if currency_csv_path.exists():
       
        df = pd.read_csv(currency_csv)
    else:
       
        tables = pd.read_html(currency_url, header=[0, 1])
        df = tables[0]  

        # Remove all columns and header rows under "Nearest actual exchange rate"
        df = df.drop("Nearest actual exchange rate", axis=1, level=0)

        # Remove the top-level header row
        df.columns = df.columns.droplevel(0)

        # Replace non-breaking spaces in column names with spaces
        df.columns = df.columns.str.replace('\xa0', ' ')

        # Drop the '30 Jun 23' column
        df = df.drop(columns=['30 Jun 23'])

        # Rename the '31 Dec 23' column to 'rate'
        df = df.rename(columns={'31 Dec 23': 'rate'})

        # Convert all column names to lowercase
        df.columns = df.columns.str.lower()

        # Replace non-breaking spaces in the 'country' and 'currency' columns with spaces
        df['country'] = df['country'].str.replace('\xa0', ' ')
        df['currency'] = df['currency'].str.replace('\xa0', ' ')

       
        df.to_csv(currency_csv, index=False)
    

    ######################################################
    # NOTE: DO NOT MODIFY THE CODE BELOW ...
    ######################################################
    log("QUESTION 3", output_df=df, other=df.shape)
    return df


######################################################
# NOTE: DO NOT MODIFY THE FUNCTION SIGNATURE BELOW ...
######################################################
def question_4(country_csv, country_url):
    """Read the country codes CSV into a DataFrame.  If the CSV file does not 
    exist, it will be scrape the data from the specified URL and save it to the 
    CSV file.

    See the assignment spec for more details.

    Args:
        cost_csv (str): Path to the country codes CSV file.
        cost_url (str): URL of the country codes page.

    Returns:
        DataFrame: The country codes DataFrame.
    """

    ######################################################
    # TODO: Your code goes here ...
    ######################################################

    country_csv_path = Path(country_csv)

   
    if country_csv_path.exists():
        
        df = pd.read_csv(country_csv)
    else:
        
        df = pd.read_html(country_url)[0]  

        
        df = df.drop(columns=['Year', 'ccTLD', 'Notes'])

        # rename columns
        df = df.rename(columns={'Country name (using title case)': 'country', 'Code': 'code'})

        
        df.to_csv(country_csv, index=False)

    ######################################################
    # NOTE: DO NOT MODIFY THE CODE BELOW ...
    ######################################################
    log("QUESTION 4", output_df=df, other=df.shape)
    return df


######################################################
# NOTE: DO NOT MODIFY THE FUNCTION SIGNATURE BELOW ...
######################################################
def question_5(jobs_df):
    """Summarise some dimensions of the jobs DataFrame.

    See the assignment spec for more details.

    Args:
        jobs_df (DataFrame): The jobs DataFrame returned in question 1.

    Returns:
        DataFrame: The summary DataFrame.
    """

    ######################################################
    # TODO: Your code goes here ...
    ######################################################

    observations = jobs_df.count()
    distinct = jobs_df.nunique()
    missing = jobs_df.isnull().sum()

    # create new DataFrame
    df = pd.DataFrame({'observations': observations, 'distinct': distinct, 'missing': missing})


    ######################################################
    # NOTE: DO NOT MODIFY THE CODE BELOW ...
    ######################################################
    log("QUESTION 5", output_df=df, other=df.shape)
    return df


######################################################
# NOTE: DO NOT MODIFY THE FUNCTION SIGNATURE BELOW ...
######################################################
def question_6(jobs_df):
    """Add an experience rating column to the jobs DataFrame.

    See the assignment spec for more details.

    Args:
        jobs_df (DataFrame): The jobs DataFrame returned in question 1.

    Returns:
        DataFrame: The jobs DataFrame with the experience rating column added.
    """

    ######################################################
    # TODO: Your code goes here ...
    ######################################################

    experience_rating_map = {'EN': 1, 'MI': 2, 'SE': 3, 'EX': 4}

    jobs_df['experience_rating'] = jobs_df['experience_level'].map(experience_rating_map)
    df = jobs_df
    ######################################################
    # NOTE: DO NOT MODIFY THE CODE BELOW ...
    ######################################################
    log("QUESTION 6", output_df=df, other=df.shape)
    return df


######################################################
# NOTE: DO NOT MODIFY THE FUNCTION SIGNATURE BELOW ...
######################################################
def question_7(jobs_df, country_df):
    """Merge the jobs and country codes DataFrames.

    See the assignment spec for more details.

    Args:
        jobs_df (DataFrame): The jobs DataFrame returned in question 6.
        country_df (DataFrame): The country codes DataFrame returned in 
                                question 4.

    Returns:
        DataFrame: The merged DataFrame.
    """

    ######################################################
    # TODO: Your code goes here ...
    ######################################################

    country_df = country_df.rename(columns={'code': 'employee_residence'})

    # Merge jobs_df and country_df based on 'employee_residence' column
    merged_df = jobs_df.merge(country_df, on='employee_residence', how='left')

    df=merged_df

    ######################################################
    # NOTE: DO NOT MODIFY THE CODE BELOW ...
    ######################################################
    log("QUESTION 7", output_df=df, other=df.shape)
    return df


######################################################
# NOTE: DO NOT MODIFY THE FUNCTION SIGNATURE BELOW ...
######################################################
def question_8(jobs_df, currency_df):
    """Add an Australian dollar salary column to the jobs DataFrame.

    See the assignment spec for more details.

    Args:
        jobs_df (DataFrame): The jobs DataFrame returned in question 7.
        currency_df (DataFrame): The currency conversion rates DataFrame 
                                 returned in question 3.

    Returns:
        DataFrame: The jobs DataFrame with the Australian dollar salary column
                   added.
    """

    ######################################################
    # TODO: Your code goes here ...
    ######################################################

    # Check if currency_df contains "United States" value
    is_usd = currency_df['country'].str.contains('United States', case=False)

    # Create a new DataFrame based on is_usd, keeping only the rows containing "United States" value
    usd_df = currency_df[is_usd]

    # Select the first value in the "rate" column as the exchange rate for USD to AUD
    rate = float(usd_df['rate'].iloc[0])

    # Select relevant data for the year 2023
    jobs_2023_df = jobs_df[jobs_df['work_year'] == 2023]

    # Add a column "salary_in_aud" and calculate the salary in Australian dollars

    jobs_2023_df['salary_in_aud'] = rate * jobs_2023_df['salary_in_usd']

    df =  jobs_2023_df
    ######################################################
    # NOTE: DO NOT MODIFY THE CODE BELOW ...
    ######################################################
    log("QUESTION 8", output_df=df, other=df.shape)
    return df


######################################################
# NOTE: DO NOT MODIFY THE FUNCTION SIGNATURE BELOW ...
######################################################
def question_9(cost_df):
    """Re-scale the cost of living DataFrame to be relative to Australia.

    See the assignment spec for more details.

    Args:
        cost_df (DataFrame): The cost of living DataFrame returned in question 2.

    Returns:
        DataFrame: The re-scaled cost of living DataFrame.
    """

    ######################################################
    # TODO: Your code goes here ...
    ######################################################

    new_df = cost_df[['country', 'cost_of_living_plus_rent_index']].copy()

    # 2. find Australia's cost_of_living_plus_rent_index
    index = cost_df.loc[cost_df['country'] == 'Australia', 'cost_of_living_plus_rent_index'].iloc[0]

    
    new_df.loc[:, 'cost_of_living_plus_rent_index'] = new_df['cost_of_living_plus_rent_index'] / index * 100

    
    new_df.loc[:, 'cost_of_living_plus_rent_index'] = new_df['cost_of_living_plus_rent_index'].round(1)

    # sort by increasing
    df = new_df.sort_values('cost_of_living_plus_rent_index')

    
    ######################################################
    # NOTE: DO NOT MODIFY THE CODE BELOW ...
    ######################################################
    log("QUESTION 9", output_df=df, other=df.shape)
    return df


######################################################
# NOTE: DO NOT MODIFY THE FUNCTION SIGNATURE BELOW ...
######################################################
def question_10(jobs_df, cost_df):
    """Merge the jobs and cost of living DataFrames.

    See the assignment spec for more details.

    Args:
        jobs_df (DataFrame): The jobs DataFrame returned in question 8.
        cost_df (DataFrame): The cost of living DataFrame returned in question 9.

    Returns:
        DataFrame: The merged DataFrame.
    """

    ######################################################
    # TODO: Your code goes here ...
    ######################################################

    
    cost_of_living_list = []

    # For each country in jobs_df, perform fuzzy matching to find the best matching country in cost_df
    for country in jobs_df['country']:
        match = process.extractOne(country, cost_df['country'])
        if match[1] >= 90:  
            # If a matching country is found, retrieve the corresponding cost of living index
            cost_of_living = cost_df.loc[cost_df['country'] == match[0], 'cost_of_living_plus_rent_index'].iloc[0]
            cost_of_living_list.append(cost_of_living)
        else:
            # If no matching country is found, add a None value
            cost_of_living_list.append(None)

    # Add the matched cost of living index list as a new column to jobs_df
    jobs_df.loc[:, 'cost_of_living'] = cost_of_living_list

    # Remove rows where cost_of_living is empty
    jobs_df_copy = jobs_df.copy()
    jobs_df_copy.dropna(subset=['cost_of_living'], inplace=True)

    merged_df = jobs_df_copy.dropna(subset=['cost_of_living'])


    df = merged_df
    ######################################################
    # NOTE: DO NOT MODIFY THE CODE BELOW ...
    ######################################################
    log("QUESTION 10", output_df=df, other=df.shape)
    return df


######################################################
# NOTE: DO NOT MODIFY THE FUNCTION SIGNATURE BELOW ...
######################################################
def question_11(jobs_df):
    """Create a pivot table of the average salary in AUD by country and 
    experience rating.

    See the assignment spec for more details.

    Args:
        jobs_df (DataFrame): The jobs DataFrame returned in question 10.

    Returns:
        DataFrame: The pivot table.
    """

    ######################################################
    # TODO: Your code goes here ...
    ######################################################
    pivot_table = pd.pivot_table(jobs_df, 
                                 index='country', 
                                 columns='experience_rating', 
                                 values='salary_in_aud', 
                                 aggfunc='mean', 
                                 fill_value=0)
    
    pivot_table = pivot_table.astype(int)

    list = pivot_table.columns.sort_values().tolist()

    pivot_table = pivot_table.sort_values(list, ascending=False)
    
    # pivot_table = pivot_table[[1, 2, 3, 4]]
    # Rename the columns
    pivot_table.columns = [('salary_in_aud', 1), ('salary_in_aud', 2), ('salary_in_aud', 3), ('salary_in_aud', 4)]
    
    df = pivot_table
    
    ######################################################
    # NOTE: DO NOT MODIFY THE CODE BELOW ...
    ######################################################
    log("QUESTION 11", output_df=None, other=df)
    return df


######################################################
# NOTE: DO NOT MODIFY THE FUNCTION SIGNATURE BELOW ...
######################################################
def question_12(jobs_df):
    """Create a visualisation of data science jobs to help inform a decision
    about where to live, based (minimally) on salary and cost of living.

    See the assignment spec for more details.

    Args:
        jobs_df (DataFrame): The jobs DataFrame returned in question 10.
    """

    ######################################################
    # TODO: Your code goes here ...
    ######################################################

    sorted_countries_df = jobs_df.sort_values(by='salary_in_aud', ascending=False)

    unique_jobs_df = sorted_countries_df.drop_duplicates(subset=['country'])

    # Selecting the top 10 unique countries
    top_10_df = unique_jobs_df.head(10)

    new_10_df = top_10_df[['country', 'job_title', 'salary_in_aud', 'cost_of_living']].copy()

    def color_mapping(index):
        if index < 60:
            return '#add8e6'  # Light Blue
        elif 60 <= index < 70:
            return '#87ceeb'  # Medium Light Blue
        elif 70 <= index < 80:
            return '#6495ed'  # Medium Blue
        elif 80 <= index < 90:
            return '#4169e1'  # Medium Deep Blue
        elif 90 <= index < 100:
            return '#0000ff'  # Deep Blue
        else:
            return '#00008b'  # Darker Blue

    # Plotting the Bar Chart
    plt.figure(figsize=(10, 6)) 
    for i, row in new_10_df.iterrows():
        color = color_mapping(row['cost_of_living'])
        plt.barh(row['country'] + ' - ' + row['job_title'], row['salary_in_aud'], color=color)

    # Adding the cost_of_living legend
    legend_handles = [plt.Rectangle((0,0),1,1, color=color_mapping(i)) for i in range(60, 111, 10)]
    plt.legend(legend_handles, ['0-60', '60-70', '70-80', '80-90', '90-100', '100-110'], title='Cost of Living')

    # Setting axis labels and title
    plt.xlabel('Salary in AUD')
    plt.title('Top 10 Countries for Data-Related Job Salaries and Cost of Living Analysis')

    # Setting x-axis ticks range and rotation
    plt.xticks(np.arange(80000, 285000, 20000), rotation=45, ha='right')

    # Setting y-axis ticks range and rotation

    plt.yticks(ticks=np.arange(len(new_10_df)), labels=new_10_df['country'] + ' - ' + new_10_df['job_title'], rotation=45, ha='right')

    ######################################################
    # NOTE: DO NOT MODIFY THE CODE BELOW ...
    ######################################################
    plt.savefig(f"{studentid}-Q12.png")


######################################################
# NOTE: DO NOT MODIFY THE MAIN FUNCTION BELOW ...
######################################################
if __name__ == "__main__":
    # data ingestion and cleaning
    df1 = question_1("ds_jobs.csv")
    df2 = question_2("cost_of_living.csv", 
                     "https://www.cse.unsw.edu.au/~cs9321/24T1/ass1/cost_of_living.html")
    df3 = question_3("exchange_rates.csv", 
                     "https://www.cse.unsw.edu.au/~cs9321/24T1/ass1/exchange_rates.html")
    df4 = question_4("country_codes.csv", 
                     "https://www.cse.unsw.edu.au/~cs9321/24T1/ass1/country_codes.html")

    # data exploration
    df5 = question_5(df1.copy(True))

    # data manipulation
    df6 = question_6(df1.copy(True))
    df7 = question_7(df6.copy(True), df4.copy(True))
    df8 = question_8(df7.copy(True), df3.copy(True))
    df9 = question_9(df2.copy(True))
    df10 = question_10(df8.copy(True), df9.copy(True))
    df11 = question_11(df10.copy(True))

    # data visualisation
    question_12(df10.copy(True))
