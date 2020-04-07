import requests
import unittest
import os
import time


"""User Login Test"""
class LoginTest(unittest.TestCase):
    def setUp(self):
        self.url = "http://0.0.0.0:5000/login"
        self.success_str = "You are now logged in"
        self.fail_str = {
            "UserNotFound": "Username not found",
            "PasswordWrong": "Invalid login",
            "Unauthorized": "Unauthorized, Please login"
        }

    def test_login_success(self):
        data = {
            "username": "sherry",
            "password": "123456",
        }
        res = requests.post(self.url, data = data)
        self.assertEqual(self.success_str in res.text, True)

    def test_username_not_found(self):
        data = {
            "username": "marc",
            "password": "123456",
        }
        res = requests.post(self.url, data = data)
        self.assertEqual(self.fail_str["UserNotFound"] in res.text, True)

    def test_password_invalid(self):
        data = {
            "username": "sherry",
            "password": "00",
        }
        res = requests.post(self.url, data = data)
        self.assertEqual(self.fail_str["PasswordWrong"] in res.text, True)

    def test_login_time_out(self):
        data = {
            "username": "sherry",
            "password": "123456",
        }
        res = requests.post(self.url, data = data)
        start = time.time()
        cookies = res.cookies
        # wait for 2 minutes
        while time.time()-start <=2.1*60:
            continue
        # test if can vist a page requiring login
        res = requests.get("http://0.0.0.0:5000/dashboard", cookies=cookies)
        self.assertEqual(self.fail_str["Unauthorized"] in res.text, True)

"""Email File Upload Test"""
class EmailUpload(unittest.TestCase):
    def setUp(self):
        self.url = "http://0.0.0.0:5000/addemail"
        self.filepath = "test_file"
        self.success_str = {
            "Upload": "Email Loaded",
            "Visit": "Upload Email File (txt)"
        }
        self.fail_str = {
            "Unauthorized": "Unauthorized, Please login",
            "FileTypeError": "Only txt file is supported",
            "DuplicateError": "The file has existed",
            "NoneFileError": "Choose a file from you folder"
        }

        # login to get cookies
        self.userdata = {
            "username": "sherry",
            "password": "123456",
        }
        res = requests.post("http://0.0.0.0:5000/login", data = self.userdata)
        self.cookies = res.cookies

    """Visit the page without login"""
    def test_unauthorized_visit(self):
        res = requests.get(self.url)
        self.assertEqual(self.fail_str['Unauthorized'] in res.text, True)

    """Visit the page after login"""
    def test_authorized_visit(self):
        res = requests.get(self.url, cookies=self.cookies)
        self.assertEqual(self.success_str['Visit'] in res.text, True)

    """Attention: use a different file for each running"""
    def test_success_upload(self):
        print('\n\nAttention! To test the successful case of email upload, use a different file for each running. (Change the file name in Line 94.)\n\n')
        path = os.path.join(self.filepath,'61257')
        files = {'file': open(path, 'rb')}
        res = requests.post(self.url, files=files, cookies=self.cookies)
        self.assertEqual(self.success_str['Upload'] in res.text, True)

    """Upload a file with a wrong type"""
    def test_filetype_error(self):
        path = os.path.join(self.filepath,'12345.csv')
        files = {'file': open(path, 'rb')}
        res = requests.post(self.url, files=files, cookies=self.cookies)
        self.assertEqual(self.fail_str['FileTypeError'] in res.text, True)

    """Upload the same file twice by the same user"""
    def test_duplicate_error(self):
        path = os.path.join(self.filepath,'61256')
        files = {'file': open(path, 'rb')}
        res = requests.post(self.url, files=files, cookies=self.cookies)
        res = requests.post(self.url, files=files, cookies=self.cookies)
        self.assertEqual(self.fail_str['DuplicateError'] in res.text, True)


    # def test_nonfile_error(self):
    #     files = {'file': None}
    #     res = requests.post(self.url, files=files, cookies=self.cookies)
    #     self.assertEqual(self.fail_str['NoneFileError'] in res.text, True)

# To be continued



if __name__ == '__main__':
    unittest.main(warnings='ignore')
