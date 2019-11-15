class LinuxCmd:
    PYTHON = "python"
    LS = "ls"
    RSYNC = "rsync {option}"
    TO_DEV_NULL = "/dev/null"

    class compress:
        TAR = "tar czf"
        ZIP = "zip"

    class extract:
        TAR = "tar xzf"
        ZIP = "unzip"

class WindowsCmd:
    PYTHON = "C:/Python27/python.exe"


class GetLinuxCmd:
    GIT_RESET = "git clean -fdx && git reset --hard"
    VM_LIST_ALL = "vboxmanage list vms"
    VM_LIST_RUNNING = "vboxmanage list runningvms"
    SVN_UPDATE = "svn update"

    @staticmethod
    def turnoff_vm(vm_name):
        return "vboxmanage controlvm {0} poweroff".format(vm_name)

    @staticmethod
    def tar_extract(package):
        return "{0} {1}".format(LinuxCmd.extract.TAR, package)

    @staticmethod
    def tar_compress(package, folder):
        return "{0} {1} {2}".format(LinuxCmd.compress.TAR, package, folder)

    @staticmethod
    def git_merge(project_path):
        return "cd {0} && git rebase origin/master".format(project_path)

    @staticmethod
    def chmod_x(package):
        return "chmod +x {0}".format(package)

    @staticmethod
    def rename(old_name, new_name):
        return "mv {0} {1}".format(old_name, new_name)

    @staticmethod
    def execute_in_dir(directory, cmd):
        return "cd {0}; {1}".format(directory, cmd)


linux_cmd_getter = GetLinuxCmd()


class GetName:
    def tar_package(self, name):
        return "{0}.tar.gz".format(name)

    def suffix_tgz(self, name):
        return "{0}.tgz".format(name)

    def suffix_json(self, name):
        return "{0}.json".format(name)

    def suffix_excel(self, name):
        return "{0}.xls".format(name)

    def suffix_text(self, name):
        return "{0}.txt".format(name)


linux_name_getter = GetName()
