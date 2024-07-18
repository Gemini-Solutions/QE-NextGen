import sys
import os
# Add the path to YourProject to sys.path
project_path = os.path.dirname(os.path.dirname(__file__))
sys.path.append(project_path)

import json
from langchain.text_splitter import (
    RecursiveCharacterTextSplitter,
    Language,
)
from utils.scrapper import (
    scrape_website_with_js
)
from utils.llm import call_llm
from utils.cost_calc import calculate_cost
from utils.error_handlers import MissingFeature
import streamlit as st

FEATURE_FINDER_PROMPT = """
You will be provided a HTML code. Your objective is to identify all the functional test cases for the given HTML code. Think about all possible positive and negative test cases that are possible.

Note:
1. Do not give the features or functionalities that aren't present in the HTML Code.
2. Do not repeat the test cases.
3. Do not hallucinate.

Present the extracted information in JSON format as follows:

{{
"feature": [
  {{"name": "Feature Name 1", "description": "Description of the feature functionality 1.", "xpath": "xpath_expression_1"}},
  {{"name": "Feature Name 2", "description": "Description of the feature functionality 2.", "xpath": "xpath_expression_2"}},
  // ... (for additional features)
]
}}

xpath expression for reference purpose is given below:
1. //tagname[contains(@attribute,'value')]
2. //tagname[@attribute='value']
3. //tagname[contains(text(),'visible text')]

Note: Do not blindly copy the xpath expressions. Create valid xpaths by yourself.

Here is the HTML Code: 
{HTML_CODE}
"""

FEATURE_FINDER_CONFIG = {
    "model": "gpt-3.5-turbo-1106",
    "chunk_size": 12000,
    "chunk_overlap": 0,
    "temperature": 0.1, 
    "max_tokens": None,
    "response_format": "json_object"
}

def scrape_and_extract_features(url, config):

    html_text = scrape_website_with_js(url)
    html_splitter = RecursiveCharacterTextSplitter.from_language(
        language=Language.HTML,
        chunk_size=config["chunk_size"],
        chunk_overlap=config["chunk_overlap"]
    )

    html_docs = html_splitter.create_documents([html_text])

    total_cost = 0
    feature_dict_list = []

    for html_chunk in html_docs:
        prompt = FEATURE_FINDER_PROMPT.format(HTML_CODE = html_chunk)

        llm_output = call_llm(
            conversation=prompt,
            model=config['model'],
            temperature=config['temperature'],
            response_format=config['response_format']
        )

        if llm_output['finish_reason'] == 'stop':
            chunk_feature_dict = json.loads(llm_output['response_generated'].content)
            if "feature" in chunk_feature_dict:   
                feature_dict_list.extend(chunk_feature_dict['feature'])
            else:
                raise MissingFeature()

            chunk_cost = calculate_cost(llm_output['token_usage'], model=config['model'])
            total_cost += chunk_cost['total_cost']

    return feature_dict_list, total_cost, html_text


@st.cache_data(ttl="8h")
def st_scrape_and_extract_features(to_extract, config):
    return scrape_and_extract_features(to_extract, config)
