import json
import random
from datetime import datetime,timedelta

DATE_FORMAT = "%d-%m-%Y"


################# Printing #################

def print_task_list(task_list, title="Task List"):
    #Prints tasks as an enumerated list
    if not task_list:
        print(f"\n{title} is empty")
        return

    print(f"\n{title}:\n" + "-" * 30)
    max_name_length = max(len(task['task_name']) for task in task_list) + 2

    for index, task in enumerate(task_list):
        #Checks for completion status and adds it. Only in random_task_select
        completion_status = " (Completed)" if task.get("completed_today") else ""
        print(
            f"\t{str(index).rjust(2)}: "
            f"{task['task_name'].ljust(max_name_length)} "
            f"Time: {task['task_time']} "
            f"\tRepeat window: {task['task_repeat_window']} "
            f"\tLast completion: {task['last_complete_date']}"
            f"\t{completion_status}"
        )

    print("-" * 30)


################# Saving & Loading #################

def save_task_list_json(task_list, filename="task_list.json"):
    # Save the task list as a json file
    with open(filename, "w") as json_file:
        json.dump(task_list, json_file)
    print(f"Tasks saved to {filename}")


def load_task_list_json(filename="task_list.json"):
    # Load the task list as a json file
    try:
        with open(filename, "r") as json_file:
            source_list = json.load(json_file)
            task_list = sort_list_abc(source_list)
        return task_list
    except (FileNotFoundError, json.JSONDecodeError):
        print("No valid file found")
        return []


################# Sorting Options #################

def sort_list_abc(task_list):
    return sorted(task_list, key=lambda x: x['task_name'])


def sort_list_completed(task_list):
    completed_list = [task for task in task_list if repeat_window_check(task)]
    print_task_list(completed_list, "Completed Task List")
    return completed_list

def sort_list_uncompleted(task_list):
    uncompleted_list = [task for task in task_list if not repeat_window_check(task)]
    print_task_list(uncompleted_list, "Uncompleted Task List")
    return uncompleted_list


################# Input Validation #################

def get_numeric_input(prompt, min_value = 1):
    while True:
        value = input(prompt)
        if value.lower() == "done":
            return None
        if value.isdigit() and int(value) >= min_value:
            return int(value)
        print(f"Please enter a number larger than {min_value}, or 'done' to cancel.\n")


def valid_time(task_time):
    return task_time.isdigit() and int(task_time) > 4


def get_valid_time_input(prompt):
    while True:
        value = input(prompt)
        if valid_time(value):
            return int(value)
        print("Numbers only and needs to be at least 5 minutes")


def get_date_input(prompt):
    while True:
        value = input(prompt)
        if value.lower() == "done":
            return None
        try:
            datetime.strptime(value, DATE_FORMAT)
            return value
        except ValueError:
            print("Invalid date. Please use format dd-mm-yyyy or type 'done' to cancel.")


def todays_list_completion(todays_list):
    while True:
        task_input = input("Enter the task number you have completed (type 'done' to exit): ")

        if task_input.lower() == "done":
            print("\nFinished for today")
            break
        if not task_input.isdigit():
            print("Enter numbers only or 'done' to exit.")
            continue

        task_number = int(task_input)

        if 0 <= task_number < len(todays_list):
            todays_list[task_number]["last_complete_date"] = datetime.today().strftime(DATE_FORMAT)
            print(f"Task '{todays_list[task_number]['task_name']}' marked as completed on {todays_list[task_number]['last_complete_date']}.")

            for task in todays_list:
                task["completed_today"] = repeat_window_check(task)

            print_task_list(todays_list, "Today's List")

            for task in todays_list:
                task.pop("completed_today")
        else:
            print(f"Invalid task number. Enter a number between 0 and {len(todays_list) - 1}.")
    return todays_list


def manual_completion(task_list):

    uncompleted_list = sort_list_uncompleted(task_list)

    while True:
        task_input = input("Enter the task number you have completed (type 'done' to exit): ")

        if task_input.lower() == "done":
            print("\nFinished for today")
            break
        if not task_input.isdigit():
            print("Enter numbers only or 'done' to exit.")
            continue

        task_number = int(task_input)

        if 0 <= task_number < len(uncompleted_list):
            uncompleted_list[task_number]["last_complete_date"] = datetime.today().strftime(DATE_FORMAT)
            print(f"Task '{uncompleted_list[task_number]['task_name']}' marked as completed on {uncompleted_list[task_number]['last_complete_date']}.")

            for task in uncompleted_list:
                task["completed_today"] = repeat_window_check(task)

            print_task_list(uncompleted_list, "Uncompleted List")

            for task in uncompleted_list:
                task.pop("completed_today")
        else:
            print(f"Invalid task number. Enter a number between 0 and {len(uncompleted_list) - 1}.")
    return uncompleted_list


################# Logic #################

def repeat_window_check(task):
    last_complete_date = datetime.strptime(task["last_complete_date"], DATE_FORMAT)
    repeat_window_days = task['task_repeat_window'] * 7
    threshold_date = datetime.today() - timedelta(days=repeat_window_days)

    return last_complete_date > threshold_date


def random_task_select(task_list):
    todays_list = []
    total_time = 0

    if not task_list:
        print("\nTask list is empty")
        return task_list

    while True:
        try:
            todays_time = int(input("How much time do you have today in minutes? "))
            break
        except ValueError:
            print("Please enter a valid number")

    uncompleted_list = [task for task in task_list if not repeat_window_check(task)]
    if not uncompleted_list:
        print("\nYou are up to date on tasks!")
        return task_list

    random.shuffle(uncompleted_list)

    for task in uncompleted_list:
        if total_time + task['task_time'] <= todays_time:
            todays_list.append(task)
            total_time += task['task_time']

        if total_time >= todays_time:
            break

    if not todays_list:
        print("\nNo tasks can be completed within the given time.")
        return task_list

    print_task_list(todays_list, "Today's Tasks")
    todays_list_completion(todays_list)

    return sort_list_abc(task_list)


