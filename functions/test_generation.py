import sys
import os
import streamlit as st
# Add the path to YourProject to sys.path
project_path = os.path.dirname(os.path.dirname(__file__))
sys.path.append(project_path)

from utils.llm import call_llm
from utils.cost_calc import calculate_cost
from utils.json_to_gherkin import parse_assistant_output

INITIAL_TEST_GEN_PROMPT = """
Create Gherkin syntax-based features for the following page/feature description:
{FEATURE_SUMMARY}

Important Notes: 
- Generate common possible scenarios that should cover the complete functional testing. Keep background description as given in example.
For example: To test the login functionality, possible scenarios can be:
a. user is logged in when enter correct credentials are used.
b. Correct warning/error appears when user enters incorrect credentials to login.
This is just an example. Do not blindly copy this.
If you can not think of any possible scenario, then generate atleast two different and unique scenarios in details.
- Also keep the output in JSON format as given below:
{{
"feature_title": "Title of the Feature",
"feature_description": "Description of the feature",
"background_description": "The application is open in a web browser",
"scenarios_list": [
    {{
    "scenario_title": "Title of the Scenario",
    "scenario_description": "Description of the scenario",
    "steps": [
        "Given [Preconditions or initial context]",
        "When [Actions taken by the user or system]",
        "Then [Expected outcomes or results]",
        # Additional steps or variations can be included using And, But, etc.
        "And [Another action or check]"
        "But [Exception or negation of a previous step]"
    ]
    }},
    {{
    # Scenario 2
    }}
]
}}

Most Important Note:
If I am selecting Login button as feature description, then return the following as scenarios_list:
"scenarios_list": [
    {{
    "scenario_title": "Verify the presence of login button",
    "scenario_description": "This feature will check that login button should appear when user is on home page",
    "steps": [
        "Given user is on the home page",
        "Then login button should be visible on the home page",
        "Then close the browser"
    ]
    }},
    {{
    "scenario_title": "Verify the click functionality of the login button",
    "scenario_description": "This feature will check that login button is redirecting when user clicks the button",
    "steps": [
        "Given user is on the home page",
        "When user clicks on the login button",
        "Then user should successfully get redirected to another page",
        "Then close the browser"
    ]
    }}
"""

ADD_TEST_GEN_PROMPT = """
Create an additional distinct scenario not covered above.
Keep the following format:
{{
"scenarios_list": [
    {{
    "scenario_title": "Title of the Scenario",
    "scenario_description": "Description of the scenario",
    "steps": [
        "Given [Preconditions or initial context]",
        "When [Actions taken by the user or system]",
        "Then [Expected outcomes or results]",
        # Additional steps or variations can be included using And, But, etc.
        "And [Another action or check]"
        "But [Exception or negation of a previous step]"
    ]
    }}
}}
"""

TEST_GEN_CONFIG = {
    "model": "gpt-3.5-turbo-1106",
    "chunk_overlap": 0,
    "temperature": 0, 
    "max_tokens": None,
    "response_format": "json_object"
}


def create_initial_test_case(code_block_summary, config):

    user_prompt = INITIAL_TEST_GEN_PROMPT.format(FEATURE_SUMMARY = code_block_summary)
    
    messages = [
        {"role": "system", "content": "You are a helpful assistant designed to output JSON."},
        {"role": "user", "content": user_prompt}
    ]

    llm_output = call_llm(
        conversation=messages,
        model=config['model'],
        temperature=config['temperature'],
        response_format=config['response_format']
    )

    if llm_output['finish_reason'] == 'stop':
        test_generated = llm_output['response_generated'].content
        # test_generated = json.loads(test_generated)
        messages.append({'role': 'assistant', 'content': test_generated})
        
        total_cost = calculate_cost(llm_output['token_usage'], model=config['model'])
        total_cost = total_cost['total_cost']

    return test_generated, total_cost, messages

def create_additional_test_case(messages, config):

    user_prompt = ADD_TEST_GEN_PROMPT
    messages.append({'role': 'user', 'content': user_prompt})

    llm_output = call_llm(
        conversation=messages,
        model=config['model'],
        temperature=config['temperature'],
        response_format=config['response_format']
    )

    if llm_output['finish_reason'] == 'stop':
        new_test_generated = llm_output['response_generated'].content
        # new_test_generated = json.loads(new_test_generated)
        messages.append({'role': 'assistant', 'content': new_test_generated})

        total_cost = calculate_cost(llm_output['token_usage'], model=config['model'])
        total_cost = total_cost['total_cost']

    return new_test_generated, total_cost, messages


@st.cache_data(ttl="8h")
def st_create_initial_test_case(code_block_summary, config):
    return create_initial_test_case(code_block_summary, config)


@st.cache_data(ttl="8h")
def st_create_additional_test_case(messages, config):
    return create_additional_test_case(messages, config)
