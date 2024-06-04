import os, re


def get_textbook(code) -> list[str] | None:
    textbook_filename = "textbook_" + str(code) + ".txt"
    textbook_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", textbook_filename)

    if not os.path.isfile(textbook_path) or os.path.getsize(textbook_path) <= 0:
        return None

    textbook = open(textbook_path, "r")
    lines = textbook.readlines()

    cur_page = -1
    cur_string = ""

    textbook_pages = []

    for line in lines:
        if len(line) > 2 and line[:3] == '$$$':
            if len(cur_string) > 1:
                textbook_pages.append(cur_string[:-1])
            
            cur_string = ""
            match = re.search(r'\d+', line)  # This regex matches one or more digits
            if match:
                cur_page = int(match.group())  # Convert the matched digits to an integer
        else:
            cur_string += line

    if len(cur_string) > 1:
        textbook_pages.append(cur_string[:-1])
    
    return textbook_pages
