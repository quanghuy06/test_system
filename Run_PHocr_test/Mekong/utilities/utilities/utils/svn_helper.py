# TOSHIBA - TSDV
# Team:             PHOcr
# Author:           Luong Van Huan
# Email:            huan.luongvan@toshiba-tsdv.com
# Date create:
# Description:
import os
import pexpect
from svn import remote
from svn.local import LocalClient
from configs.credential import Credential
from baseapi.file_access import make_dir


class SvnAccountKey(object):
    PHOCR_SERVER = "svn"
    TSDV_SERVER = "svn_vc1"


class SVNStatus(object):
    ADDED = 'added'
    CONFLICTED = 'conflicted'
    DELETED = 'deleted'
    EXTERNAL = 'external'
    IGNORED = 'ignored'
    INCOMPLETE = 'incomplete'
    MERGED = 'merged'
    MISSING = 'missing'
    MODIFIED = 'modified'
    NO_MODIFICATION = ''
    NONE = 'none'
    NORMAL = 'normal'
    OBSTRUCTED = 'obstructed'
    REPLACED = 'replaced'
    UNVERSIONED = 'unversioned'


class SVNHelper:

    Accounts = SvnAccountKey

    def __init__(self, url=None, output_dir=None):
        self.url = url
        self.output_dir = output_dir
        if self.output_dir:
            self.init_output_dir()
        self.credential = Credential()
        self.__username = None
        self.__password = None
        self.remote_client = None
        self.local_client = None
        if self.url and self.output_dir:
            self.__user, self.__password = \
                self.credential.get_account_for(SvnAccountKey.PHOCR_SERVER)
        if self.url:
            self.remote_client = remote.RemoteClient(self.url,
                                                     username=self.__user,
                                                     password=self.__password)
        if self.output_dir:
            self.local_client = LocalClient(self.output_dir,
                                            username=self.__user,
                                            password=self.__password)

    def init_output_dir(self):
        if not os.path.isdir(self.output_dir):
            make_dir(self.output_dir)

    def checkout(self):
        self.remote_client.checkout(self.output_dir)

    def update(self):
        self.local_client.update()

    def add(self, file_path):
        """
        Add a file to SVN.

        Parameters
        ----------
        file_path: str
            Path to file which will be added to SVN.

        """
        self.local_client.add(file_path)

    def add_list_file(self, list_file, actor, change_number):
        list_add = []
        for file_ in list_file:
            self.add(file_)
            list_add.append(os.path.basename(file_))
        self.commit(self.get_add_message(list_add, actor, change_number),
                    list_file)

    def commit(self, message, list_files):
        """
        Update a list file to SVN.

        Parameters
        ----------
        message: str
            Message for file will be committed.
        list_files: list
            List file will be committed.

        """
        self.local_client.commit(message, list_files)

    def is_checkouted(self):
        if os.listdir(self.output_dir):
            return True
        else:
            return False

    def check_status(self):
        """
        Check status of a directory.

        Returns
        -------
        list
            List file and its status.

        """
        return self.local_client.status()

    @staticmethod
    def get_file_status(file_dir, file_name):
        """
        Get svn status of a file!

        Parameters
        ----------
        file_dir: str
            Directory contains file.
        file_name: str
            File name.

        Returns
        -------
        str:
            If file status if one of "unversioned", "added" or "modified"
        None
            If other.

        """
        local_client = LocalClient(file_dir)
        status = local_client.status()
        try:
            for stat in status:
                if os.path.basename(stat.name) == file_name:
                    file_status = stat.type_raw_name
                    return file_status
                else:
                    print "File {0} may be redundant file, please recheck!!!" \
                          "".format(file_name)
            status.next()
        except StopIteration:
            print "{0} is not changed!".format(file_name)

    @staticmethod
    def get_update_message(list_file_name, actor, change_number):
        """
        Get commit message when update a file to svn.

        Parameters
        ----------
        list_file_name: list
            List files will be updated to svn.
        actor:
            Who will update files to SVN.

        Returns
        -------
        str:
            Commit message when update list files to svn.

        """
        list_file_str = ""
        for file_name in list_file_name:
            list_file_str = list_file_str \
                                   + " {0}".format(os.path.basename(file_name))\
                                   + ","
        list_file_str = list_file_str[:-1]
        message = "{0} updates {1} for change {2} of PHOcr!" \
                  "".format(actor, list_file_str, change_number)
        print message
        return message

    @staticmethod
    def get_add_message(list_file_name, actor, change_number):
        """
        Get commit message when add a file to svn.

        Parameters
        ----------
        list_file_name: list
            List files will be added to svn.
        actor:
            Who will add files to svn.

        Returns
        -------
        str:
            Commit message when add list files to svn.

        """
        list_file_str = ""
        for file_name in list_file_name:
            list_file_str = list_file_str + " {0}".format(file_name) + ","
        list_file_str = list_file_str[:-1]
        message = "{0} adds files {1} for change {2} of PHOcr!" \
                  "".format(actor, list_file_str, change_number)
        print message
        return message

    def import_file_to_svn(self, local_path, svn_url, message, timeout=300):
        """
        Import a file on local to svn

        Parameters
        ----------
        local_path: str
            Path to file on local machine
        svn_url: str
            URL to svn destination to import file
        message: str
            Commit message for importing
        timeout: int
            Timeout for processing

        Returns
        -------
        None/int
            Return None if everything OK, otherwise there are something wrong in processing.

        """
        if not os.path.isfile(local_path):
            print ("WARN: No such file {file}".format(file=local_path))
            return

        account = self.get_account_key(url=svn_url)
        password = None
        if not account:
            print ("WARN: No account is setting up for accessing {url}".format(url=svn_url))
        elif account == self.Accounts.PHOCR_SERVER:
            username, password = self.credential.get_account_for(account)

        password_option = ""
        if password:
            password_option = "--password {password}".format(password=password)

        # Check if URL exists or not, if it already exists then delete it first.
        ls_cmd = "svn ls {url} {password}".format(url=svn_url, password=password_option)
        child = pexpect.spawn(ls_cmd, timeout=timeout)
        child.expect(pexpect.EOF)
        # If file does not exist then output of the ls command will contain error message
        if "svn: E200009" not in child.before:
            # URL already exists on SVN repository then delete it first
            delete_cmd = "svn delete {url} -m \"Delete {url} to import new one\" {password}".format(
                url=svn_url, password=password_option)
            print ("Deleting {url}".format(url=svn_url))
            child = pexpect.spawn(delete_cmd, timeout=timeout)
            child.expect(pexpect.EOF)
            if child.exitstatus:
                print (child.before)
                print ("Can not delete existing file on SVN repository!")
                return child.exitstatus
        # Import file to SVN repository
        print ("Import {file_path} to SVN under {url}".format(file_path=local_path, url=svn_url))
        import_cmd = "svn import -m \"{message}\" {file_path} {svn_url} {password}" \
                     "".format(message=message, file_path=local_path, svn_url=svn_url,
                               password=password_option)
        child = pexpect.spawn(import_cmd, timeout=timeout)
        child.expect(pexpect.EOF)
        if child.exitstatus:
            print (child.before)
            print ("Can not import file to SVN repository!")
            return child.exitstatus

    def get_account_key(self, url):
        """
        Base on url, detect which account should be used. Currently, there are two SVN
        repositories are used: SVN repo on OCR1 (10.116.41.162) and SVN repo for PHOcr team on TSDV
        server (vc1.tsdv.com.vn).

        Parameters
        ----------
        url: str
            Url to SVN repository

        Returns
        -------
        str
           Key to get right account for connecting to SVN url in account/credential.json

        """
        if url.startswith("http://10.116.41.162"):
            return self.Accounts.PHOCR_SERVER
        elif url.startswith("http://vc1.tsdv.com.vn"):
            return self.Accounts.TSDV_SERVER
        else:
            return None
