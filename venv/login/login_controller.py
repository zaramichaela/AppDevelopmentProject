import hashlib
import shelve
import backend.settings as settings
from flask import flash

class admin_login_controller():
    def __init__(self):
        self.all_admins = get_all_admin()




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
            else:
                return False


    def login_admin(self, username, password):
        details = self.find_admin_username(username)
        print(details)
        print(self.all_admins)
        if(not details):
            return False
        if(hash_password(password) == details["hash"]):
            return True
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
                item["hash"] = password
                self.all_admins.append(item)
                return True
        except Exception as e:
            print(e)
            return False
        finally:
            s.close()




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
# def find_admin_username(username):
#       userhash = ''
#       s = shelve.open(settings.ADMIN_DB)
#       try:
#           userhash = s[str(username)]
#           return userhash
#       except Exception as e:
#           print(e)
#           return False
#       finally:
#           s.close()
#       return userhash

# def login_admin(username, password):
#     found_hash = find_admin_username("Zarateo")
#     password_hash = hash_password(password)
#     if(found_hash and password_hash == found_hash):
#         return True
#     else:
#         return False
#

#
# def delete_admin_account(username):
#     s = shelve.open(settings.ADMIN_DB)
#     try:
#         del s[username]
#     except:
#         print(Exception)
#         return False
#     finally:
#         s.close()
#     return True
