import io.cucumber.java.en.Given;
import io.cucumber.java.en.Then;
import io.cucumber.java.en.When;
import locators.Locator;
import org.openqa.selenium.WebElement;

import java.io.IOException;

import static implementation.Implement.*;

public class StepDefinitions {
    @Given("User opens the app")
    public void userOpensTheApp() throws IOException {
        capabilities();
    }

    @When("User clicks on Skip button")
    public void userClicksOnSkipButton() {
        skip();
    }

    @Then("Verifying the elements on main screen")
    public void verifyingTheElementsOnMainScreen() {
        verifyTitle();
    }

    @Given("User clicks on add button")
    public void userClicksOnAddButton() {
        clickAddButton();
    }

    @When("User creates a new note")
    public void userCreatesANewNote() {
        writeNote();
    }

    @Then("Verifying that note is created")
    public void verifyingThatNoteIsCreated() {
        verifyNote();
    }

    @Given("User opens the note")
    public void userOpensTheNote() {
        openNote();
    }

    @When("User makes changes to the note")
    public void userMakesChangesToTheNote() {
        editNote();
    }

    @Then("Verifying that changes are made")
    public void verifyingThatChangesAreMade() {
        verifyChanges();
    }

    @When("User deletes the note")
    public void userDeletesTheNote() {
        deleteNote();
    }

    @Then("Verifying that the note is deleted")
    public void verifyingThatTheNoteIsDeleted() {
        verifyDelete();
    }

    @Given("User clicks on search icon")
    public void userClicksOnSearchIcon() {
        clickSearch();
    }

    @When("User searches for a note")
    public void userSearchesForANote() {
        searchValue();
    }

    @Then("Verifying that searched note is displayed")
    public void verifyingThatSearchedNoteIsDisplayed() {
        verifySearch();
    }

    @Given("User goes back to homepage")
    public void userGoesBackToHomepage() {
        goBack();
    }

    @When("User sorts notes alphabetically")
    public void userSortsNotesAlphabetically() {
        sort();
    }

    @Then("Verifying that notes are alphabetically sorted")
    public void verifyingThatNotesAreAlphabeticallySorted() {
        verifySort();
        driver.quit();
    }
}
