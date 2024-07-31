import requests
import pandas as pd

def fetch_swim_results(event_id, event_course_id, limit=100):
    print("Fetching swim results...")

    from_value = 0
    all_results = []

    while True:
        url = f"https://results.athlinks.com/event/{event_id}?eventCourseId={event_course_id}&divisionId=&intervalId=&from={from_value}&limit={limit}"
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch data from {url}")

        data = response.json()
        if not data or 'interval' not in data[0] or 'intervalResults' not in data[0]['interval']:
            break
        
        results = data[0]['interval']['intervalResults']
        if not results:
            break
        
        all_results.extend(results)
        from_value += limit
    
    print("Successfully fetched results...")

    return all_results

def parse_and_store_results(results, race_date):
    columns = ['Place', 'Name', 'Gender', 'Pace (min/mi)', 'Time (ms)', 'Age', 'Bib', 'Country', 'Locality', 'Region', 'OverallRank', 'GenderRank', 'RaceDate']
    data = []

    for result in results:
        print("Parsing results...")

        place = result.get('overallRank')
        name = result.get('displayName')
        gender = result.get('gender')
        time = result.get('time', {}).get('timeInMillis')
        
        # Check for pace data and convert to min/mi if necessary
        if 'pace' in result and 'time' in result['pace']:
            if result['pace']['distance']['distanceUnit'] == '100m':
                pace = time / (2 * 60 * 1000)  # Convert milliseconds to minutes per mile
            else:
                pace = result['pace']['time']['timeInMillis'] / (2 * 60 * 1000)
        else:
            pace = time / (2 * 60 * 1000)  # Default conversion if pace is not given

        age = result.get('age')
        bib = result.get('bib')
        country = result.get('country')
        locality = result.get('locality')
        region = result.get('region')
        overall_rank = result.get('overallRank')
        gender_rank = result.get('genderRank')
        
        data.append([place, name, gender, pace, time, age, bib, country, locality, region, overall_rank, gender_rank, race_date])

        print("Appended data to dataframe... ")
        
    df = pd.DataFrame(data, columns=columns)
    return df

events = [
    {"event_id": 71537, "event_course_id": 105499, "race_date": '2008-08-09'},
    {"event_id": 99327, "event_course_id": 138171, "race_date": '2009-08-08'},
    {"event_id": 116712, "event_course_id": 160351, "race_date": '2010-08-07'},
    {"event_id": 174805, "event_course_id": 240534, "race_date": '2011-08-06'},
    {"event_id": 222157, "event_course_id": 307963, "race_date": '2012-08-04'},
    {"event_id": 280767, "event_course_id": 399878, "race_date": '2013-08-10'},
    {"event_id": 396845, "event_course_id": 594582, "race_date": '2014-08-02'},
    {"event_id": 473893, "event_course_id": 705520, "race_date": '2015-08-01'},
    {"event_id": 591486, "event_course_id": 889709, "race_date": '2016-08-06'},
    {"event_id": 575969, "event_course_id": 863680, "race_date": '2017-07-29'},
    {"event_id": 667229, "event_course_id": 1051781, "race_date": '2018-08-04'},
    {"event_id": 766892, "event_course_id": 1310567, "race_date": '2019-08-03'},
    {"event_id": 976979, "event_course_id": 2088562, "race_date": '2021-08-07'},
    {"event_id": 1026801, "event_course_id": 2278451, "race_date": '2022-08-06'},
    {"event_id": 1057715, "event_course_id": 2388869, "race_date": '2023-08-05'}
]

all_results_df = pd.DataFrame()

for event in events:
    results = fetch_swim_results(event['event_id'], event['event_course_id'])
    event_df = parse_and_store_results(results, event['race_date'])
    all_results_df = pd.concat([all_results_df, event_df], ignore_index=True)

all_results_df.to_csv('swim_results.csv', index=False)
print("All data successfully saved to swim_results.csv")
