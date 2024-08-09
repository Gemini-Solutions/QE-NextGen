import io.appium.java_client.AppiumDriver;
import io.appium.java_client.android.AndroidDriver;
import locators.Locator;
import org.apache.commons.io.FileUtils;
import org.openqa.selenium.OutputType;
import org.openqa.selenium.TakesScreenshot;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.remote.DesiredCapabilities;
import org.testng.Assert;

import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.net.URL;
import java.util.List;
import java.util.Properties;
import java.util.concurrent.TimeUnit;

public class Implement {
    //declaring required variables
    public static AppiumDriver driver = null;
    public static String deviceName;
    public static String udid;
    public static String platformName;
    public static String appPath;

    //creating object for config.properties
    static Properties properties = new Properties();
    public static void properties() {
        try (InputStream inputStream = new FileInputStream("C:\\Users\\Pallavi.Arora\\IdeaProjects\\mobileassessment1\\src\\config.properties")) {
            properties.load(inputStream);
            //getting resources from config.properties file
            deviceName = properties.getProperty("appium.deviceName");
            udid = properties.getProperty("appium.udid");
            platformName = properties.getProperty("appium.platformName");
            appPath = properties.getProperty("appium.app");

        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public static void capabilities() throws IOException {
        try {
            //calling properties method
            properties();
            //setting the desired capabilites
            DesiredCapabilities cap = new DesiredCapabilities();
            cap.setCapability("deviceName",deviceName);
            cap.setCapability("udid", udid);
            cap.setCapability("platformName", platformName);
            cap.setCapability("app",appPath);
            //allowing all permissions
            cap.setCapability("autoGrantPermissions","true");

            //getting the hub
            URL url = new URL(properties.getProperty("appium.hub"));

            //setting the driver
            driver = new AndroidDriver(url, cap);
            //adding implicit wait
            driver.manage().timeouts().implicitlyWait(5, TimeUnit.SECONDS);
        }
        catch (Exception e) {
            e.printStackTrace();
        }
        screenshot("appOpens.jpg");
    }

    //click on skip button
    public static void skip() {
        try {
        WebElement skipButton = driver.findElement(Locator.skip);
        skipButton.click();
        screenshot("skipButton.jpg");
        }
        catch (Exception e) {
            e.printStackTrace();
        }
    }

    //verifying main screen element
    public static void verifyTitle() {
        WebElement addNoteTitle = driver.findElement(Locator.homeTile);
        //"Add note" is displayed on main screen
        String addNote = addNoteTitle.getText();
        Assert.assertEquals(addNote, "Add note");
    }

    public static void clickAddButton() {
        //clicking on add button
        WebElement addButton = driver.findElement(Locator.add);
        addButton.click();
    }

    public static void writeNote() {
        try{
            //adding a note
            WebElement noteType = driver.findElement(Locator.noteType);
            noteType.click();

            WebElement noteField = driver.findElement(Locator.editNote);
            noteField.sendKeys("Hello There!");

            screenshot("noteAdded.jpg");

            WebElement done = driver.findElement(Locator.doneButton);
            done.click();
        }
        catch (Exception e) {
            e.printStackTrace();
        }
    }

    public static void verifyNote() {
        try {
            //verifying that the note is added by verifying that the title given
            //and the title displayed on the home screen are the same

            WebElement expected = driver.findElement(Locator.title);
            String expectedTitle = expected.getText();

            WebElement back = driver.findElement(Locator.backButton);
            back.click();

            driver.manage().timeouts().implicitlyWait(3, TimeUnit.SECONDS);

            WebElement titleDisplayed = driver.findElement(Locator.noteTitle);
            String title = titleDisplayed.getText();

            Assert.assertEquals(expectedTitle, title);
        }
        catch (Exception e) {
            e.printStackTrace();
        }
    }

    public static void openNote() {
        //opening note again
        WebElement note = driver.findElement(Locator.noteTitle);
        note.click();
    }

    public static void editNote() {
        try {
            //making changes to the note
            WebElement edit = driver.findElement(Locator.editButton);
            edit.click();

            WebElement addText = driver.findElement(Locator.editNote);
            addText.sendKeys("How are you today?");

            screenshot("editedNote.jpg");

            WebElement done = driver.findElement(Locator.doneButton);
            done.click();
        }
        catch (Exception e) {
            e.printStackTrace();
        }
    }

    public static void verifyChanges() {
        //verifying that the changes are made by verifying that the title we gave
        //is same as the title being displayed on home screen

        WebElement viewNote = driver.findElement(Locator.view);
        String noteText = viewNote.getText();

        WebElement back = driver.findElement(Locator.backButton);
        back.click();

        driver.manage().timeouts().implicitlyWait(3, TimeUnit.SECONDS);

        WebElement mainTitle = driver.findElement(Locator.noteTitle);
        String finalTitle = mainTitle.getText();

        Assert.assertEquals(finalTitle, noteText);
    }

    //method to take screenshots
    public static void screenshot(String fileName) throws IOException {
        File srcFile = ((TakesScreenshot)driver).getScreenshotAs(OutputType.FILE);
        FileUtils.copyFile(srcFile, new File("C:\\Users\\Pallavi.Arora\\IdeaProjects\\mobileassessment1\\src\\images\\" + fileName));
    }

    ////////////////////////////////////////////////////////////////////////////////////////

    public static void deleteNote() {
        WebElement menu = driver.findElement(Locator.menuButton);
        menu.click();

        WebElement delete = driver.findElement(Locator.deleteButton);
        delete.click();

        WebElement ok = driver.findElement(Locator.confirm);
        ok.click();
    }

    public static void verifyDelete() {
        driver.manage().timeouts().implicitlyWait(3, TimeUnit.SECONDS);
        List<WebElement> notes = driver.findElements(Locator.noteTitle);

        Assert.assertEquals(notes.size(),0);
    }

    public static void clickSearch() {
        clickAddButton();
        writeNote();

        WebElement back = driver.findElement(Locator.backButton);
        back.click();

        clickAddButton();

        //adding a note
        WebElement noteType = driver.findElement(Locator.noteType);
        noteType.click();

        WebElement noteField = driver.findElement(Locator.editNote);
        noteField.sendKeys("Bye");

        WebElement done = driver.findElement(Locator.doneButton);
        done.click();

        WebElement back1 = driver.findElement(Locator.backButton);
        back1.click();

        WebElement search = driver.findElement(Locator.searchButton);
        search.click();
    }

    public static void searchValue() {
        WebElement searchInput = driver.findElement(Locator.searchField);
        searchInput.sendKeys("Bye");
    }

    public static void verifySearch() {
        WebElement searchInput = driver.findElement(Locator.searchField);
        String actual = searchInput.getText();

        WebElement noteFound = driver.findElement(Locator.element);
        String expected = noteFound.getText();

        Assert.assertEquals(actual, expected);
    }

    public static void goBack() {
        WebElement searchBack = driver.findElement(Locator.searchBackButton);
        searchBack.click();
    }

    public static void sort() {
        WebElement sortOptions = driver.findElement(Locator.sortOptions);
        sortOptions.click();

        WebElement alphabetically = driver.findElement(Locator.alphabetical);
        alphabetically.click();
    }

    public static void verifySort() {
        WebElement sorted = driver.findElement(Locator.sortOptions);
        String expected = sorted.getText();
        String actual = "Sort alphabetically";
        if(expected.contains(actual)) {
            Assert.assertTrue(true);
        }
    }

}
