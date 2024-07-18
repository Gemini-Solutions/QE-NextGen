import sys
import os
from utils.llm import call_llm
from utils.cost_calc import calculate_cost
import streamlit as st

project_path = os.path.dirname(os.path.dirname(__file__))
sys.path.append(project_path)

CODE_GENERATION_PROMPT_1 = """
{FEATURE_STRING}
Given the feature file, generate a step definition file in java from it. All steps defined in feature file must map with methods in step definition file. 
Example of Step Definition file for reference purpose is given below:

package stepdefinitions;
import implementation.FABImplementation;
import io.cucumber.java.en.Given;
import io.cucumber.java.en.When;
import io.cucumber.java.en.Then;

public class FABStepDefinition {{
    public FABImplementation fabImplementation = new FABImplementation();

    @Given("user is on the home page")
    public void launchUrl(){{
        fabImplementation.launchUrl(url);
    }}

    @When("user clicks on login button")
        public void userClicksOnLoginButton() {{
            fabImplementation.clickOnLoginButton();
    }}

    @Then("username and password fields should appear")
        public void verifyLoginWindowAppears() {{
            fabImplementation.verifyLoginElements();
    }}

    @Then("close the browser")
    public void closeBrowser(){{
        fabImplementation.closeBrowser();
    }}
}}

The above code is just an example. Do not blindly copy this.
Add necessary import statements. Return only the java code and nothing else.

It is mandatory to follow the rules given below:
1. The name of step definition file must be FABStepDefinition.
2. Keep the package and imports same in all cases.
3. The step definition file must contain a launchUrl method as the first method and a closeBrowser method at the end.
    @Given("the user is on the home page")
    public void launchUrl(){{
        String url = ""; // give the URL here that you want to launch
        fabImplementation.launchUrl();
    }}

    @Then("close the browser")
    public void closeBrowser(){{
        fabImplementation.closeBrowser();
    }}

Most Important Request: 
1. If the {FEATURE_STRING} contains "Verify the presence of login button", then generate the step definition file as given below:
public class FABStepDefinition {{
    public FABImplementation fabImplementation = new FABImplementation();
    
    @Given("the user is on the home page")
    public void launchUrl(){{
        String url = ""; // give the URL here that you want to launch
        fabImplementation.launchUrl(url);
    }}

    @Then("the login button should be visible on the home page")
        public void verifyLoginBtn() {{
            fabImplementation.verifyLoginBtn();
    }}

    @Then("close the browser")
    public void closeBrowser(){{
        fabImplementation.closeBrowser();
    }}
}}

2. If the {FEATURE_STRING} contains "Verify the click functionality of the login button", then generate the step definition file as given below:
public class FABStepDefinition {{
    public FABImplementation fabImplementation = new FABImplementation();
    
    @Given("the user is on the home page")
    public void launchUrl(){{
        String url = ""; // give the URL here that you want to launch
        fabImplementation.launchUrl();
    }}

    @When("user clicks on the login button")
    public void userClicksOnLoginButton() {{
        fabImplementation.clickOnLoginButton();
    }}

    @Then("user should successfully get redirected to another page")
        public void verifyLoginRedirection(String homeUrl) {{
            fabImplementation.verifyLoginRedirection(homeUrl);
    }}

    @Then("close the browser")
    public void closeBrowser(){{
        fabImplementation.closeBrowser();
    }}
}}
"""

CODE_GENERATION_PROMPT_2 = """
Create a locator file that will store the xpaths of the required HTML elements. Use FABLocators as locator file name. 
The html code block is given below:
{CODE_BLOCK}
Example of locator file for reference purpose is given below:
package locators;
public class FABLocators {{
    public static By loginButton = By.xpath("//span[text()='Login with Gemini mail!']");
    public static By firstName = By.xpath("//input[contains(@class,'first-name')]");
    public static String textField = "//input[@id='email']";
}}

Note:
The above code is just an example. Do not blindly copy this.
Add necessary import statements and return only the java code and nothing else.

If feature contains login functionality, then create the following locator file:
public class FABLocators {{
    public static By loginButton = By.xpath("//button[contains(text(),'Login')]");
}}
"""