################# Management #################


def add_tasks(task_list):
    # User inputs the task name, task time and repeat window and a check is done to see if all is valid
    while True:

        task_name = input("\nEnter task name: ").title()
        if task_name.lower() == "done":
            print("Task discarded\n")
            break

        task_time = get_numeric_input(f"How long will {task_name} take in minutes? ", 5)
        if task_time is None:
            print("Task discarded\n")
            break

        task_repeat_window = get_numeric_input(f"Repeat {task_name} after how many weeks? ", 1)
        if task_repeat_window == None:
            print("Task discarded")
            break


        task_last_completed = input(f"\nWhen was '{task_name}' last completed?\n1. Today\n2. Never\n3. Enter Date\n\nPlease Choose: ")
        if task_last_completed.lower() == "done":
            print("Task discarded\n")
            break

        if task_last_completed == "1":
            last_complete_date = datetime.today().strftime(DATE_FORMAT)
        elif task_last_completed == "2":
            last_complete_date = "01-01-1900"
        elif task_last_completed == "3":
            last_complete_date = get_date_input("Please enter last completion date(DD-MM-YYYY): ")
            if last_complete_date == None:
                print("Task discarded\n")
                break

        else:
            print("Invalid choice, task discarded")
            continue


        task_list.append({
            "task_name": task_name,
            "task_time": int(task_time),
            "task_repeat_window": int(task_repeat_window),
            "last_complete_date" : last_complete_date
        })
        print(f"\nTask created: {task_name}")

    return sort_list_abc(task_list)


def remove_tasks(task_list):

    if not task_list:
        print("\nTask list is empty")
        return

    print_task_list(task_list, "Select a Task to Remove")

    try:
        choice = int(input("\nEnter the index of the task to remove: "))

        if 0 <= choice < len(task_list):
            removed_task = task_list.pop(choice)
            print(f"\nRemoved task: {removed_task['task_name']}\n")
        else:
            print(f"Invalid index number. Enter a number between 0 and {len(task_list) - 1}.")
    except ValueError:
        print("\nPlease enter a valid number")


def edit_task(task_list):

    if not task_list:
        print("\nTask list is empty")
        return

    print_task_list(task_list, "Select a Task to Edit")

    while True:
        try:
            choice = int(input("\nEnter the index of the task to edit: "))
            break
        except ValueError:
            print(f"\nPlease enter a valid number between 0 and {len(task_list) - 1}")
            continue

    if 0 <= choice < len(task_list):
        task_to_edit = task_list[choice]
        print(f"\nTask to edit: {task_to_edit['task_name']}\n")

        parameter_choice = input("Which parameter would you like to edit? (name/time/window/date): ").strip().lower()

        if parameter_choice == "name":
            task_to_edit['task_name'] = input("Please enter new name: ").title()
        elif parameter_choice == "time":
            task_to_edit['task_time'] = get_valid_time_input("Please enter new time in minutes: ")
        elif parameter_choice == "window":
            task_to_edit['task_repeat_window'] = get_numeric_input("Please enter new repeat window in weeks: ", 1)
        elif parameter_choice == "date":
            task_to_edit['last_complete_date'] = get_date_input("Please enter new completion date (dd-mm-yyyy): ")
        else:
            print("Invalid parameter")
            return

        print(f"\nUpdated task:")
        print_task_list([task_to_edit], "Edited Task")

    else:
        print(f"Invalid index number. Enter a number between 0 and {len(task_list) - 1}.")

################# Show List #################

def show_list(task_list):

    print_task_list(task_list, "Task List")

    while True:
        try:
            sort_option = int(input("\nSort differently? \n1. Completed\n2. Uncompleted\n3. Back\n\nPlease Choose: "))
        except ValueError:
            print("Invalid input (1/2/3 only)")
            continue

        if sort_option == 1:
            sort_list_completed(task_list)
        elif sort_option == 2:
            sort_list_uncompleted(task_list)
        elif sort_option == 3:
            break
        else:
            print("Invalid input (1/2/3 only)")


################# Main Menu #################

def menu(task_list):
    while True:
        menu_choice = input("\n1. Start cleaning\n"
                            "2. Add a task\n"
                            "3. Edit a task\n"
                            "4. Remove a task\n"
                            "5. Show task list\n"
                            "6. Save task list\n"
                            "9. Exit\n\n"
                            "Please choose: ")

        if menu_choice == "1":
            while True:
                cleaning_choice = input("\n1. Randomly\n2. Manually\n\nPlease choose: ")
                if cleaning_choice == "1":
                    task_list = random_task_select(task_list)
                    break
                elif cleaning_choice == "2":
                    manual_completion(task_list)
                    break
        elif menu_choice == "2":
            task_list = add_tasks(task_list)
        elif menu_choice == "3":
            edit_task(task_list)
        elif menu_choice == "4":
            remove_tasks(task_list)
        elif menu_choice == "5":
            show_list(task_list)
        elif menu_choice == "6":
            save_task_list_json(task_list)
        elif menu_choice == "9":
            print("\nGoodbye!")
            break
        else:
            print("Numbers only")
            continue


################# Main #################

def main():
    task_list = load_task_list_json()
    menu(task_list)


main()
