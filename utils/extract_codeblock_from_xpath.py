from lxml import html
from utils.error_handlers import IncorrectXpath

def convert_xpath(xpath):
    # Check if the XPath already contains 'contains'
    if "contains" not in xpath:
        # Split the XPath into the tag part and the attribute part
        xpath_components = xpath.split("[")

        # Ensure the XPath has the correct format before proceeding
        if len(xpath_components) == 2 and xpath_components[1].endswith("]"):
            # Extract the tag and attribute parts
            tag_part = xpath_components[0]
            attr_part = xpath_components[1][:-1]  # Remove the trailing ']'

            # Replace '=' with ',' in the attribute part
            attr_part = attr_part.replace("=", ",")

            # Construct the new XPath with 'contains'
            xpath = f"{tag_part}[contains({attr_part})]"

    return xpath


def extract_code_block(html_content, xpath_expression):
    """
    Extracts the HTML code block based on the provided XPath expression.

    Parameters:
    - html_content (str): The HTML content to parse.
    - xpath_expression (str): The XPath expression to select the desired elements.

    Returns:
    - str: The extracted HTML code block.
    """

    # Parse the HTML content
    tree = html.fromstring(html_content)
    # xpath_expression = convert_xpath(xpath_expression)

    # Use XPath to select the desired elements
    selected_elements = tree.xpath(xpath_expression)

    # Extract the HTML code block represented by the XPath
    if selected_elements:
        try:
            extracted_code_block = html.tostring(selected_elements[0]).decode('utf-8')
            return extracted_code_block
        except:
            return False
    else:
        return False