CODE_GENERATION_PROMPT_3 = """ 
Now, generate an implementation file which should contain the main methods that will be called from Step Definition file. Use FABImplementation as file name.
One example of Implementation for reference purpose:

package implementation;
import locators.FABLocators;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;
import org.openqa.selenium.By;
import io.github.bonigarcia.wdm.WebDriverManager;
import static org.junit.Assert.*;
public class FABImplementation {{
    WebDriver driver;

    public FABImplementation() {
    }

    public FABLocators fabLocators = new FABLocators();

    public void launchUrl(String url){
        // launches Url
        driver.get(url);
    }

    public void clickOnLoginButton() {{
       // contains logic to achieve this functionality
    }}

    public void verifyLoginElements() {{
       // contains logic to achieve this functionality
    }}
}}
The implementation file should contain the code written in Selenium using java to achieve that functionality.
Use locator file objects for xpaths and add proper import statements. Return only the java code and nothing else.

The above code is just an example. Do not blindly copy this.
Add necessary import statements. Return only the java code and nothing else.

It is mandatory to follow the rules given below:
1. The name of implementation file must be FABImplementation.
2. Keep the package and imports same in all cases.
3. The implementation file must contain a launchUrl method to launch the url as the first method and a close browser method at the end in all cases.
    public void launchUrl{{
        WebDriverManager.chromedriver().setup();
        driver = new ChromeDriver();
        driver.get(url);
    }}

    public void closeBrowser(){
        driver.close();
    }

Most Important Request: 
1. If the {FEATURE_STRING} contains "Verify the presence of login button", then generate the implementation file as given below:
public class FABImplementation {{
    WebDriver driver;
    public FABImplementation() {
    }
    public FABLocators fabLocators = new FABLocators();

    public void verifyLoginBtn() {{
        WebElement loginBtn = driver.findElement(fabLocators.loginBtn);
        if(loginBtn.isDisplayed()){
            assertTrue("Login button is available on home page", true);
        }else{
            assertFalse("Login button is not available on home page", true);
        }
    }}
}}

2. If the {FEATURE_STRING} contains "Verify the click functionality of the login button", then generate the implementation file as given below:
public class FABImplementation {{
    WebDriver driver;
    public FABImplementation() {
    }
    public FABLocators fabLocators = new FABLocators();
    public void clickOnLoginButton() {{
        WebElement loginBtn = driver.findElement(fabLocators.loginBtn);
        if(loginBtn.isEnabled()){
            loginBtn.click();
        }else{
            assertFalse("Could not click on Login button successfully", true);
        }
    }}

    public void verifyLoginRedirection(String homeUrl) {{
       String url = driver.getCurrentUrl();
       assertNotEquals(url, homeUrl);
"""

CODE_GEN_CONFIG = {
    "model": "gpt-3.5-turbo-1106",
    "chunk_size": 12000,
    "chunk_overlap": 0,
    "temperature": 0.3, 
    "max_tokens": None,
    "response_format": "text"
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

# feature = """
# Feature: User Authentication
# 	The feature represents a login form with two input fields for username and password, along with a login button. The form is enclosed within a container with a specific class. The purpose of the code is to create a user interface for entering login credentials and submitting them for authentication.

# Background: Given the user is on the login page

# Scenario: Successful Login
# 	The user successfully logs in with valid credentials
# 	Given the user is on the login page
# 	When the user enters a valid username and password
# 	And clicks on the login button
# 	Then the user should be redirected to the dashboard
# """
# xpath = "//div[@id='login_credentials']"

# code_block = """
# <div class="login_container">
#    <div class="login_logo">Swag Labs</div>
#    <div class="login_wrapper">
#       <div class="login_wrapper-inner">
#          <div id="login_button_container" class="form_column">
#             <div class="login-box">
#                <form>
#                   <div class="form_group"><input class="input_error form_input" placeholder="Username" type="text" data-test="username" id="user-name" name="user-name" autocorrect="off" autocapitalize="none" value=""></div>
#                   <div class="form_group"><input class="input_error form_input" placeholder="Password" type="password" data-test="password" id="password" name="password" autocorrect="off" autocapitalize="none" value=""></div>
#                   <div class="error-message-container"></div>
#                   <input type="submit" class="submit-button btn_action" data-test="login-button" id="login-button" name="login-button" value="Login">
#                </form>
#             </div>
#          </div>
#       </div>
#       <div class="login_credentials_wrap">
#          <div class="login_credentials_wrap-inner">
#             <div id="login_credentials" class="login_credentials">
#                <h4>Accepted usernames are:</h4>
#                standard_user<br>locked_out_user<br>problem_user<br>performance_glitch_user<br>error_user<br>visual_user<br>
#             </div>
#             <div class="login_password">
#                <h4>Password for all users:</h4>
#                secret_sauce
#             </div>
#          </div>
#       </div>
#    </div>
# </div>
# """

@st.cache_data(ttl="8h")
def st_generate_code(feature,code_block, config):
    return generate_code(feature, code_block,config)
