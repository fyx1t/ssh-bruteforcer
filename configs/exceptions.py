class ArgumentBadValueError(Exception):
    """Exception raised for errors in the arguments value input.

    Attributes:
        argument_name -- arguments name
    """

    def __init__(self, argument_name):
        self.argument_name = argument_name
        self.message = f'Bad value for key {argument_name}'
        super().__init__(self.message)


class NoKeyError(Exception):
    """Exception raised for errors in arguments.

    Attributes:
        argument_name -- arguments name
    """

    def __init__(self):
        self.message = f'For brute you need to specify ip file as well as logins and passwords files. Please, see help page for more details'
        super().__init__(self.message)
