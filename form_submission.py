import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from login_logout import test_valid_login

@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()

# TC1: Điền và gửi biểu mẫu đăng kí với thông tin hợp lệ
def test_valid_register(driver):
    # Truy cập vào trang web
    driver.get("http://127.0.0.1:8000/")
    time.sleep(2)  # Chờ 2 giây trước khi tiếp tục

    # Nhấn vào nút Register
    register_link = driver.find_element(By.LINK_TEXT, "Register")
    register_link.click()
    time.sleep(2)  # Chờ 2 giây trước khi tiếp tục

    # Nhập thông tin vào các ô
    wait = WebDriverWait(driver, 10)

    # Nhập tên
    name_input = wait.until(EC.visibility_of_element_located((By.ID, "name")))
    name_input.send_keys("Huy Nguyễn")
    time.sleep(1)  # Chờ 1 giây sau khi nhập tên

    # Nhập email
    email_input = wait.until(EC.visibility_of_element_located((By.ID, "email")))
    email_input.send_keys("kiet3kt2003@gmail.com")
    time.sleep(1)  # Chờ 1 giây sau khi nhập email

    # Nhập số điện thoại
    phone_input = wait.until(EC.visibility_of_element_located((By.NAME, "phone")))
    phone_input.send_keys("0918273437")
    time.sleep(1)  # Chờ 1 giây sau khi nhập số điện thoại

    # Nhập mật khẩu
    password_input = wait.until(EC.visibility_of_element_located((By.ID, "password")))
    password_input.send_keys("123456789")
    time.sleep(1)  # Chờ 1 giây sau khi nhập mật khẩu

    # Nhập xác nhận mật khẩu
    password_confirmation_input = wait.until(EC.visibility_of_element_located((By.NAME, "password_confirmation")))
    password_confirmation_input.send_keys("123456789")
    time.sleep(1)  # Chờ 1 giây sau khi nhập xác nhận mật khẩu

    # Nhấn nút Register
    register_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit'].inline-flex")))
    register_button.click()
    time.sleep(2)  # Chờ 2 giây trước khi kiểm tra URL

    # Kiểm tra xem có chuyển hướng đến trang login không
    WebDriverWait(driver, 10).until(EC.url_to_be("http://127.0.0.1:8000/login"))
    assert driver.current_url == "http://127.0.0.1:8000/login"

    # Nhập thông tin đăng nhập
    email_login_input = wait.until(EC.visibility_of_element_located((By.ID, "email")))
    email_login_input.send_keys("kiet3kt2003@gmail.com")

    password_login_input = wait.until(EC.visibility_of_element_located((By.ID, "password")))
    password_login_input.send_keys("123456789")

    # Nhấn nút Log in
    login_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
    login_button.click()
    time.sleep(2)  # Chờ 2 giây trước khi kiểm tra URL

    # Kiểm tra xem có chuyển hướng đến trang redirects không
    WebDriverWait(driver, 10).until(EC.url_to_be("http://127.0.0.1:8000/redirects"))
    assert driver.current_url == "http://127.0.0.1:8000/redirects"

# TC2: Kiểm tra trường hợp thông tin đã tồn tại
def test_email_number_register(driver):
    # Truy cập vào trang web
    driver.get("http://127.0.0.1:8000/")
    time.sleep(2)  # Chờ 2 giây trước khi tiếp tục

    # Nhấn vào nút Register
    register_link = driver.find_element(By.LINK_TEXT, "Register")
    register_link.click()
    time.sleep(2)  # Chờ 2 giây trước khi tiếp tục

    # Nhập thông tin vào các ô
    wait = WebDriverWait(driver, 10)

    # Nhập tên
    name_input = wait.until(EC.visibility_of_element_located((By.ID, "name")))
    name_input.send_keys("Huy Nguyễn")
    time.sleep(1)  # Chờ 1 giây sau khi nhập tên

    # Nhập email
    email_input = wait.until(EC.visibility_of_element_located((By.ID, "email")))
    email_input.send_keys("kiet3bx2003@gmail.com")
    time.sleep(1)  # Chờ 1 giây sau khi nhập email

    # Nhập số điện thoại
    phone_input = wait.until(EC.visibility_of_element_located((By.NAME, "phone")))
    phone_input.send_keys("0918273421")
    time.sleep(1)  # Chờ 1 giây sau khi nhập số điện thoại

    # Nhập mật khẩu
    password_input = wait.until(EC.visibility_of_element_located((By.ID, "password")))
    password_input.send_keys("123456789")
    time.sleep(1)  # Chờ 1 giây sau khi nhập mật khẩu

    # Nhập xác nhận mật khẩu
    password_confirmation_input = wait.until(EC.visibility_of_element_located((By.NAME, "password_confirmation")))
    password_confirmation_input.send_keys("123456789")
    time.sleep(1)  # Chờ 1 giây sau khi nhập xác nhận mật khẩu

    # Nhấn nút Register
    register_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit'].inline-flex")))
    register_button.click()
    time.sleep(2)  # Chờ 2 giây trước khi kiểm tra URL

