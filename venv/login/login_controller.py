import hashlib
import shelve
import backend.settings as settings


class login_controller():
    def __init__(self):
        all_admins = get_all_admin()


    def get_all_admin(self):
        all = []
        s = shelve.open(settings.ADMIN_DB)
        try:
            for i in s:
                user[i] = s[i]
                all.append(user)
        except Exception as e:
            print(e)
            return False
        finally:
            s.close()
        return all

    def find_admin_username(self, username):
        try:
            hash = user[username]
            return hash
        except:
            return False


    def login_admin(self, username, password):
        found_hash = self.find_admin_username()
        password_hash = hash_password(password)
        if(found_hash and password_hash == found_hash):
            return True
        else:
            return False

def hash_password(plaintext):
    h = hashlib.sha1()
    h.update(plaintext.encode("ASCII"))
    return h.digest()

# def find_admin_username(username):
#     userhash = ''
#     s = shelve.open(settings.ADMIN_DB)
#     try:
#         userhash = s[str(username)]
#         return userhash
#     except Exception as e:
#         print(e)
#         return False
#     finally:
#         s.close()
#     return userhash

def login_admin(username, password):
    found_hash = find_admin_username("Zarateo")
    password_hash = hash_password(password)
    if(found_hash and password_hash == found_hash):
        return True
    else:
        return False

def add_admin_account(username, password):
    hash = hash_password(password)
    s = shelve.open(settings.ADMIN_DB)
    try:
        s[username] = hash
    except:
        print(Exception)
        return False
    finally:
        s.close()
    return True

def delete_admin_account(username):
    s = shelve.open(settings.ADMIN_DB)
    try:
        del s[username]
    except:
        print(Exception)
        return False
    finally:
        s.close()
    return True
