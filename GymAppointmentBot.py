# Import necessary libraries
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# from bs4 import BeautifulSoup
# import time


# Function to log in to the website
def login(username, password):
    # Initialize the web driver (Make sure you have the appropriate web driver executable for your browser)
    chrome_driver_path = 'C:\Users\emirhan.ozkan\Documents\personal\GymAppointmentBot\chromedriver.exe'
    driver = webdriver.Chrome(executable_path=chrome_driver_path)

    # Navigate to the login page
    driver.get('https://online.spor.istanbul/uyegiris')

    # Find and fill in the login form
    username_field = driver.find_element(By.ID, 'txtTCPasaport')
    password_field = driver.find_element(By.ID, 'txtSifre')
    username_field.send_keys(username)
    password_field.send_keys(password)
    password_field.send_keys(Keys.RETURN)

    # Wait for the login to be successful (you might need to add more waiting time or improve this logic)
    WebDriverWait(driver, 10).until(EC.url_to_be(
        'https://online.spor.istanbul/anasayfa'))

    return driver


def get_appointments(driver):
    # Navigate to the appointments page
    driver.get('https://online.spor.istanbul/appointments')

    # Wait for the page to load (you might need to adjust the waiting time)
    WebDriverWait(driver, 10).until(EC.url_to_be(
        'https://online.spor.istanbul/appointments'))

    # Assuming the appointments are listed in a table, find the table element
    appointments_table = driver.find_element(By.ID, 'appointments-table')

    # Extract the available appointments from the table
    available_appointments = []
    rows = appointments_table.find_elements(By.TAG_NAME, 'tr')
    for row in rows:
        # Assuming the date and time are in the first two columns of the table
        date_cell, time_cell = row.find_elements(By.TAG_NAME, 'td')[:2]
        date = date_cell.text.strip()
        time = time_cell.text.strip()
        # Check if the appointment is available (you can add more conditions here based on the website's structure)
        if 'Available' in time:
            available_appointments.append(f'{date} - {time}')

    return available_appointments


def reserve_appointment(driver, appointment_time):
    # Navigate to the appointments page
    driver.get('https://online.spor.istanbul/appointments')

    # Wait for the page to load (you might need to adjust the waiting time)
    WebDriverWait(driver, 10).until(EC.url_to_be(
        'https://online.spor.istanbul/appointments'))

    # Assuming there is a dropdown or form to select the desired appointment time
    appointment_dropdown = driver.find_element(By.ID, 'appointment-dropdown')
    appointment_dropdown.click()

    # Assuming each option in the dropdown has the format "date - time"
    # We will try to find and click the option that matches the desired appointment time
    options = appointment_dropdown.find_elements(By.TAG_NAME, 'option')
    for option in options:
        if appointment_time in option.text:
            option.click()
            break

    # Assuming there is a button to confirm the reservation
    confirm_button = driver.find_element(By.ID, 'confirm-button')
    confirm_button.click()

    # Wait for the reservation confirmation (you might need to adjust the waiting time)
    WebDriverWait(driver, 10).until(EC.url_to_be(
        'https://online.spor.istanbul/confirmation'))

    # Assuming there is a confirmation message
    confirmation_message = driver.find_element(
        By.ID, 'confirmation-message').text
    if 'Your appointment has been successfully reserved' in confirmation_message:
        print("Appointment reserved successfully!")
    else:
        print("Failed to reserve appointment.")


"""
# Function to get available gym appointments
def get_appointments(driver):
    # Navigate to the gym schedule page
    driver.get('https://online.spor.istanbul/uyeseanssecim')

    # Wait for the page to load and display the schedule (you might need to adjust the waiting time)
    time.sleep(5)

    # Extract the page source and create a BeautifulSoup object for parsing
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Use BeautifulSoup to find and extract available appointment times
    # You'll need to inspect the page source and find the appropriate HTML elements for this.
    # It might be a table, a list, or some other element containing the appointment details.

    return available_appointments

# Function to reserve an appointment
def reserve_appointment(driver, appointment_time):
    # Implement the logic to select and reserve the desired appointment time.
    # This will depend on the website's specific interface for reserving appointments.
    # You might need to interact with drop-down menus, buttons, or forms.

    # After reserving the appointment, you might want to add some logic to confirm the reservation was successful.

"""

# Main function to run the bot


def main():
    username = '35476323148'
    password = 'Emirhan244'

    try:
        # Log in to the website
        driver = login(username, password)

        # Get available appointments
        available_appointments = get_appointments(driver)

        # If there are available appointments, reserve one
        if available_appointments:
            # You can modify this logic to select the appointment you prefer
            appointment_time = available_appointments[0]
            reserve_appointment(driver, appointment_time)

    finally:
        # Close the web driver after the script finishes
        if driver is not None:
            driver.quit()


# Run the main function
if __name__ == "__main__":
    main()