# TC3: Kiểm tra trường hợp thiếu thông tin bắt buộc
def test_empty_register(driver):
    # Truy cập vào trang web
    driver.get("http://127.0.0.1:8000/")
    time.sleep(2)  # Chờ 2 giây trước khi tiếp tục

    # Nhấn vào nút Register
    register_link = driver.find_element(By.LINK_TEXT, "Register")
    register_link.click()
    time.sleep(2)  # Chờ 2 giây trước khi tiếp tục

    # Nhập thông tin vào các ô
    wait = WebDriverWait(driver, 10)

    # Nhập tên
    name_input = wait.until(EC.visibility_of_element_located((By.ID, "name")))
    name_input.send_keys("Huy Nguyễn")
    time.sleep(1)  # Chờ 1 giây sau khi nhập tên

    # Nhập email
    email_input = wait.until(EC.visibility_of_element_located((By.ID, "email")))
    email_input.send_keys("")
    time.sleep(1)  # Chờ 1 giây sau khi nhập email

    # Nhập số điện thoại
    phone_input = wait.until(EC.visibility_of_element_located((By.NAME, "phone")))
    phone_input.send_keys("0918273411")
    time.sleep(1)  # Chờ 1 giây sau khi nhập số điện thoại

    # Nhập mật khẩu
    password_input = wait.until(EC.visibility_of_element_located((By.ID, "password")))
    password_input.send_keys("123456789")
    time.sleep(1)  # Chờ 1 giây sau khi nhập mật khẩu

    # Nhập xác nhận mật khẩu
    password_confirmation_input = wait.until(EC.visibility_of_element_located((By.NAME, "password_confirmation")))
    password_confirmation_input.send_keys("123456789")
    time.sleep(1)  # Chờ 1 giây sau khi nhập xác nhận mật khẩu

    # Nhấn nút Register
    register_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit'].inline-flex")))
    register_button.click()
    time.sleep(5)  # Chờ 2 giây trước khi kiểm tra URL

# TC4: Điền và gửi biểu mẫu liên hệ với thông tin hợp lệ
def test_contact_us(driver):
    # Gọi hàm đăng nhập
    test_valid_login(driver)
    time.sleep(2)

    # Chờ và nhấn vào liên kết 'Contact Us'
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[@href='/#reservation']"))
    ).click()
    time.sleep(2)

    # Nhập thông tin vào các trường
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "name"))
    ).send_keys("Nguyễn Việt Hoàng")
    time.sleep(2)

    driver.find_element(By.ID, "phone").send_keys("0123456259")
    time.sleep(2)

    driver.find_element(By.ID, "date").send_keys("01/12/2023")
    time.sleep(2)

    driver.find_element(By.ID, "email").send_keys("nguyenviethoang@example.com")
    time.sleep(2)

    # Chọn số lượng khách từ dropdown
    Select(driver.find_element(By.ID, "number-guests")).select_by_value("5")
    time.sleep(2)

    # Chọn thời gian từ dropdown
    Select(driver.find_element(By.ID, "time")).select_by_value("Dinner")
    time.sleep(2)

    # Nhập tin nhắn vào ô Message
    driver.find_element(By.ID, "message").send_keys("Đặt bàn cho 5 người vào buổi tối.")
    time.sleep(2)

    # Nhấn nút "Make A Reservation"
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "form-submit"))
    ).click()
    time.sleep(2)