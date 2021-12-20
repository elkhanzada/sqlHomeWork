import cx_Oracle
import os
import pandas as pd
from tabulate import tabulate




cls = lambda: os.system('cls')

connection = []

# Print functions
def nice_print(res,table="computer"):
    columns = ["name","price","type","cpu","feature"] if table=="computer" else ["name","price","type","screen_size"]
    df = pd.DataFrame(res, columns=columns)
    print(tabulate(df,headers='keys',tablefmt='psql'))
def print_welcome():
    print("What are you looking for \n \
        1. Computer \n \
        2. Television \n \
        3. Price update \n \
        4. Exit")
def print_comp():
    print("- Computer - \n \
        1. Product list \n \
        2. Recommended products \n \
        3. Back")
def print_tv():
    print("- Television - \n \
        1. Search by price \n \
        2. Recommended products \n \
        3. Back")    









# Virtual tables in SQL
def get_datas():
    sql_comp = "(select 'A'||model as name, price,'D' as type,cpu,'None' as feature  from desktop \
            UNION \
            select 'A'||model as name,price,'L' as type,cpu, CAST(weight as varchar2(20)) as feature from laptop) \
            UNION \
            (select 'B'||model||code as name,price,type,cpu,'None' as feature from pc \
            UNION \
            select 'B'||model||code as name,price,'S' as type,cpu,'None' as feature from server)"
    sql_tv = "(select 'A'||model as name, price,'H' as type,screen_size  from hdtv \
            UNION \
            select 'A'||model as name,price,'P' as type,screen_size from pdptv) \
            UNION \
            (select 'A'||model as name,price,'L' as type,screen_size from lcdtv \
            UNION \
            select 'B'||model||code as name,price,type,screen_size from tv)"
    return sql_comp,sql_tv








# Query function for Computer table
def query_computer(option):
    cursor = connection.cursor()
    sql_comp,_ = get_datas()
    sql_comp = f"({sql_comp})"
    query = ""
    if option == 1:
        query = f"select * from {sql_comp} order by name asc"
    elif option == 2:
        avg_PA = f"select AVG(price) from {sql_comp} where name like 'A%'"
        avg_PB = f"select AVG(price) from {sql_comp} where name like 'B%'"
        avg_CPUA = f"select AVG(cpu) from {sql_comp} where name like 'A%'"
        avg_CPUB = f"select AVG(cpu) from {sql_comp} where name like 'B%'"
        query = f"select * from {sql_comp} where name like 'A%' and price < ({avg_PA}) and cpu > ({avg_CPUA}) \
                  UNION \
                  select * from {sql_comp} where name like 'B%' and price < ({avg_PB}) and cpu > ({avg_CPUB})"
    cursor.execute(query)
    res = cursor.fetchall()
    nice_print(res,"computer")








# Query function for Television table
def query_tv(option, price=-1):
    cursor = connection.cursor()
    _,sql_tv = get_datas()
    sql_tv = f"({sql_tv})"
    query = ""
    if option==1:
        distance = f"select MIN(ABS(price-{price})) as mindis from {sql_tv}"
        query = f"select * from {sql_tv} where price={price} or abs(price-{price})=({distance})  order by name asc"
    elif option==2:
        avg_price = f"select AVG(price) from {sql_tv}"
        avg_size = f"select AVG(screen_size) from {sql_tv}"
        max_ratio = f"select MAX(screen_size/price) from {sql_tv}"
        query = f"select * from {sql_tv} where price < ({avg_price}) and screen_size > ({avg_size}) and screen_size/price = ({max_ratio})"
    cursor.execute(query)
    res = cursor.fetchall()
    nice_print(res,"tv")








# Parsing input (code) before query for Computer table
def execute_comp(code):
    if code == 1 or code==2:
        query_computer(code)
    elif code == 3:
        return 3
    else:
        cls()
        print("No such option. Try again.")
    return 1

# Parsing input (code) before query for Television table
def execute_tv(code):
    if code==1:
        try:
            price = int(input("Input a non-negative integer: "))
            if price < 0:
                cls()
                print("ONLY NON-NEGATIVE INTEGER NUMBER IS ALLOWED!!!!")
            query_tv(code,price)
        except:
            cls()
            print("ONLY NON-NEGATIVE INTEGER NUMBER IS ALLOWED!!!!")
    elif code == 2:
        query_tv(code)
    elif code == 3:
        return 3
    else:
        cls()
        print("No such option. Try again.")
    return 2











# Update tables according to given parameters
def update_tables():
    cursor = connection.cursor()
    sql_comp, sql_tv = get_datas()
    sql_comp = f"({sql_comp})"
    sql_tv = f"({sql_tv})"
    tables_comp = ["desktop", "laptop","pc","server"]
    tables_tv = [ "hdtv", "pdptv", "lcdtv", "tv"]

    avg_CPU = f"select AVG(cpu) from {sql_comp}"
    cursor.execute(avg_CPU)
    avg_CPU = cursor.fetchall()[0][0]
    max_price = f"select MAX(price) from {sql_comp}"
    cursor.execute(max_price)
    max_price = cursor.fetchall()[0][0]
    for table in tables_comp:
        update_comp = f"update {table} set price=0.9*price where cpu < {avg_CPU}"
        cursor.execute(update_comp)
        connection.commit()
        delete_comp = f"delete from {table} where price={max_price}"
        cursor.execute(delete_comp)
        connection.commit()

    max_screen = f"select MAX(screen_size) from {sql_tv}"
    cursor.execute(max_screen)
    max_screen = cursor.fetchall()[0][0]
    max_ratio = f"select MAX(screen_size/price) from {sql_tv}"
    cursor.execute(max_ratio)
    max_ratio = cursor.fetchall()[0][0]
    for table in tables_tv:
        update_tv = f"update {table} set price=1.1*price where screen_size={max_screen}"
        cursor.execute(update_tv)
        connection.commit()        
        delete_tv = f"delete from {table} where screen_size/price={max_ratio}"
        cursor.execute(delete_tv)
        connection.commit()
    

if __name__=='__main__':
    success = False
    while not success:
        try:
            user = str(input("Username: "))
            password = str(input("Password: ")) 
            connection = cx_Oracle.connect(
                user=user,
                password=password,
                dsn="localhost:1521"
            )
            success = True
        except:
            print("Wrong credentials. Please try again.")

    code = 0
    subsection = False
    while True:
        try:
            if not subsection:
                print_welcome()
                code = int(input("Choose a number [1-4]: "))
                cls()
            if code==1:
                subsection = True
                print_comp()
                code = int(input("Choose a number [1-3]: "))
                code = execute_comp(code)
                if code == 3:
                    subsection = False
                    cls()
                    continue
            elif code==2:
                subsection = True
                print_tv()
                code = int(input("Choose a number [1-3]: "))
                if code == 3:
                    subsection = False
                    cls()
                code = execute_tv(code)
            elif code==3:
                print("Updating table")
                update_tables()
                print("Updating is done")
                subsection = False
                continue
            elif code==4:
                break
            else:
                print("No such option. Try again.")
                continue
        except Exception as e:
            cls()
            #print(e)
            print("ONLY INTEGER NUMBER IS ALLOWED!!!!")
            continue
    connection.close()