import hashlib
from flask import flash
import pickle
from login.user_account import user_account
import backend.settings as settings
import shelve



class login_controller():
    def __init__(self):
        self.all_admins = get_all_admin()
        self.all_users = get_all_users()



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
        print(username)
        self.all_users.remove(user)
        s = shelve.open(settings.USER_DB)
        try:
            del s[username]
            return True
        except Exception as e:
            print(e)
            return False
        finally:
            s.close()

    def set_ban_user_flag(self,user ,flag):
        user.set_ban_flag(flag)
        user.save()

    def user_change_pass(self, username, oldpassword, newpassword):
        user = self.login_admin(username, oldpassword)
        if (user):
            self.all_users.remove(user)
            user.set_password(newpassword)
            user.save()
            self.all_users.append(user)
            flash("Your password has been changed.", "success")
        else:
            flash("You have input the wrong password, password is not changed.", "error")
            return False

    def get_all_users(self):
        print(self.all_users)
        return self.all_users



    def find_admin_username(self, username):
        for i in self.all_admins:
            if i["username"] == username:
                return i
        return None




    def login_admin(self, username, password):
        details = self.find_admin_username(username)
        print(details)
        if(not details):
            return False
        if(hash_password(password) == details["hash"]):
            return details
        return False

    def add_admin_account(self, username, password):
        hash = hash_password(password)
        s = shelve.open(settings.ADMIN_DB)
        try:
            exist = self.find_admin_username(username)
            if exist:
                flash("An account with the same username exists.")
                return False
            else:
                s[username] = hash
                item = dict()
                item["username"] = username
                item["hash"] = hash
                self.all_admins.append(item)
                return True
        except Exception as e:
            print(e)
            return False
        finally:
            s.close()

    def find_admin_username(self, username):
        for i in self.all_admins:
            if i["username"] == username:
                return i
        return None


    def delete_admin_account(self, username):
        for i in self.all_admins:
            if(i["username"] == username):
                self.all_admins.remove(i)
                delete_admin_from_shelve(username)
                return True

        return False

    def change_admin_password(self, username, oldpassword, newpassword):
        user = self.login_admin(username, oldpassword)
        if(user):
            user["hash"] = hash_password(newpassword)
            self.add_admin_account(username, newpassword)
            flash("Password is changed", "success")
            return True
        else:
            flash("Old password is wrong", "error")
            return False

    def get_all_admins(self):
        print(self.all_admins)
        return self.all_admins


def delete_admin_from_shelve(username):
    s = shelve.open(settings.ADMIN_DB)
    try:
        del s[username]
        return True
    except Exception as e:
        return False
    finally:
        s.close()

def hash_password(plaintext):
    h = hashlib.sha1()
    h.update(plaintext.encode("ASCII"))
    return h.digest()


def get_all_admin():
    all = []
    s = shelve.open(settings.ADMIN_DB)
    try:
        for i in s:
            item = dict()
            item["username"] = i
            item["hash"] = s[i]
            all.append(item)
    except Exception as e:
        print(e)
        return False
    finally:
        s.close()
    return all







def deserialize(dict):
    try:
        return pickle.loads(dict)
    except:
        return None

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
