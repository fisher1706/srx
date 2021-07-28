class BaseSetup():
    def __init__(self, context):
        self.context = context
        self.logger = context.logger
        self.url = context.session_context.url
        self.data = context.data

    def add_option(self, name, value=True):
        if name not in self.options: #pylint: disable=E1101
            self.logger.error(f"Setup '{self.setup_name}' doesn't contain option '{name}'. Available options: {self.options.keys()}") #pylint: disable=E1101
        else:
            self.options[name] = value #pylint: disable=E1101

    def set_options(self, options):
        for name in options.keys(): #pylint: disable=E1101
            if name not in self.options: #pylint: disable=E1101
                self.logger.warning(f"Setup '{self.setup_name}' doesn't contain option '{name}'. Available options: {self.options.keys()}") #pylint: disable=E1101
                break
            else:
                self.options[name] = options[name] #pylint: disable=E1101
