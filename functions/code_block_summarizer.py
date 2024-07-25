import sys
import os
import streamlit as st
# Add the path to YourProject to sys.path
project_path = os.path.dirname(os.path.dirname(__file__))
sys.path.append(project_path)

from langchain.text_splitter import (
    RecursiveCharacterTextSplitter,
    Language,
)
from utils.llm import call_llm
from utils.cost_calc import calculate_cost


SUMMARIZER_PROMPT = """
Examine the HTML code snippet provided below:
{CODE_BLOCK}

Compose a concise, non-technical summary without delving into HTML, CSS, or JavaScript details. \
Describe the overall functionality of the code and highlight the visible elements, avoiding technical language. \
Do not provide information related to the underlying technologies; focus solely on the code's purpose and the elements it presents.

Additional Considerations:
* Content Structure: Mention if there's a discernible structure or hierarchy within the code.
* User Interface Elements: Identify and describe any visible components or elements that users may interact with.
* Functionality: Summarize the primary purpose or function of the code, focusing on its intended outcomes.
"""

SUMMARIZER_CONFIG = {
    "model": "gpt-4o",
    "chunk_size": 12000,
    "chunk_overlap": 0,
    "temperature": 0.1,
    "max_tokens": None,
    "response_format": "text",
}

def summarizer_function(html_code_block, config):

    html_splitter = RecursiveCharacterTextSplitter.from_language(
        language=Language.HTML,
        chunk_size=config["chunk_size"],
        chunk_overlap=config["chunk_overlap"]
    )

    html_docs = html_splitter.create_documents([html_code_block])

    total_cost = 0
    summary_list = []

    for html_chunk in html_docs:
        prompt = SUMMARIZER_PROMPT.format(CODE_BLOCK = html_chunk)
        llm_output = call_llm(
            conversation=prompt,
            model=config['model'],
            temperature=config['temperature'],
            response_format=config['response_format']
        )

        if llm_output['finish_reason'] == 'stop':
            chunk_summary = llm_output['response_generated'].content
            summary_list.append(chunk_summary)

            chunk_cost = calculate_cost(llm_output['token_usage'], model=config['model'])
            total_cost += chunk_cost['total_cost']

    final_summary = "\n".join(summary_list)

    return final_summary, total_cost

# # Example
# html_code_block = """
# <div class="view_div_decorator base_view_no_view_top_container"><div class="base_view_container"><form method="post" action="/cgi/login" name="vpnForm" autocomplete="off" style="magin:0" id="vpnForm"><div id="ctl08_loginAgentCdaHeaderText2" class="CTX_ContentTitleHeader login_page">PIMCO Remote Access -- Please log on</div><div class="field clearfix CredentialTypeusername"><div class="left"><span class="plain input_labels form_text" id="User_name">User name</span></div><div class="right"><input type="text" id="Enter user name" class="prePopulatedCredentials" autocomplete="off" spellcheck="false" name="a2846756235806483" size="30" maxlength="127" width="180px" autofocus="autofocus" title="Enter user name"><input id="dummy_username" name="a4589405952229673" type="text" style="display:none"></div></div><div class="field clearfix CredentialTypepassword"><div class="left"><span class="plain input_labels form_text" id="Password">Password</span></div><div class="right"><input type="password" id="dummy_pass1" name="a6442027923823698" style="display:none"><input type="password" id="passwd" class="prePopulatedCredentials" autocomplete="off" spellcheck="false" name="a5267119956436579" size="30" maxlength="127" width="180px"></div></div><div class="field clearfix CredentialTypepassword"><div class="left"><span class="plain input_labels form_text" id="Password2">Pin+Token:</span></div><div class="right"><input type="password" id="dummy_pass2" name="a5836195608198522" style="display:none"><input type="password" id="passwd1" class="prePopulatedCredentials" autocomplete="off" spellcheck="false" name="a5997215735863678" size="30" maxlength="127" width="180px"></div></div><div class="field CredentialTypenone"></div><div class="field buttons"><div class="left"></div><div class="right"><input type="submit" id="Log_On" value="Log On" class="custombutton login_page"></div></div></form></div></div>
# """
# final_code_block_summary = summarizer_function(html_code_block, SUMMARIZER_CONFIG)
# print(final_code_block_summary)


@st.cache_data(ttl="8h")
def st_summarizer_function(html_code_block, SUMMARIZER_CONFIG):
    return summarizer_function(html_code_block, SUMMARIZER_CONFIG)
