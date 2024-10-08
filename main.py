import requests
import json
import time

# Paste your SportsMonk API key here
API_KEY = '1KLBIcXtDpZxPYP3GvKRslOUWVE1h9pBeuT2Zixjg7ZmohRTjGL4DUWBp6Kr'
# Endpoint for live and upcoming matches
LIVE_API_URL = 'https://cricket.sportmonks.com/api/v2.0/livescores'
UPCOMING_API_URL = 'https://cricket.sportmonks.com/api/v2.0/fixtures?include=localteam,visitorteam'

def print_header(title):
    print("\n" + "=" * 40)
    print(f"{title.center(40)}")
    print("=" * 40)

def get_live_cricket_scores(team_filter=None):
    print_header("Live Cricket Scores")
    try:
        response = requests.get(LIVE_API_URL, params={'api_token': API_KEY})
        response.raise_for_status()
        data = response.json()

        if data['data']:
            for match in data['data']:
                team1 = match['localteam']['name']
                team2 = match['visitorteam']['name']
                
                # Filter by team (if user specifies)
                if team_filter and team_filter.lower() not in (team1.lower(), team2.lower()):
                    continue

                # Match details
                print(f"Match: {team1} vs {team2}")
                print(f"Status: {match['status']}")
                print(f"Venue: {match['venue']['name'] if 'venue' in match else 'Unknown'}")
                print(f"Toss: {match['toss_won_team']['name'] if 'toss_won_team' in match else 'Not decided'}")

                # Score details
                score = match.get('scoreboards', {})
                if score:
                    for innings in score:
                        team = innings.get('team', {}).get('name', 'Unknown Team')
                        runs = innings.get('score', 0)
                        wickets = innings.get('wickets', 0)
                        overs = innings.get('overs', 0.0)
                        print(f"{team} - {runs}/{wickets} in {overs} overs")
                else:
                    print("Score not available yet.")
                print("-" * 40)
        else:
            print("No live matches right now.")
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")
    except Exception as e:
        print(f"An error occurred: {e}")

def get_upcoming_matches():
    print_header("Upcoming Cricket Matches")
    try:
        response = requests.get(UPCOMING_API_URL, params={'api_token': API_KEY})
        response.raise_for_status()
        data = response.json()

        if data['data']:
            for match in data['data']:
                team1 = match['localteam']['name']
                team2 = match['visitorteam']['name']
                print(f"{team1} vs {team2}")
                print(f"Start Time: {match['starting_at']}")
                print(f"Venue: {match['venue']['name'] if 'venue' in match else 'Unknown'}")
                print("-" * 40)
        else:
            print("No upcoming matches.")
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")
    except Exception as e:
        print(f"An error occurred: {e}")

def save_scores_to_file(scores):
    try:
        with open('live_scores.txt', 'w') as file:
            file.write(scores)
        print("Scores saved to live_scores.txt")
    except Exception as e:
        print(f"Error saving scores: {e}")

def refresh_scores(interval=60, team_filter=None):
    print(f"Auto-refreshing every {interval} seconds. Press Ctrl+C to stop.\n")
    try:
        while True:
            get_live_cricket_scores(team_filter=team_filter)
            print(f"Refreshing in {interval} seconds...\n")
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\nAuto-refresh stopped. Returning to the main menu...\n")

def main_menu():
    while True:
        print_header("Cricket Score Viewer")
        print("1. View Live Scores")
        print("2. View Upcoming Matches")
        print("3. Filter Live Scores by Team")
        print("4. Save Live Scores to File")
        print("5. Auto-Refresh Live Scores")
        print("6. Exit")

        choice = input("Choose an option (1-6): ")

        if choice == '1':
            get_live_cricket_scores()
            if not back_to_menu(): break
        elif choice == '2':
            get_upcoming_matches()
            if not back_to_menu(): break
        elif choice == '3':
            team_name = input("Enter team name to filter by: ")
            get_live_cricket_scores(team_filter=team_name)
            if not back_to_menu(): break
        elif choice == '4':
            scores = get_live_cricket_scores()
            if scores:
                save_scores_to_file(scores)
            if not back_to_menu(): break
        elif choice == '5':
            team_name = input("Enter team name to filter (leave blank for no filter): ")
            interval = int(input("Enter refresh interval (in seconds): "))
            refresh_scores(interval=interval, team_filter=team_name)
        elif choice == '6':
            print("Thank you for using the Cricket Score Viewer. Goodbye!")
            break
        else:
            print("Invalid option! Please choose a number between 1 and 6.")

def back_to_menu():
    """Ask the user if they want to go back to the main menu or exit."""
    while True:
        choice = input("\nPress M to return to the main menu or E to exit: ").lower()
        if choice == 'm':
            return True  # Go back to the main menu
        elif choice == 'e':
            print("Thank you for using the Cricket Score Viewer. Goodbye!")
            return False  # Exit the program
        else:
            print("Invalid choice. Please press M to return to the menu or E to exit.")

if __name__ == '__main__':
    main_menu()
