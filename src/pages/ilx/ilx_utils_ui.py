import time


class IlxUtils:

    @staticmethod
    def generate_name(name):
        timestamp = int(time.time())
        return f'{name}-{timestamp}'


if __name__ == '__main__':
    u = IlxUtils()

    # x = u.generate_name('group')
    # print(x)

    x = string = "Добро пожалов\nать!"
    print("Индекс первой буквы 'о':", string.find('\n'))


