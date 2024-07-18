import json
def fetch_scenarios_list(messages):
    output_list = [json.loads(entry['content']) for entry in messages if entry['role'] == 'assistant']
    scenarios_list = []
    
    for feature_dict in output_list:
        for scenario in feature_dict['scenarios_list']:
            scenarios_list.append(scenario)

    return scenarios_list

def generate_string_from_scenario(scenario_list):
    gherkin_string = ""
    for scenario in scenario_list:
        gherkin_string += f"Scenario: {scenario['scenario_title']}\n"
        gherkin_string += f"\t{scenario['scenario_description']}\n"

        for step in scenario['steps']:
            gherkin_string += f"\t{step}\n"

        gherkin_string += "\n"

    return gherkin_string

def fetch_feature_header(messages):
    output_list = [json.loads(entry['content']) for entry in messages if entry['role'] == 'assistant']
    gherkin_string = ""
    
    for feature_dict in output_list:
        # print(feature_dict)
        if 'feature_title' in feature_dict:
            gherkin_string += f"Feature: {feature_dict['feature_title']}\n"
        
        if 'feature_description' in feature_dict:
            gherkin_string += f"\t{feature_dict['feature_description']}\n\n"

        if 'background_description' in feature_dict:
            gherkin_string += f"Background: {feature_dict['background_description']}\n\n"

    return gherkin_string