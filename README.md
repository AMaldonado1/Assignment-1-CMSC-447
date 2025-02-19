# School CRUD MySQL Application

Assignment 1 Part 2

---

## Features

- **Database Creation:** Automatically creates the `school` database and required tables (`student`, `instructor`, `course`, and `enrollment`).
- **CRUD Operations:**
  - **View Tables:** Display table data using Pandas.
  - **Add Entry:** Dynamically add entries to any table.
  - **Remove Entry:** Delete entries by primary key.
  - **Delete All Entries:** Remove all rows from all tables while preserving the table structure.
- **User-Friendly CLI:** Provides a text-based menu to perform all CRUD operations.

---

## Requirements

- **MySQL Server** (running on localhost or a remote server)
- Python packages:
  - **PyMySQL**
  - **Pandas**
  - **getpass**

Install the required packages using:
```bash
pip install pymysql pandas getpass
```

---

## MySQL Server
- Install and start your MySQL server.
- Ensure you have your credentials (username, password, host, port) ready.

---

## Usage

1. Run the Application:

```bash
python main.py
```
The program will prompt you for your MySQL credentials.

2. Main Menu Options:
   - 0: View tables
   - 1: Add entry
   - 2: Remove entry
   - 3: Delete all entries (tables are kept)
   - 4: Exit database


3. Follow On-Screen Prompts:
   - For adding an entry, the program displays the attributes (excluding primary keys) and asks you to enter values separated by comma and space.
   - For viewing tables, you can choose which table(s) to display.
   - For removal, you input primary key values.
   - For deleting all entries, you'll be asked for confirmation to prevent accidental data loss.
