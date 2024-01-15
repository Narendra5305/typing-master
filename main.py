import random
import time
import json
import os

WORD_LIST_FILE = "word_list.json"
LEADERBOARD_FILE = "leaderboard.json"

if not os.path.exists(WORD_LIST_FILE):
    with open(WORD_LIST_FILE, "w") as file:
        json.dump({}, file)

if not os.path.exists(LEADERBOARD_FILE):
    with open(LEADERBOARD_FILE, "w") as file:
        json.dump({}, file)

def update_leaderboard(username, wpm):
    with open(LEADERBOARD_FILE, "r") as file:
        leaderboard = json.load(file)

    if username in leaderboard:
        if not isinstance(leaderboard[username], list):
            leaderboard[username] = [leaderboard[username]]
        leaderboard[username].append(wpm)
        average_speed = sum(leaderboard[username]) / len(leaderboard[username])
        leaderboard[username] = average_speed
    else:
        leaderboard[username] = wpm
    sorted_leaderboard = {
        k: v for k, v in sorted(leaderboard.items(), key=lambda item: item[1], reverse=True)
    }
    with open(LEADERBOARD_FILE, "w") as file:
        json.dump(sorted_leaderboard, file, indent=4)

def show_leaderboard():
    with open(LEADERBOARD_FILE, "r") as file:
        leaderboard = json.load(file)
        for idx, (username, wpm) in enumerate(leaderboard.items(), start=1):
            print(f"{idx}. {username}: {wpm} WPM")

def load_words_from_json(category):
    with open(WORD_LIST_FILE, "r") as file:
        word_list = json.load(file)
        return word_list.get(category, [])

def get_random_word():
    with open(WORD_LIST_FILE, "r") as file:
        word_list = json.load(file)

    random_category = random.choice(list(word_list.keys()))
    random_word = random.choice(word_list[random_category])

    return random_word

def main():
    print("Welcome to the Terminal Typing Master!")
    username = input("Enter your username: ")

    while True:
        print("\nOptions:")
        print("1. Start Typing Test")
        print("2. Show Leaderboard")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            random_word = get_random_word()

            print("Type the following word:")
            print(random_word)

            start_time = time.time()

            user_input = input("Your input: ")

            end_time = time.time()

            if user_input.strip().lower() == random_word.lower():
                time_taken = end_time - start_time
                words_per_minute = len(user_input.split()) / time_taken * 60 if time_taken > 0 else 0

                print(f"Time taken: {time_taken:.2f} seconds")
                print(f"Words per minute: {words_per_minute:.2f} WPM")

                update_leaderboard(username, words_per_minute)
            else:
                print("Incorrect! You earned 0 points for this attempt.")

        elif choice == "2":
            print("\nLeaderboard:")
            show_leaderboard()

        elif choice == "3":
            print("Exiting the Terminal Typing Master. Goodbye!")
            break

        else:
            print("Invalid choice. Please enter a valid option.")

if __name__ == "__main__":
    main()
