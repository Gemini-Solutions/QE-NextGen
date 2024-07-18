Feature: PIMCO Remote Access Login
        The feature describes the login form for PIMCO Remote Access, which includes fields for username, password, and pin+token, along with a 'Log On' button for submitting the login details. The form provides a user-friendly interface for user authentication to access PIMCO's remote resources.

Background: As a user, I want to access PIMCO's remote resources securely by providing my login credentials through the Remote Access login form.

Scenario: Successful Login with Valid Credentials
        The user successfully logs in to the PIMCO Remote Access system with valid credentials.
        Given the user is on the PIMCO Remote Access login page
        When the user enters a valid username, password, and pin+token
        And clicks on the 'Log On' button
        Then the user should be redirected to the remote resources page

Scenario: Unsuccessful Login with Invalid Credentials
        The user fails to log in to the PIMCO Remote Access system with invalid credentials.
        Given the user is on the PIMCO Remote Access login page
        When the user enters an invalid username, password, or pin+token
        And clicks on the 'Log On' button
        Then an error message should be displayed indicating the invalid credentials

Scenario: Forgot Password Recovery
        The user initiates the password recovery process after forgetting the password for PIMCO Remote Access.        Given the user is on the PIMCO Remote Access login page
        When the user clicks on the 'Forgot Password' link
        And enters the registered email address for password recovery
        And completes the necessary verification steps
        Then the user should receive an email with instructions to reset the password

Scenario: Account Lockout after Multiple Failed Login Attempts
        The user's account gets locked out after multiple failed login attempts to the PIMCO Remote Access system.
        Given the user attempts to log in to the PIMCO Remote Access system
        When the user enters incorrect credentials multiple times
        Then the user's account should be locked out for a specified duration
        And the user should receive a notification about the account lockout

