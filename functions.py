import requests
import csv
from api_key import omdb_key


def clean_box_office(input_box_office):
    box_office_split = input_box_office.split('$')[1].split(',')
    box_office_string =''.join(box_office_split)
    box_office_int = int(box_office_string)
    return box_office_int

def clean_award_wins(input_wins):
    wins_split = input_wins.split('wins')[0].split('.')[1]
    wins_int = int(wins_split)
    return wins_int

def clean_award_noms(input_noms):
    noms_split = input_noms.split('nominations')[0].split('&')[1]
    noms_int = int(noms_split)
    return noms_int

def clean_runtime(input_time):
    runtime_split = input_time.split(' ')[0]
    runtime_int = int(runtime_split)
    return runtime_int

def create_movies_csv(oscar_winners_csv):
    with open('movies.csv', 'w', newline='') as movies_csv:
        fieldnames = ['movie_title','runtime','genre','award_wins','award_nominations','box_office']
        writer = csv.DictWriter(movies_csv, fieldnames=fieldnames)
        writer.writeheader()
        with open(oscar_winners_csv) as winners_csv:
            winners_data = csv.reader(winners_csv)
            next(winners_data) #skips header row
            for row in winners_data:
                res = requests.get(f"http://www.omdbapi.com/?i={row[1]}&apikey={omdb_key}")
                writer.writerow({
                    fieldnames[0]: res.json()['Title'], 
                    fieldnames[1]: clean_runtime(res.json()['Runtime']), 
                    fieldnames[2]: res.json()['Genre'], 
                    fieldnames[3]: clean_award_wins(res.json()['Awards']), 
                    fieldnames[4]: clean_award_noms(res.json()['Awards']),
                    fieldnames[5]: clean_box_office(res.json()['BoxOffice'])
                })

