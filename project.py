import sqlite3
from prettytable import from_db_cursor

# functionality: will allow user to choose 1. add, 2. read
# program will run according to user choice 
# case statements? like type 1 to add, 2 to read, etc...
def main():
    while True:
        try:
            choice = int(input("Welcome to your grocery list! Type in corresponding number for your selection. \n 1. Read list \n 2. Add to list \n 3. Edit list \n 4. Delete entry \n --> "))
            match choice:
                case 1:
                    read_items()
                case 2:
                    add_items()
                case 3:
                    edit_items()
                case 4:
                    delete_items()
        except ValueError:
            pass


def read_items():
    con = sqlite3.connect("grocery.db")
    cur = con.cursor()
    try:
        read_list = cur.execute("SELECT * FROM grocery_list ORDER BY item")
    except Exception:
        print("No available list")
        return 
    print("------- Grocery List --------")
    grocery_table = from_db_cursor(cur)
    grocery_table.align = "l"
    print(grocery_table, "\n")
    # for i, row in enumerate(read_list):
    #     print(f"{i + 1}.", f"{row[0]}: {row[1]}")
    con.close()


def add_items():
    # create and open a new database connection 
    # Connection object is to the on-disk database
    
    con = sqlite3.connect("grocery.db")
    # in order to execute SQL statements and fetch results from SQL queries
    # need to use database cursor - allows for traversal over records in database
    # allows you to retrieve, add, remove database records
    # Cursor object - are iterators.. if use SELECT query, can simply iterate
    # over the cursor to fetch resulting row 
    cur = con.cursor()
    # create database table called "grocery_list" with columns in paren
    # only if the file doesn't exist
    # if not os.path.exists("grocery.db"):
    cur.execute(f"CREATE TABLE IF NOT EXISTS grocery_list(item, quantity)")
    
    # ask for user_item to add
    
    while True:
        try:            
            user_item = input("What to add? ")
            user_quantity = input("How many? ")
            insert_sql = """ INSERT INTO grocery_list(item, quantity) VALUES
                            (?,?) """
            if not user_item == "" and not user_quantity == "":
                cur.execute(insert_sql, (user_item, user_quantity))
            else:
                pass        
        except EOFError:
            con.commit()
            print()
            read_items()
            break 


def edit_items():
    # form connection with database
    con = sqlite3.connect("grocery.db")
    cur = con.cursor()
    # show user current list
    read_list = cur.execute("SELECT * FROM grocery_list")
    for i, row in enumerate(read_list):
        print(f"{i + 1}.", f"{row[0]}: {row[1]}")  
    # capture user answer
    while True:
        try:
            # prompt user to select entry to edit
            entry_num = int(input("What entry would you like to edit? "))
            # match id that user selects with database entry id
            # sql_entry = cur.execute("SELECT * FROM grocery_list WHERE rowid = ?")
            cur.execute("SELECT * FROM grocery_list WHERE rowid = ?", (entry_num,))
            # get the specific rowid entry
            row = cur.fetchone()
            verify = input(f"Edit {row[0]} with quantity of {row[1]} Y|N? ")
            verify = verify.lower()
            # edit item
            if verify == "y":
                edit_item = input(f"Edit item? {row[0]} Y|N? ")
                edit_item = edit_item.lower()
                if edit_item == "y":
                    item_value = input(f"What do you want to edit {row[0]} to? " )
                    item_sql = """ UPDATE grocery_list SET item = ? WHERE rowid = ? """
                    cur.execute(item_sql, (item_value, entry_num))
                    con.commit()
                    # edit quantity
                    edit_quantity(entry_num, row)
                elif edit_item == "n":
                    edit_quantity(entry_num, row)
                    return
                else:
                    print("Invalid Selection")         
            else:
                pass                
        except (ValueError, TypeError):
            print("Invalid Selection")
            pass
        except EOFError:
            return

def edit_quantity(id, result):    
    edit_qty = input(f"Edit quantity? {result[1]} Y|N? ")
    edit_qty = edit_qty.lower()
    if edit_qty == "y":
        con = sqlite3.connect("grocery.db")
        cur = con.cursor()
        qty_value = input(f"What do you want to edit {result[1]} to? ")
        qty_sql = """ UPDATE grocery_list SET quantity = ? WHERE rowid = ? """
        cur.execute(qty_sql, (qty_value, id))
        con.commit()
        cur.execute("SELECT * FROM grocery_list WHERE rowid = ?", (id,))
        edited_row = cur.fetchone()
        print(f"{edited_row[0]}: {edited_row[1]}")
        con.close()
    else:
        con = sqlite3.connect("grocery.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM grocery_list WHERE rowid = ?", (id,))
        edited_row = cur.fetchone()
        print(f"{edited_row[0]}: {edited_row[1]}")
        con.close()
        return

def delete_items():
   
    con = sqlite3.connect("grocery.db")
    cur = con.cursor()
    cur.execute("SELECT rowid AS [item number], item, quantity FROM grocery_list")
    print("-------------- Grocery List ---------------")
    grocery_table = from_db_cursor(cur)
    grocery_table.align = "l"
    print(grocery_table, "\n")

    while True:
        try:
            entry_num = int(input("Which entry do you want to delete? "))            
            cur.execute("SELECT * FROM grocery_list WHERE rowid = ?", (entry_num,))
            row = cur.fetchone()
            confirm = input(f"Are you sure you want to delete {row[0]} from your list Y|N? ")
            confirm = confirm.lower()
            if confirm == "y":
                cur.execute("DELETE FROM grocery_list WHERE rowid = ?", (entry_num,))
                con.commit()
                con.close()
            elif confirm == "n":
                return
            else:
                print("Invalid Selection-")
        except (ValueError, TypeError):
            print("Invalid Selection")
            pass
        except EOFError:
            return



if __name__ == "__main__":
     main()



     