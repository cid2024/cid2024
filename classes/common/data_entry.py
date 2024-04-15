class DataEntry:
    def __init__(self, typename = "None"):
        self.typename = typename
        self.attributes = {}

    def __str__(self):
        entry_str = "{"

        for key, value in self.attributes.items():
            if len(entry_str) > 1:
                entry_str += ", "
            entry_str += str(key) + " : " + str(value)

        entry_str += "}"

        return entry_str
    
    def set_attribute(self, key, value):
        self.attributes[key] = value
    
    def has_attribute(self, key):
        return True

    def get_attribute(self, key):
        return self.attributes[key]
