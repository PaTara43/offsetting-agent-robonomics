"""
Custom exceptions used in the project.

"""


class FailedToUploadFile(Exception):
    """
    Failed to upload a file to Crust Network.
    """

    pass


class FailedToPinFile(Exception):
    """
    Failed to upload a file to Crust Network.
    """

    pass


class InvalidIPFSCIDFormat(Exception):
    """
    Invalid IPFS cid format. The right example: QmZ4tDuvesekSs4qM5ZBKpXiZGun7S2CYtEZRB3DYXkjGx.
    """

    pass
