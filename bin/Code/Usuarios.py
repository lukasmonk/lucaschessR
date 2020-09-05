from Code import Util

from Code.Config import Configuration


class User:
    name = ""
    number = 0
    password = ""


class Usuarios:
    def __init__(self):
        self.file = "%s/users.p64" % Configuration.active_folder()
        self.list_users = self.read()

    def save(self):
        Util.save_pickle(self.file, self.list_users)

    def read(self):
        if Util.exist_file(self.file):
            resp = Util.restore_pickle(self.file)
            return resp if resp else []
        return []

    def save_list(self, list_users):
        self.list_users = list_users
        self.save()
