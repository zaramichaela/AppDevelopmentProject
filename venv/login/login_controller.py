import hashlib
from flask import flash
import pickle
from login.user_account import user_account
import backend.settings as settings
import shelve
from login.utilities import *
from login.admin_account import *

class login_controller():
    def __init__(self):
        self.all_admins = get_all_admin()
        self.all_users =  get_all_users()

    def login_user(self, username, password):
        for i in self.all_users:
            if(i.check_login(username,password)):
                if (i.get_ban_flag()):
                    flash("your account have been banned", "error")
                    return False
                return i
        flash('Wrong credentials!', "error")
        return False
    def find_user_username(self, username):
        for i in self.all_users:
            if(i.get_username() == username):
                return i
        return False
    def create_user_account(self, username , password, email):
        u1 = user_account(username, email, password)
        if(u1.save()):
            self.all_users.append(u1)
            return True
        return False

    def del_user_account(self, username):
        user = self.find_user_username(username)
        user.delete()

    def set_ban_user_flag(self,user ,flag):
        user.set_ban_flag(flag)
        user.save()

    def user_change_pass(self, username, oldpassword, newpassword):
        user = self.find_user_username(username)
        print( "username : ", username , "old password : ", oldpassword)
        correct = user.check_password(oldpassword)

        if (user and correct):
            print("change")
            self.all_users.remove(user)
            user.set_password(newpassword)
            user.save()
            self.all_users.append(user)
            flash("Your password has been changed. Please log in using your new password.", "success")
            return True
        else:
            flash("You have input the wrong password, password is not changed.", "error")
            return False

    def get_all_users(self):
        print(self.all_users)
        return self.all_users

    def find_admin_username(self, username):
        for i in self.all_admins:
            if username == i.get_username():
                return i
        return None



    def login_admin(self, username, password):
        acc = self.find_admin_username(username)
        if(not acc):
            return False
        if(acc.check_login(username, password)):
            return acc
        return False

    def create_admin_account(self, username, password):
        s = shelve.open(settings.ADMIN_DB)
        try:
            exist = self.find_admin_username(username)
            if exist:
                flash("An account with the same username exists.", "error")
                return False
            else:
                a = admin_account(username, password)
                a.save()
                self.all_admins.append(a)
                return True
        except Exception as e:
            print(e)
            return False
        finally:
            s.close()

    def find_admin_username(self, username):
        for i in self.all_admins:
            if i.get_username() == username:
                return i
        return None


    def delete_admin_account(self, id):
        username = ''
        delete_acc = None
        for i in self.all_admins:
            if i.get_adminID() == id:
                username = i.get_username()
                delete_acc = i
        i.delete()
        self.all_admins.remove(delete_acc)
        return username

    def find_admin_id(self, id):
        for i in self.all_admins:
            if i.get_adminID() == id:
                return i

        return False

    def change_admin_password(self, username, oldpassword, newpassword):
        user = self.login_admin(username, oldpassword)
        if(user):
            user["hash"] = hash_password(newpassword)
            self.create_admin_account(username, newpassword)
            flash("Password is changed", "success")
            return True
        else:
            flash("Old password is wrong", "error")
            return False

    def get_all_admins(self):
        print(self.all_admins)
        return self.all_admins



# def delete_admin_from_shelve(username):
#     s = shelve.open(settings.ADMIN_DB)
#     try:
#         del s[username]
#         return True
#     except Exception as e:
#         return False
#     finally:
#         s.close()

def hash_password(plaintext):
    h = hashlib.sha1()
    h.update(plaintext.encode("ASCII"))
    return h.digest()

#get all admin from admin_DB
def get_all_admin():
    all = []
    s = shelve.open(settings.ADMIN_DB)
    try:
        for i in s:
            #deserialize dict to object
            all.append(deserialize(s[i]))
    except Exception as e:
        print(e)
        return False
    finally:
        s.close()
    return all



def get_all_users():
    all = []
    s = shelve.open(settings.USER_DB)
    try:
        for i in s:
            all.append(deserialize(s[i]))
    except Exception as e:
        print(e)
        return False
    finally:
        s.close()
    return all
