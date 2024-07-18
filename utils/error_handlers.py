class MissingFeature(Exception):
    def __init__(self, message="Missing 'Feature' Key in LLM Response. Please Check"):
        self.message = message
        super().__init__(self.message)

class IncorrectXpath(Exception):
    def __init__(self, message="The Xpath provided couldn't extract any codeblocks, please check the Xpath or the codeblock"):
        self.message = message
        super().__init__(self.message)


# # Raise the custom exception
# try:
#     raise MissingFeature("Something went wrong!")
# except MissingFeature as ce:
#     print(f"Custom Error: {ce}")
