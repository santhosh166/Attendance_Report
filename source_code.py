import psycopg2

# pip install rich
from rich import print

from rich.table import Table

from rich.console import Console

# first create a database name as attendance->  create database attendance;

con = psycopg2.connect(database="attendance", user='postgres', password='123098', host='localhost')

class santhosh:

      def connection(self):          #Check Connection valid or not
          if con:return True
          else:return False
      
      def exists(self,tb):            #Check table exists or not
          res=con.cursor()
          res.execute("select to_regclass('public.{}')".format(tb))
          if res.fetchone()[0]==tb:
              return False
          return True
      
      def create(self,tb):           # Create table for attendance(based on date,month,year)
          if self.exists(tb)==True:
            res=con.cursor()
            q="create table {} (Roll_no int,Name VARCHAR(50),Active VARCHAR(10))".format(tb)
            res.execute(q)
            con.commit()
          else:
                
                print("\n[bold red]Attendance table for {:02d}-{:02d}-{:02d} already exists[/bold red]".format(int(tb[2:3]),int(tb[4:5]),int(tb[6:10])))
                print()
                return 'p'

      def add(self,roll,name,active,t):  # Add roll no,name,and active(present or not) into the table

          res=con.cursor()
          q="insert into {} values(%s,%s,%s)".format(t)
          res.execute(q,(roll,name,active))
          con.commit()
          print("[bold green]Attendance added successfully..![/bold green]")
           

      def show(self,*l):             # show the Attendance table(based on user input)
          console=Console()
          if l:
              res=con.cursor()
              q="select * from {}".format('t'+"_"+str(l[0])+"_"+str(l[1])+"_"+str(l[2]))
              res.execute(q)

              table=Table(show_header=True,header_style="bold magenta")

              table.add_column('Roll_no',justify='center')
              table.add_column('Name',justify='center')
              table.add_column('Active',justify='center')
              
              for row in res.fetchall():
                  table.add_row(str(row[0]),str(row[1]),str(row[2]))

              print("\n\tAttendance Report:{:02d}-{:02d}-{:02d}".format(int(l[0]),int(l[1]),int(l[2])))
              console.print(table)
          else:
              res=con.cursor()
              res.execute("select * from information_schema.tables where table_schema = 'public'")

              for row in res.fetchall():
                  res1=con.cursor()
                  q="select * from {}".format(row[2])
                  res1.execute(q)

                  table=Table(show_header=True,header_style="bold magenta")

                  table.add_column('Roll_no',justify='center')
                  table.add_column('Name',justify='center')
                  table.add_column('Active',justify='center')
                    
                  for row1 in res1.fetchall():
                    table.add_row(str(row1[0]),str(row1[1]),str(row1[2]))

                  d,m,y=row[2][2:3],row[2][4:5],row[2][6:10]
            
                  print("\n\tAttendance Report:{:02d}-{:02d}-{:02d}".format(int(d),int(m),int(y)))
                  console.print(table)
                 

          print('\n\n')

      def update(self,tb,roll):            # update the attendance details(based on user input)
          res=con.cursor()
          new_name=input("Enter the new name:")
          new_active=input("Enter the new present status 'yes' or 'no' :")
          q='update {} set Name=%s,Active=%s where Roll_no=%s'.format(tb)
          res.execute(q,(new_name,new_active,roll))
          con.commit()
          print("[bold green]Attendance upadtaion successfully..![/bold green]")
    
      def delete(self,d,m,y):              # delete the attendance details(based on user input)
          res=con.cursor()
          roll=int(input("Enter the roll no for delete:"))
          q="delete from {}  where Roll_no={}".format('t'+"_"+str(d)+"_"+str(m)+"_"+str(y),roll)
          res.execute(q)
          con.commit()
          print("[bold green]Attendance Deletion successfully..![/bold green]")

      def existing_table(self):
          res=con.cursor()
          while True:
            date=input("Enter the date:")
            month=input("Enter the month number:")
            year=input("Enter the Year:")
            tb='t'+'_'+str(date)+'_'+str(month)+'_'+str(year)
            roll_no=int(input("Enter the roll no:"))
            name=input("Enter the name:")
            active=input("Enter the active status if present type 'yes' or type 'no' :")
            q="insert into {} values(%s,%s,%s)".format(tb)
            res.execute(q,(roll_no,name,active))
            con.commit()
            print()
            print("[bold green]Attendance added successfully..![/bold green]")
            print()
            cancel=int(input("Enter '0' to exit from adding attendance or Enter '1' to continue.. "))
            if cancel==0:break
             
s=santhosh() #create a object for class santhosh

if s.connection():

    while True:

            print("[bold magenta]----Add Attendance-----[/bold magenta]")

            date=input("Enter the date:")
            month=input("Enter the month number:")
            year=input("Enter the Year:")

            p=s.create("t"+"_"+str(date)+"_"+str(month)+"_"+str(year))
            print("[bold yellow]0[/bold yellow].Exit from attendance \n[bold yellow]1[/bold yellow].continue")
            go=int(input("Enter:"))
            print()

            while p!='p':
                roll_no=int(input("Enter the roll no:"))
                name=input("Enter the name:")
                active=input("Enter the active status if present type [bold yellow]'yes'[/bold yellow] or type [bold yellow]'no'[/bold yellow] :")

                s.add(roll_no,name,active,'t'+"_"+str(date)+"_"+str(month)+"_"+str(year))
                
                print("[bold yellow]0[/bold yellow].Exit from adding attendance \n[bold yellow]1[/bold yellow].continue...")
                cancel=int(input("Enter:"))
                
                if cancel==0:
                    break

                elif cancel==1:
                    roll_no=int(input("Enter the roll no:"))
                    name=input("Enter the name:")
                    print("Enter the active status if present type [bold yellow]'yes'[/bold yellow] or type [bold yellow]'no'[/bold yellow]")
                    active=input("Enter:")

            while go==0:
                print("1.Show Attendance report")
                print("2.Update Attendance report")
                print("3.Delete Attendance report")
                print("4.Add attendance to the existing one")
                print("5.Exit:")

                n=int(input("Enter:"))

                if n==1:
                    
                    print("Enter [bold yellow]'f'[/bold yellow] for filter or [bold yellow]'a'[/bold yellow] for all")
                    f=input("Enter:")

                    if f=='f':
                        s_d=int(input("enter the date:")) # for example : 1
                        s_m=input("Enter the month number:")  #for example :2 
                        s_y=int(input("Enter the year:")) # for example :2022
                        s.show(s_d,s_m,s_y)
                    elif f=='a':
                        s.show()

                elif n==2:

                        u_d=int(input("enter the date:")) # for example : 1
                        u_m=input("Enter the month number:")  #for example :2 
                        u_y=int(input("Enter the year:")) # for example :2022
                        roll_no=int(input("Enter the roll no to Update:"))
                        s.update('t'+'_'+str(u_d)+'_'+str(u_m)+'_'+str(u_y),roll_no)

                elif n==3:

                        d_d=int(input("enter the date:")) # for example : 1
                        d_m=input("Enter the month number:")  #for example :2 
                        d_y=int(input("Enter the year:")) # for example :2022
                        s.delete(d_d,d_m,d_y)

                elif n==4:
                        print()
                        s.existing_table()

                elif n==5:

                    print("\n\t\t\t\t[bold green]Thank You![/bold green]\n")
                    quit()
