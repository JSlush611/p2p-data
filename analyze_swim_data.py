import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from util import save_fig, calculate_percentile

df = pd.read_csv('swim_results.csv')

# Convert RaceDate to datetime
df['RaceDate'] = pd.to_datetime(df['RaceDate'])

# Extract year from RaceDate for analysis
df['Year'] = df['RaceDate'].dt.year


# 1. Overall Participation Over the Years
def plot_participation_over_years(df):
    participation = df.groupby('Year')['Name'].count()
    fig, ax = plt.subplots()
    participation.plot(kind='bar', ax=ax)
    ax.set_title('Overall Participation Over the Years')
    ax.set_xlabel('Year')
    ax.set_ylabel('Number of Participants')
    save_fig(fig, 'participation_over_years.png')


# 2. Average Pace Over the Years
def plot_average_pace_over_years(df):
    avg_pace = df.groupby('Year')['Pace (min/mi)'].mean()
    fig, ax = plt.subplots()
    avg_pace.plot(ax=ax)
    ax.set_title('Average Pace Over the Years')
    ax.set_xlabel('Year')
    ax.set_ylabel('Average Pace (min/mi)')
    save_fig(fig, 'average_pace_over_years.png')


# 3. Participation by Age Group
def plot_participation_by_age_group(df):
    bins = [0, 18, 30, 40, 50, 60, 70, 80]
    labels = ['<18', '18-29', '30-39', '40-49', '50-59', '60-69', '70+']
    df['AgeGroup'] = pd.cut(df['Age'], bins=bins, labels=labels, right=False)
    fig, ax = plt.subplots()
    df['AgeGroup'].value_counts(sort=False).plot(kind='bar', ax=ax)
    ax.set_title('Participation by Age Group')
    ax.set_xlabel('Age Group')
    ax.set_ylabel('Number of Participants')
    save_fig(fig, 'participation_by_age_group.png')


# 4. Regional Participation
def plot_regional_participation(df):
    top_regions = df['Region'].value_counts().head(10)
    fig, ax = plt.subplots()
    top_regions.plot(kind='bar', ax=ax)
    ax.set_title('Top 10 Regions by Participation')
    ax.set_xlabel('Region')
    ax.set_ylabel('Number of Participants')
    save_fig(fig, 'regional_participation.png')


# 5. Pace Percentiles
def plot_pace_percentiles(df):
    percentiles = df['Pace (min/mi)'].quantile([0.25, 0.5, 0.75])
    fig, ax = plt.subplots()
    percentiles.plot(kind='bar', ax=ax)
    ax.set_title('Pace Percentiles')
    ax.set_xlabel('Percentile')
    ax.set_ylabel('Pace (min/mi)')
    save_fig(fig, 'pace_percentiles.png')


# 6. Gender Distribution Over the Years
def plot_gender_distribution(df):
    gender_distribution = df.groupby('Year')['Gender'].value_counts().unstack().fillna(0)
    fig, ax = plt.subplots()
    gender_distribution.plot(kind='bar', stacked=True, ax=ax)
    ax.set_title('Gender Distribution Over the Years')
    ax.set_xlabel('Year')
    ax.set_ylabel('Number of Participants')
    save_fig(fig, 'gender_distribution_over_years.png')


# 7. Top 10 Fastest Swimmers
def plot_top_10_fastest_swimmers(df):
    top_10_fastest = df.nsmallest(10, 'Pace (min/mi)')
    fig, ax = plt.subplots()
    top_10_fastest.plot(kind='bar', x='Name', y='Pace (min/mi)', ax=ax)
    ax.set_title('Top 10 Fastest Swimmers')
    ax.set_xlabel('Swimmer')
    ax.set_ylabel('Pace (min/mi)')
    save_fig(fig, 'top_10_fastest_swimmers.png')


# 8. Plot specific persons pace
def plot_specific_person_pace(df, name):
    dad_data = df[df['Name'] == name]

    if dad_data.empty:
        print(f"No data found for {name}")

        return

    fig, ax = plt.subplots()
    dad_data.plot(kind='line', x='Year', y='Pace (min/mi)', marker='o', ax=ax)
    ax.set_title(f"{name}'s Pace Over the Years")
    ax.set_xlabel('Year')
    ax.set_ylabel('Pace (min/mi)')

    filename = f"{name}_pace_over_years.png"
    save_fig(fig, filename)


# 9. Plot specific persons percentile
def plot_person_percentile_over_years(df, person_name, person_gender):
    person_data = df[df['Name'] == person_name]

    if person_data.empty:
        print(f"No data found for {person_name}")
        return

    percentiles_all = []
    percentiles_gender = []

    for year in person_data['Year'].unique():
        yearly_data = df[df['Year'] == year]
        yearly_data_gender = yearly_data[yearly_data['Gender'] == person_gender]

        pace = person_data[person_data['Year'] == year]['Pace (min/mi)'].values[0]
        percentiles_all.append((year, calculate_percentile(yearly_data['Pace (min/mi)'], pace)))
        percentiles_gender.append((year, calculate_percentile(yearly_data_gender['Pace (min/mi)'], pace)))

    years, percentiles_all = zip(*percentiles_all)
    _, percentiles_gender = zip(*percentiles_gender)

    fig, ax = plt.subplots()
    ax.plot(years, percentiles_all, marker='o', label='Overall Percentile')
    ax.plot(years, percentiles_gender, marker='x', label=f"{person_gender} Percentile")

    ax.set_title(f"{person_name}'s Percentile Over the Years")
    ax.set_xlabel('Year')
    ax.set_ylabel('Percentile')
    ax.legend()

    filename = f"{person_name}_percentile_over_years.png"
    save_fig(fig, filename)
    print(f"Plot saved as {filename}")


# 10. Plot Average Pace by Age Group
def plot_average_pace_by_age_group_over_years(df):
    bins = [0, 18, 30, 40, 50, 60, 70, 80]
    labels = ['<18', '18-29', '30-39', '40-49', '50-59', '60-69', '70+']
    df['AgeGroup'] = pd.cut(df['Age'], bins=bins, labels=labels, right=False)
    
    avg_pace_age_group = df.groupby(['Year', 'AgeGroup'])['Pace (min/mi)'].mean().unstack()
    
    fig, ax = plt.subplots(figsize=(10, 6))
    avg_pace_age_group.plot(ax=ax)
    ax.set_title('Average Pace by Age Group Over the Years')
    ax.set_xlabel('Year')
    ax.set_ylabel('Average Pace (min/mi)')
    save_fig(fig, 'average_pace_by_age_group_over_years.png')

# 11. Plot Age vs Pace
def plot_age_vs_pace_distribution(df):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(df['Age'], df['Pace (min/mi)'], alpha=0.5)
    ax.set_title('Age vs. Pace Distribution')
    ax.set_xlabel('Age')
    ax.set_ylabel('Pace (min/mi)')
    save_fig(fig, 'age_vs_pace_distribution.png')
    print("Plot saved as age_vs_pace_distribution.png")

# Run visulizations
def main():
    print("Data analysis and visulizations running...")

    plot_participation_over_years(df)
    plot_average_pace_over_years(df)
    plot_participation_by_age_group(df)
    plot_regional_participation(df)
    plot_gender_distribution(df)
    plot_top_10_fastest_swimmers(df)
    plot_average_pace_by_age_group_over_years(df)
    plot_age_vs_pace_distribution(df)

    name = "Tara Schluesche" 
    plot_specific_person_pace(df, name)
    plot_person_percentile_over_years(df, name, "F")

    print("Data analysis and visualizations saved successfully.")


if __name__ == "__main__":
    main()