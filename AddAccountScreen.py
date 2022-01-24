from logging import warning
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.uix.button import MDRectangleFlatIconButton,  MDFlatButton
from kivymd.uix.dialog import MDDialog
import pymysql

class AddAccountsScreen(Screen):
    # Function That will add data to a data base
    def Add_Account_Info_To_db(self, account_title, account_type, account_description):
        if (account_title.text != "" and account_type.text != ""):
            con = pymysql.connect(host="LocalHost",  user="root",
                                password="JawadAhmed", db="General_Journal_information")
            mycursor = con.cursor()
            query = "INSERT INTO accounts_info(account_title, account_type, account_description) VALUES (%s,%s,%s)"
            vl = (account_title.text, account_type.text, account_description.text)
            mycursor.execute(query, vl)
            con.commit()
            con.close()
            # Clear the Fields
            account_title.text = ""
            account_type.text = ""
            account_description.text = ""
        else:
            close_button = MDFlatButton(
                text='Close', on_release=self.close_dialog)
            show_warning = "Please Fill All The Fields"
            self.dialog = MDDialog(title='Empty Fields', text=show_warning, size_hint=(0.7, 1),
                                   buttons=[close_button])
            self.dialog.open()
    # Close the dialog box
    def close_dialog(self, obj):
        self.dialog.dismiss()