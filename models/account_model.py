class Account(object):
    def __init__(self, cookie, username, password, newPassword, status):
        self.cookie = cookie
        self.username = username
        self.password = password
        self.newPassword = newPassword
        self.status = status