from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp, sp
import pymysql

# CLass For Income Statement Screen
class IncomeStatementScreen(Screen):
    def add_income_statement_to_db(self):
        con = pymysql.connect(host="LocalHost",  user="root",
                              password="JawadAhmed", db="General_Journal_information")
        mycursor = con.cursor()
        mycursor.execute(
            "SELECT account_title, account_type, total FROM balance_sheet_accounts ")
        balance_sheet_data = mycursor.fetchall()
        acc_type_check = ["Revenue Account", "Expense Account"]
        income_table_row = []
        dummy_list = ["", "", ""]
        for acc_type in acc_type_check:
            for tupl in balance_sheet_data:
                if (acc_type == tupl[1]):
                    dummy_list[0] = tupl[0]
                    dummy_list[1] = tupl[1]
                    dummy_list[2] = tupl[2]
                    dummy_list = tuple(dummy_list)
                    income_table_row.append(dummy_list)
                    dummy_list = list(dummy_list)
        # Clean Table
        mycursor.execute("DELETE FROM income_statement_data")
        for tupl in income_table_row:
            query = "INSERT INTO income_statement_data(account_title, account_type, total_amount) VALUES (%s,%s,%s)"
            vl = (tupl[0], tupl[1], tupl[2])
            mycursor.execute(query, vl)
            con.commit()
    def display_income_statement(self):
        con = pymysql.connect(host="LocalHost",  user="root",
                              password="JawadAhmed", db="General_Journal_information")
        mycursor = con.cursor()
        spacer = "  "
        income_statement_row = []
        dummy_list = ["", ""]
        income_statement_head =[("Revenue ", dp(70)), ("Expenses", dp(70))]

        mycursor.execute('SELECT account_title, total_amount FROM income_statement_data WHERE account_type=%s', 'Revenue Account')
        income_statement_data = mycursor.fetchall()
        income_statement_row = []
        dummy_list = ["", ""]
        total = 0
        spacer = "  "
        for tupl in income_statement_data:
            dummy_list[0] = spacer + tupl[0] + spacer + tupl[1]
            total = int(tupl[1])
            dummy_list = tuple(dummy_list)
            income_statement_row.append(dummy_list)
            dummy_list = list(dummy_list)
        # Expense
        dummy_list = ["", ""]
        rev_total = total
        total = "Total Revneues: " + spacer + spacer + str(rev_total)
        dummy_list[0] = total
        dummy_list = tuple(dummy_list)
        income_statement_row.append(dummy_list)
        dummy_list = list(dummy_list)
        dummy_list = ["", ""]
        for i in range(len(income_statement_row)):
            income_statement_row[i] = list(income_statement_row[i])
        
        mycursor.execute('SELECT account_title, total_amount FROM income_statement_data WHERE account_type=%s', 'Expense Account')
        income_statement_data = mycursor.fetchall()
        counter = 0
        total = 0
        for tupl in income_statement_data:
            if (counter == len(income_statement_row)):
                dummy_list[1] = spacer + tupl[0] + spacer + tupl[1]
                total += int(tupl[1])
                dummy_list = tuple(dummy_list)
                income_statement_row.append(dummy_list)
                dummy_list = list(dummy_list)
            else:
                income_statement_row[counter][1] = spacer + tupl[0] + spacer + tupl[1]
                total += int(tupl[1])
                counter += 1
        exp_total = total
        total = "Total Expenses: " + spacer + spacer + str(exp_total)
        dummy_list = ["", ""]
        dummy_list[1] = total
        dummy_list = tuple(dummy_list)
        income_statement_row.append(dummy_list)
        dummy_list = list(dummy_list)
        net_income = rev_total - exp_total
        if (net_income < 0):
            net_income = "Net Loss: " + spacer + spacer + spacer + str(net_income)
        else:
            net_income = "Net Profit: " + spacer + spacer + spacer + str(net_income)
        dummy_list = ["", ""]
        dummy_list[0] = net_income
        dummy_list = tuple(dummy_list)
        income_statement_row.append(dummy_list)
        dummy_list = list(dummy_list)
        for i in range(len(income_statement_row)):
            income_statement_row[i] = tuple(income_statement_row[i])
        income_statement = MDDataTable(
            size_hint=(0.6, 0.7),
            use_pagination=True,
            column_data=income_statement_head,
            row_data=income_statement_row,
            elevation=2,
        )

        self.manager.ids.income_statement.ids.income_statement_table.add_widget(income_statement)
        con.commit()
        con.close()
