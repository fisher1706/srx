class BaseSetup():
    def __init__(self, context):
        self.context = context
        self.logger = context.logger
        self.url = context.session_context.url
        self.data = context.data

    def add_option(self, name, value=True):
        if (name not in self.options):
            self.logger.error(f"Setup '{self.setup_name}' doesn't contain option '{name}'. Available options: {self.options.keys()}")
        else:
            self.options[name] = value

