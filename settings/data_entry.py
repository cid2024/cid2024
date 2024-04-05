class data_entry:
    def __init__(self, typename = "None"):
        self.typename = typename
        self.attributes = {}

    def __str__(self):
        problem_str = "{"

        for key, value in self.attributes.items():
            if len(problem_str) > 1:
                problem_str += ", "
            problem_str += str(key) + " : " + str(value)

        problem_str += "}"

        return problem_str
    
    def set_attribute(self, key, value):
        self.attributes[key] = value
    
    def get_attribute(self, key):
        return self.attributes[key]
