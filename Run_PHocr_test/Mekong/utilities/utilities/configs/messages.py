class StandardMessages:
    class StandartIO:
        STDOUT = "Standard ouput"
        STDERR = "Standard error"
        STDIN = "Standard input"

    class Ssh:
        GET_FILE = "Get {0} from master to {1} in {2}"
        PUT_FILE = "Put {0} from {1} to master in {2}"

class ErrorMessages:

    class FileIO:
        NO_FILE = "No such file or directory {0}, {1}"

    class Network:
        NO_ROUTE = "No route to host"
        TIMEOUT = "Connect timeout"
        TIMEOUT_DETAIL = "Failed to connect to host, time over {0}s"
        CHECK_CONNECTION_FAILED = "Check ssh connection failed. Disconnected to host!"

    class Ssh:
        EXEC_CMD = "Failed to execute command {0} on {1}"


class TestSystemMessage(object):
    """
    Store test system messages
    """

    class TestCase(object):
        """
        Store test system message relate to test case
        """
        UPDATE = "Test System update for D{0}"
