import sys
import os
from utils.llm import call_llm
from utils.cost_calc import calculate_cost
import streamlit as st

project_path = os.path.dirname(os.path.dirname(__file__))
sys.path.append(project_path)

CODE_GENERATION_PROMPT_1 = """
{FEATURE_STRING}

Given a feature file, generate a step definition file in Java that maps all steps in the feature file to corresponding methods in the step definition file.

package stepdefinitions;
import implementation.Implementation;
import io.cucumber.java.en.Given;
import io.cucumber.java.en.When;
import io.cucumber.java.en.Then;

public class StepDefinition {{
    public Implementation implementation = new Implementation();

    @Given("the user is on the home page")
    public void launchUrl(){{
        implementation.launchUrl(url);
    }}

    @When("the user clicks on login button")
        public void userClicksOnLoginButton() {{
            implementation.clickOnLoginButton();
    }}

    @Then("username and password fields should appear")
        public void verifyLoginWindowAppears() {{
            implementation.verifyLoginElements();
    }}

    @Then("close the browser")
    public void closeBrowser(){{
        implementation.closeBrowser();
    }}
}}

Important points:
1. The above code is just an example. Do not blindly copy this code.
2. Add necessary import statements. Return only the java code and nothing else.
3. Ensure the step definition file contains launchUrl and closeBrowser methods.
    @Given("the user is on the home page")
    public void launchUrl(){{
        String url = ""; // give the URL here that you want to launch
        implementation.launchUrl();
    }}

    @Then("close the browser")
    public void closeBrowser(){{
        implementation.closeBrowser();
    }}
"""

CODE_GENERATION_PROMPT_2 = """
Create a locator file named Locators to store the XPaths of the required HTML elements from the provided HTML code block.

{CODE_BLOCK}

One example of a locator file for reference purpose is given below:

package locators;
public class Locators {{
    public static By loginButton = By.xpath("//span[text()='Login with Gemini mail!']");
    public static By firstName = By.xpath("//input[contains(@class,'first-name')]");
    public static String textField = "//input[@id='email']";
}}

Important points:
1. The above code is just an example. Do not blindly copy this code.
2. Add necessary import statements. Return only the java code and nothing else.
"""

CODE_GENERATION_PROMPT_3 = """ 
Generate an implementation file named Implementation containing the main methods to be called from the previously defined step definition file.
One example of Implementation for reference purpose:

package implementation;
import locators.Locators;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;
import org.openqa.selenium.By;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;
import io.github.bonigarcia.wdm.WebDriverManager;
import static org.junit.Assert.*;
import java.time.Duration;

public class Implementation {{
    WebDriver driver;

    public Implementation() {{
    }}

    public Locators locators = new Locators();

    public void launchUrl(String url){{
        // launches Url
        driver.get(url);
    }}

    public void clickOnLoginButton() {{
       // contains logic to achieve this functionality
    }}

    public void verifyLoginElements() {{
       // contains logic to achieve this functionality
    }}
}}

Important Points:
1. The implementation file should contain Selenium code in Java to achieve the described functionality.
2. Use the objects from the locator file for XPaths.
3. The above code is just an example. Do not blindly copy this code.
4. Add necessary import statements. Return only the Java code and nothing else.
5. Ensure that the implementation file contains launchUrl and closeBrowser methods:
    public void launchUrl{{
        WebDriverManager.chromedriver().setup();
        driver = new ChromeDriver();
        driver.get(url);
        driver.manage().window().maximize();
    }}

    public void closeBrowser(){{
        driver.close();
    }}
"""

CODE_GEN_CONFIG = {
    "model": "gpt-4o",
    "chunk_size": 12000,
    "chunk_overlap": 0,
    "temperature": 0.3,
    "max_tokens": None,
    "response_format": "text",
}

def generate_code(feature_string, code_block, config):
    prompt_1 = CODE_GENERATION_PROMPT_1.format(FEATURE_STRING=feature_string)
    prompt_2 = CODE_GENERATION_PROMPT_2.format(CODE_BLOCK = code_block)
    prompt_3 = CODE_GENERATION_PROMPT_3

    messages = [
        {"role": "system", "content": "You are a helpful assistant designed to output java code."},
        {"role": "user", "content": prompt_1}
    ]

    llm_output_1 = call_llm(
        conversation=messages,
        model=config['model'],
        temperature=config['temperature'],
        response_format=config['response_format']
    )

    code_generated = llm_output_1['response_generated'].content
    messages.append({'role': 'assistant', 'content': code_generated})
    cost = calculate_cost(llm_output_1['token_usage'], model=config['model'])
    total_cost = cost['total_cost']

    step_definition_code = code_generated.split("Implementation File")[0] + "```"

    messages.append({"role":"user", "content": prompt_2})

    llm_output_2 = call_llm(
        conversation=messages,
        model=config['model'],
        temperature=config['temperature'],
        response_format=config['response_format']
    )

    locator_code = llm_output_2['response_generated'].content
    messages.append({'role':'assistant', 'content': locator_code})
    cost = calculate_cost(llm_output_2['token_usage'], model=config['model'])
    total_cost = total_cost + cost['total_cost']

    messages.append({"role":"user", "content":prompt_3})

    llm_output_3= call_llm(
        conversation=messages,
        model=config['model'],
        temperature=config['temperature'],
        response_format=config['response_format']
    )

    implementation_code = llm_output_3['response_generated'].content
    messages.append({'role':'assistant', 'content': locator_code})
    cost = calculate_cost(llm_output_3['token_usage'], model=config['model'])
    total_cost = total_cost + cost['total_cost']

    return step_definition_code, locator_code, implementation_code, total_cost

@st.cache_data(ttl="8h")
def st_generate_code(feature,code_block, config):
    return generate_code(feature, code_block,config)
