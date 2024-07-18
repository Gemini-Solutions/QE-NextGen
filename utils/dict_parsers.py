import ast
import re

def extract_dictionary_from_text(text):
    # match = re.search(r'({.+})', text)
    text = text.replace("\n", "")
    try:
        x = ast.literal_eval(re.search('({.+})', text).group(0))
        return x

    except Exception as E:
        print(E)
        return None
    
def merge_dicts_list(list_of_dicts):
    final_dict = {}
    
    for idx, d in enumerate(list_of_dicts):
        for key, value in d.items():
            new_key = key + (f"_{idx}" if key in final_dict else "")
            final_dict[new_key] = value
    
    return final_dict