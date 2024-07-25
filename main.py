import re
import streamlit as st
from functions.feature_finder import st_scrape_and_extract_features, FEATURE_FINDER_CONFIG
from functions.code_block_summarizer import st_summarizer_function, SUMMARIZER_CONFIG
import pandas as pd
from utils.extract_codeblock_from_xpath import extract_code_block
from functions.test_generation import (
    st_create_additional_test_case,
    st_create_initial_test_case,
    TEST_GEN_CONFIG
    )
from functions.code_generation import st_generate_code, CODE_GEN_CONFIG
from utils.fetch_scenarios_list import fetch_scenarios_list, generate_string_from_scenario, fetch_feature_header
from utils.json_to_gherkin import parse_assistant_output
from utils.download_md import create_download_button

def on_click_button():
    st.session_state.clear()

st.markdown("## Find Features")
st.write("Hint: Enter URL if the web page contains single feature. Enter part of DOM structure if web page contains multiple features.")
col_1, col_2 = st.columns([1,3])
code_or_url = col_1.selectbox(
    "Select URL/DOM structure",
    ["URL", "DOM structure"],
    index=0,
    on_change=on_click_button,
)
if code_or_url == None:
    st.stop()

if code_or_url == "URL":
    url_to_scrape = col_2.text_input("Enter the URL to find features.")

    if url_to_scrape == "":
        st.warning("Enter URL!")
        st.stop()

    resulting_features_list, cost_feature_finder, html_text = st_scrape_and_extract_features(url_to_scrape, FEATURE_FINDER_CONFIG)

    # Remove xpaths that does not parse correctly
    for xpath in resulting_features_list:
        if not extract_code_block(html_text, xpath["xpath"]):
            resulting_features_list.remove(xpath)

    df_feature_list = pd.DataFrame(resulting_features_list)
    st.write(df_feature_list)

    st.markdown("## Select the Feature")
    selected_feature = st.selectbox("Select Feature to Summarize:", df_feature_list['name'], index=None,on_change=on_click_button)

    if selected_feature == None:
        st.warning("Select Feature")
        st.stop()

    selected_XPath = df_feature_list[df_feature_list['name'] == selected_feature]['xpath'].values[0]

    code_block = extract_code_block(html_text, selected_XPath)
else:
    code_block = col_2.text_input("Enter the DOM structure to find features.")

    if code_block == "":
        st.warning("Enter DOM structure")
        st.stop()

if code_block == "":
    st.stop()
    
final_code_block_summary, cost_summarization  = st_summarizer_function(code_block, SUMMARIZER_CONFIG)

st.markdown("## Code Block Summary")
edited_summary = st.text_area("Generated Summary: ", final_code_block_summary)

st.markdown("### Feature File")

# Run the loop until the user clicks on the button
# if 'generate_button' in st.session_state and st.session_state["generate_button"]:

gherkin_syntax = ""

# Generation and Download buttons
col1, col2, _ = st.columns([1,2,1])
generate_button = col1.button("Generate Test Cases")

if 'messages' in st.session_state:
    with col2:
        create_download_button(gherkin_syntax, "_Feature.md")


if generate_button:
    if 'test_gen_count' in st.session_state:
        messages = st.session_state['messages']
        total_cost_test_gen = st.session_state['total_cost_test_gen']
        # Run additional test case generation using the output from the previous step
        _, cost_test_generation, messages = st_create_additional_test_case(messages, TEST_GEN_CONFIG)
        total_cost_test_gen += cost_test_generation

        #addition
        st.session_state['test_gen_count'] += 1
        st.session_state['messages'] = messages
        st.session_state['total_cost_test_gen'] = total_cost_test_gen
    else: #first time
        # Run the initial test case generation
        _, cost_test_generation, messages = st_create_initial_test_case(edited_summary, TEST_GEN_CONFIG)

        #initialize
        st.session_state['test_gen_count'] = 1
        st.session_state['messages'] = messages
        st.session_state['total_cost_test_gen'] = cost_test_generation

if 'messages' in st.session_state:
    gherkin_syntax = parse_assistant_output(st.session_state['messages'])
    # Display the final result
    st.code(gherkin_syntax, language='gherkin')


# st.write(st.session_state['messages'])
if 'messages' not in st.session_state:
    st.stop()
st.markdown("### Code Generation")


scenatio_list = fetch_scenarios_list(st.session_state["messages"])

selected_scenario_name = st.selectbox("Select scenario to generate code", [scenario['scenario_title'] for scenario in scenatio_list], index=None)
if selected_scenario_name != None:
    scenario = next((scenario for scenario in scenatio_list if scenario['scenario_title'] == selected_scenario_name), None)
    scenario_str = generate_string_from_scenario([scenario])
    feature_header = fetch_feature_header(st.session_state["messages"])
    

    stepdefinition_file, locator_file, implementation_file, code_gen_cost = st_generate_code(feature_header+scenario_str,code_block,CODE_GEN_CONFIG)
    # stepdefinition_file, locator_file, implementation_file= "","",""
    try:
        t = re.search(r"`java\n(.*?)`", stepdefinition_file, re.DOTALL).group(1)
        st.markdown("#### StepDefinition File")
        st.code(t, language='java')
        st.markdown("#### Implementation File")
        st.code(re.search(r"`java\n(.*?)`", implementation_file, re.DOTALL).group(1), language='java')
        st.markdown("#### Locator File")
        st.code(re.search(r"`java\n(.*?)`", locator_file, re.DOTALL).group(1), language='java')
    except:
        st.markdown("#### StepDefinition File")
        st.code(stepdefinition_file, language='java')
        st.markdown("#### Implementation File")
        st.code(implementation_file, language='java')
        st.markdown("#### Locator File")
        st.code(locator_file, language='java')
