import time

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()


# User Authentication
# TC1: Kiểm tra chức năng Đăng nhập thành công
def test_valid_login(driver):
    # Truy cập vào trang web đăng nhập
    driver.get("http://127.0.0.1:8000")
    time.sleep(2)  # Thêm thời gian chờ sau khi tải trang

    # Nhấn vào nút "Log in" để chuyển hướng đến trang đăng nhập
    login_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='http://127.0.0.1:8000/login']"))
    )
    login_link.click()
    time.sleep(2)  # Thêm thời gian chờ sau khi nhấn vào liên kết

    # Đợi trang đăng nhập tải xong
    WebDriverWait(driver, 10).until(EC.url_to_be("http://127.0.0.1:8000/login"))
    time.sleep(2)  # Thêm thời gian chờ để trang ổn định

    # Nhập email
    email_input = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "email"))
    )
    email_input.send_keys("conghuy251020@gmail.com")
    time.sleep(1)  # Thêm thời gian chờ sau khi nhập email

    # Nhập password
    password_input = driver.find_element(By.ID, "password")
    password_input.send_keys("123456789")
    time.sleep(1)  # Thêm thời gian chờ sau khi nhập password

    # Tìm và nhấn nút "Log in" bằng CSS Selector
    login_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
    )
    login_button.click()
    time.sleep(3)  # Thêm thời gian chờ sau khi nhấn nút "Log in"

    # Chờ chuyển hướng đến trang `http://127.0.0.1:8000/redirects`
    WebDriverWait(driver, 10).until(EC.url_to_be("http://127.0.0.1:8000/redirects"))
    assert driver.current_url == "http://127.0.0.1:8000/redirects", "Login failed: Not redirected to expected page."

# TC2: Kiểm tra chức năng Đăng nhập khi mật khẩu không đúng
def test_password_login(driver):
    # Truy cập vào trang web đăng nhập
    driver.get("http://127.0.0.1:8000")
    time.sleep(2)  # Thêm thời gian chờ sau khi tải trang

    # Nhấn vào nút "Log in" để chuyển hướng đến trang đăng nhập
    login_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='http://127.0.0.1:8000/login']"))
    )
    login_link.click()
    time.sleep(2)  # Thêm thời gian chờ sau khi nhấn vào liên kết

    # Đợi trang đăng nhập tải xong
    WebDriverWait(driver, 10).until(EC.url_to_be("http://127.0.0.1:8000/login"))
    time.sleep(2)  # Thêm thời gian chờ để trang ổn định

    # Nhập email không hợp lệ
    email_input = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "email"))
    )
    email_input.send_keys("conghuy251020@gmail.com")

    # Nhập password không đúng
    password_input = driver.find_element(By.ID, "password")
    password_input.send_keys("wrongpassword")

    # Tìm và nhấn nút "Log in" bằng CSS Selector
    login_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
    )
    login_button.click()
    time.sleep(5)  # Thêm thời gian chờ để trang ổn định

    # Kiểm tra xem vẫn ở trang đăng nhập
    assert driver.current_url == "http://127.0.0.1:8000/login", "User was redirected away from the login page despite invalid credentials."

# TC3: Kiểm tra chức năng Đăng nhập khi tài khoản chứa kí tự đặc biệt
def test_account_login(driver):
    # Truy cập vào trang web đăng nhập
    driver.get("http://127.0.0.1:8000")
    time.sleep(2)  # Thêm thời gian chờ sau khi tải trang

    # Nhấn vào nút "Log in" để chuyển hướng đến trang đăng nhập
    login_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='http://127.0.0.1:8000/login']"))
    )
    login_link.click()
    time.sleep(2)  # Thêm thời gian chờ sau khi nhấn vào liên kết

    # Đợi trang đăng nhập tải xong
    WebDriverWait(driver, 10).until(EC.url_to_be("http://127.0.0.1:8000/login"))
    time.sleep(2)  # Thêm thời gian chờ để trang ổn định

    # Nhập email không hợp lệ
    email_input = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "email"))
    )
    email_input.send_keys("conghuy251020@@gmail.com")

    # Nhập password không đúng
    password_input = driver.find_element(By.ID, "password")
    password_input.send_keys("123456789")

    # Tìm và nhấn nút "Log in" bằng CSS Selector
    login_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
    )
    login_button.click()
    time.sleep(5)  # Thêm thời gian chờ để trang ổn định

    # Kiểm tra xem vẫn ở trang đăng nhập
    assert driver.current_url == "http://127.0.0.1:8000/login", "User was redirected away from the login page despite invalid credentials."

# TC4: Kiểm tra chức năng Đăng xuất
def test_valid_logout(driver):
    # Gọi hàm đăng nhập trước để đảm bảo người dùng đã đăng nhập
    test_valid_login(driver)
    time.sleep(3)  # Thời gian chờ để đảm bảo trang đã tải hoàn toàn

    # Tìm và nhấn vào nút "Công Huy" sau khi đăng nhập thành công
    user_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Công Huy')]"))
    )
    user_button.click()
    time.sleep(3)  # Thời gian chờ sau khi nhấn nút "Công Huy"

    # Tìm và nhấn vào liên kết "Logout"
    logout_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[@href='http://127.0.0.1:8000/logout']"))
    )
    logout_link.click()
    time.sleep(5)  # Thời gian chờ sau khi nhấn vào "Logout"

    # Kiểm tra sự hiện diện của ô nhập `email` để xác nhận đăng xuất thành công
    email_input = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "email"))
    )

    # Xác nhận người dùng đã đăng xuất thành công
    assert email_input.is_displayed(), "Logout failed: Login page did not load as expected."

