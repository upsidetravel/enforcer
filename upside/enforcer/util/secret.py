class Secret:
    key: str
    value: str
    tags: list
    parent_directory: str
    name: str

    def __init__(self, key: str, value: str, tags: list = list):
        self.key = key
        self.value = value
        self.tags = tags

        result = key.split('/')
        self.parent_directory = result[1]
        self.name = result[2]
