from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.uix.datatables import TableData
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp, sp
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.label import MDLabel
import pymysql

class LeidgersScreen(Screen):
    # Leidgers Display Account
    def display_leidgers(self):
        # DataBase Connection
        con = pymysql.connect(host="LocalHost",  user="root",
                              password="JawadAhmed", db="General_Journal_information")
        mycursor = con.cursor()
        # Cleaning the db
        mycursor.execute("DELETE FROM trail_balance")
        con.commit()
        mycursor.execute("SELECT company_name FROM company_name")
        company_name = mycursor.fetchall()
        company_name = company_name[0][0]
        mycursor.execute(
            "SELECT account_entry_date, account_title, debit_amount, credit_amount FROM general_journal_info")
        accounts_data = mycursor.fetchall()
        accounts_data = list(accounts_data)
        # Accounts_name has the info of all the accounts
        accounts_name = []
        for tupls in accounts_data:
            if tupls[1] not in accounts_name:
                accounts_name.append(tupls[1])
        table_row = []
        table_col = [("Date", dp(20)), ("Account Title", dp(40)),
                     ("Debit", dp(20)), ("Credit", dp(20))]
        for account in accounts_name:
            for tupls in accounts_data:
                if account == tupls[1]:
                    table_row.append(tupls)
        con.commit()
        con.close()
        dummy_list = []
        acc_name = ""
        menu_items = [
            {
                "text": i,
                "viewclass": "OneLineListItem",
                "on_release": lambda x=i: self.menu_callback(x, table_row, table_col),
            } for i in accounts_name
        ]
        self.menu = MDDropdownMenu(
            caller=self.manager.ids.leidgers_account.ids.button,
            items=menu_items,
            width_mult=4,
        )
        credit_amount = 0
        debit_amount = 0
        for account in accounts_name:
            for tupl in table_row:
                if (account == tupl[1]):
                    acc_name = tupl[1]
                    dummy_list.append(tupl[2])
                    dummy_list.append(tupl[3])
            for i in range(0, len(dummy_list)):
                # Debit Index
                if (i % 2 == 0):
                    debit_amount += int(dummy_list[i])
                # Credit Index
                else:
                    credit_amount += int(dummy_list[i])
            total = debit_amount - credit_amount
            if (total < 0):
                # Credit Balance
                credit_amount = abs(total)
                debit_amount = 0
            else:
                # Debit Balance
                debit_amount = total
                credit_amount = 0
            # Add This Data In DB
            con = pymysql.connect(host="LocalHost",  user="root",
                                  password="JawadAhmed", db="General_Journal_information")
            mycursor = con.cursor()
            query = "INSERT INTO trail_balance(account_title, debit_amount, credit_amount) VALUES (%s,%s,%s)"
            vl = (acc_name, str(debit_amount), str(credit_amount))
            mycursor.execute(query, vl)
            con.commit()
            con.close()
            total = debit_amount = credit_amount = 0
            dummy_list = []
    # Display The Leidgers
    def menu_callback(self, acc_name, table_row, table_head):
        tbl_row = []
        debit_sum = 0
        credit_sum = 0
        for tupl in table_row:
            if (acc_name == tupl[1]):
                debit_sum += int(tupl[2])
                credit_sum += int(tupl[3])
                tbl_row.append(tupl)
        total = debit_sum - credit_sum
        l = ["", "", "", ""]
        l[1] = "Total"
        if (total < 0):
            l[3] = str(abs(total))
            l = tuple(l)
            tbl_row.append(l)
        else:
            l[2] = str(total)
            l = tuple(l)
            tbl_row.append(l)
        self.leidgers_table = MDDataTable(
            size_hint=(0.6, 0.7),
            use_pagination=True,
            column_data=table_head,
            row_data=tbl_row,
            elevation=2,
        )
        self.manager.ids.leidgers_account.ids.box.add_widget(self.leidgers_table)