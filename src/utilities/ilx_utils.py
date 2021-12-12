class Utils:

    @staticmethod
    def generate_url(uri, **kwargs):
        for arg in kwargs:
            uri += '/' + str(kwargs[arg])
        return uri
