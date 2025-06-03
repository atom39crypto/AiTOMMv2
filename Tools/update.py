import csv
import os

csv_file = "Tools/data.csv"

def insert_to_csv( name, value):

    role = "Contact"

    file_exists = os.path.isfile(csv_file)

    with open(csv_file, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["role", "name", "value"])

        if not file_exists:  # Write the header only if the file is new
            writer.writeheader()

        writer.writerow({"role": role, "name": name, "value": value})

    print(f"Inserted: {role}, {name}, {value}")


def delete_from_csv(name):
    if not os.path.isfile(csv_file):
        print(f"File '{csv_file}' does not exist.")
        return

    rows = []
    deleted = False

    with open(csv_file, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["name"] != name:
                rows.append(row)
            else:
                deleted = True

    with open(csv_file, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["role", "name", "value"])
        writer.writeheader()
        writer.writerows(rows)

    if deleted:
        print(f"Deleted row with name: {name}")
    else:
        print(f"No row found with name: {name}")


def update(a, b, c):
    name = a
    value = b
    choice = c
    try:
        if choice.lower() == 'insert':
            insert_to_csv(name, value)
        elif choice.lower() == 'delete':
            delete_from_csv(name)
        else:
            print("Invalid choice. Use 'insert' or 'delete'.")
        return 'phone number updated successfully'
    
    except Exception as e:
        print(f"Error: {e}")
        return 'something went wrong'

def image_update(a):
    print("<=----- IMAGE UPDATE -----=>")
    new_name = a + ".jpg"
    folder = r"VisualIntelligence\known_faces"
    old_name = os.path.join(folder, "stranger.jpg")
    try:
        if os.path.exists(old_name):
            # Rename the file
            new_name_path = os.path.join(folder, new_name)
            os.rename(old_name, new_name_path)
            return f"File renamed to {new_name}"
        else:
            return f"The file '{old_name}' does not exist."
    except FileNotFoundError as e:
       return f"Error: {e}"
    except PermissionError as e:
        return f"Permission Error: {e}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"


if __name__ == "__main__":
    # Example usage
    update("insert", "shounak", "6290664017")
