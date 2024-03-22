class ArgumentBadValueError(Exception):
    """Exception raised for errors in the arguments value input.

    Attributes:
        argument_name -- arguments name
    """

    def __init__(self, argument_name):
        self.argument_name = argument_name
        self.message = f'Bad value for key {argument_name}'
        super().__init__(self.message)

