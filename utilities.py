
class Utilities:
    @staticmethod
    def escape_markdown_v2(text:str) -> str:
        escape_chars = '_[]()~>#+-=|{}.!' # `*
        server_valid = ''.join("\\" + char if char in escape_chars else char for char in text)
        return server_valid.replace('**', '*')