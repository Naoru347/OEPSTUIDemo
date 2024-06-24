import subprocess
import os

def run_script(script_name):
    if not os.path.exists(script_name):
        print(f"Required Python script({script_name}) not found. Please reverify installation and try again.")
        return
    try:
        subprocess.run(["python3", script_name], check=True)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running {script_name}: {e}")
        print(f"Return code: {e.returncode}")
        if e.output:
            print(f"Output: {e.output.decode()}")
    except FileNotFoundError:
        print(f"Error: Python interpreter not found. Ensure Python is installed and in your PATH.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        
def get_valid_input(prompt, options):
    while True:
        choice = input(prompt)
        if(choice in options):
            return choice
        else:
            print("Invalid entry detected.")
            choice = input("Please try again: ")


def main(): 
    while True: 
        print("\n1. Begin new exam")
        print("2. Generate placement report")
        print("3. Generate annual report")
        print("4. Generate x-year")
        print("5. Exit")
        menu_choice = get_valid_input("Please enter the number of your selection here (e.g., 1, 5, etc.): ", ['1', '2', '3', '4', '5'])

        if(menu_choice == '1'):
            run_script("OEPS_Examination.py")
        elif(menu_choice == '2'):
            run_script("OEPS_EXT_Reporting.py")
        elif(menu_choice == '3' or menu_choice == '4'):
            run_script("OEPS_AR.py")
        elif(menu_choice == '5'):
            break
        else:
            print("\nInvalid choice. Please try again.")    

if __name__ == "__main__":
    main()
