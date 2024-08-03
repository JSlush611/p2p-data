import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from util import save_fig, calculate_percentile

plt.style.use("fivethirtyeight")
df = pd.read_csv('swim_results.csv')

# Convert RaceDate to datetime
df['RaceDate'] = pd.to_datetime(df['RaceDate'])

# Extract year from RaceDate for analysis
df['Year'] = df['RaceDate'].dt.year

# Convert MS to Minutes
df['Time (min)'] = df['Time (ms)'] / 60000


# Function to find the position of a swimmer's best performance in a specific year
def find_swimmer_position(df, name, year):
    swimmer_data = df[(df['Name'] == name) & (df['Year'] == year)]

    if swimmer_data.empty:
        print(f"No data found for {name} in {year}")
        return None

    best_time = swimmer_data['Time (min)'].min()

    year_data = df[df['Year'] == year]

    # Calculate the rank of the swimmer's best time among all swimmers in that year
    overall_rank = (df['Time (min)'] < best_time).sum() + 1

    print(f"{name}'s time in {year} is ranked {overall_rank} out of {len(df)} participants across all years.")
    return overall_rank


# 1. Overall Participation Over the Years
def plot_participation_over_years(df):
    participation = df.groupby('Year')['Name'].count()
    fig, ax = plt.subplots()
    participation.plot(kind='bar', ax=ax)
    ax.set_title('Overall Participation Over the Years')
    ax.set_xlabel('Year')
    ax.set_ylabel('Number of Participants')
    save_fig(fig, 'participation_over_years.png')


# 2. Average Time Over the Years
def plot_average_time_over_years(df):
    avg_time = df.groupby('Year')['Time (min)'].mean()
    fig, ax = plt.subplots()
    avg_time.plot(ax=ax)
    ax.set_title('Average Time Over the Years')
    ax.set_xlabel('Year')
    ax.set_ylabel('Average Time (min)')
    save_fig(fig, 'average_time_over_years.png')


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


# 5. Time Percentiles
def plot_time_percentiles(df):
    percentiles = df['Time (min)'].quantile([0.25, 0.5, 0.75])
    fig, ax = plt.subplots()
    percentiles.plot(kind='bar', ax=ax)
    ax.set_title('Time Percentiles')
    ax.set_xlabel('Percentile')
    ax.set_ylabel('Time (min)')
    save_fig(fig, 'time_percentiles.png')


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
    top_10_fastest = df.nsmallest(10, 'Time (ms)')
    fig, ax = plt.subplots()
    top_10_fastest.plot(kind='bar', x='Name', y='Time (ms)', ax=ax)
    ax.set_title('Top 10 Fastest Swimmers')
    ax.set_xlabel('Swimmer')
    ax.set_ylabel('Time (ms)')
    save_fig(fig, 'top_10_fastest_swimmers.png')


# 8. Plot specific person's time
def plot_specific_person_time(df, name):
    person_data = df[df['Name'] == name]

    if person_data.empty:
        print(f"No data found for {name}")
        return

    fig, ax = plt.subplots()
    person_data.plot(kind='line', x='Year', y='Time (min)', marker='o', ax=ax)
    ax.set_title(f"{name}'s Time Over the Years")
    ax.set_xlabel('Year')
    ax.set_ylabel('Time (min)')

    # Create directory structure
    sanitized_name = name.replace(" ", "_").lower()  # Replace spaces with underscores and convert to lower case
    directory = f"/Users/jonathanschluesche/Desktop/development/p2p-data/graphs/names/{sanitized_name}"
    os.makedirs(directory, exist_ok=True)  # Create the directory if it doesn't exist
    filename = os.path.join(directory, f"{sanitized_name}_time_percentile_over_years.png")
    save_fig(fig, filename)
    print(f"Plot saved as {filename}")


# 9. Plot specific person's time percentile
def plot_person_time_percentile_over_years(df, name, person_gender):
    person_data = df[df['Name'] == name]

    if person_data.empty:
        print(f"No data found for {name}")
        return

    percentiles_all = []
    percentiles_gender = []

    for year in person_data['Year'].unique():
        yearly_data = df[df['Year'] == year]
        yearly_data_gender = yearly_data[yearly_data['Gender'] == person_gender]

        time = person_data[person_data['Year'] == year]['Time (min)'].values[0]
        percentiles_all.append((year, calculate_percentile(yearly_data['Time (min)'], time)))
        percentiles_gender.append((year, calculate_percentile(yearly_data_gender['Time (min)'], time)))

    years, percentiles_all = zip(*percentiles_all)
    _, percentiles_gender = zip(*percentiles_gender)

    fig, ax = plt.subplots()
    ax.plot(years, percentiles_all, marker='o', label='Overall Percentile')
    ax.plot(years, percentiles_gender, marker='x', label=f"{person_gender} Percentile")

    ax.set_title(f"{name}'s Percentile Over the Years")
    ax.set_xlabel('Year')
    ax.set_ylabel('Percentile')
    ax.legend()

    # Create directory structure
    sanitized_name = name.replace(" ", "_").lower()  # Replace spaces with underscores and convert to lower case
    directory = f"/Users/jonathanschluesche/Desktop/development/p2p-data/graphs/names/{sanitized_name}"
    os.makedirs(directory, exist_ok=True)  # Create the directory if it doesn't exist
    filename = os.path.join(directory, f"{sanitized_name}_time_over_years.png")
    save_fig(fig, filename)
    print(f"Plot saved as {filename}")


# 10. Plot Average Time by Age Group
def plot_average_time_by_age_group_over_years(df):
    bins = [0, 18, 30, 40, 50, 60, 70, 80]
    labels = ['<18', '18-29', '30-39', '40-49', '50-59', '60-69', '70+']
    df['AgeGroup'] = pd.cut(df['Age'], bins=bins, labels=labels, right=False)
    
    avg_time_age_group = df.groupby(['Year', 'AgeGroup'])['Time (min)'].mean().unstack()
    
    fig, ax = plt.subplots(figsize=(10, 6))
    avg_time_age_group.plot(ax=ax)
    ax.set_title('Average Time by Age Group Over the Years')
    ax.set_xlabel('Year')
    ax.set_ylabel('Average Time (min)')
    save_fig(fig, 'average_time_by_age_group_over_years.png')


# 11. Plot Age vs Time
def plot_age_vs_time_distribution(df):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(df['Age'], df['Time (min)'], alpha=0.5)
    ax.set_title('Age vs. Time Distribution')
    ax.set_xlabel('Age')
    ax.set_ylabel('Time (min)')
    save_fig(fig, 'age_vs_time_distribution.png')


# Run visulizations
def main():
    print("Data analysis and visualizations running...")

    plot_participation_over_years(df)
    plot_average_time_over_years(df)
    plot_participation_by_age_group(df)
    plot_regional_participation(df)
    plot_gender_distribution(df)
    plot_top_10_fastest_swimmers(df)
    plot_average_time_by_age_group_over_years(df)
    plot_age_vs_time_distribution(df)

    name = "Mark Schluesche".lower()
    plot_specific_person_time(df, name)
    plot_person_time_percentile_over_years(df, name, "M")
    find_swimmer_position(df, name, 2024)

    print("Data analysis and visualizations saved successfully.")

if __name__ == "__main__":
    main()