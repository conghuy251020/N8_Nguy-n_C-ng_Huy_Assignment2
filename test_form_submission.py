import time
import pytest
from httpcore import TimeoutException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from test_login_logout import test_valid_login

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
    email_input.send_keys("kiet3px2003@gmail.com")
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
    email_login_input.send_keys("kiet3px2003@gmail.com")

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

    # Kiểm tra thông báo lỗi nếu email đã đăng ký
    try:
        # Kiểm tra sự xuất hiện của thông báo lỗi
        alert_message = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.alert")))
        alert_text = alert_message.text
        if "Email already registered" in alert_text:
            print("Error: Email already registered!")
        else:
            print("Registration successful!")
    except TimeoutException:
        print("No error message displayed.")

# TC3: Kiểm tra trường hợp thiếu thông tin bắt buộc
def test_empty_register(driver):
    # Truy cập vào trang web
    driver.get("http://127.0.0.1:8000/")

    # Nhấn vào nút Register
    wait = WebDriverWait(driver, 10)
    register_link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Register")))
    register_link.click()

    # Nhập thông tin vào các ô
    # Nhập tên
    name_input = wait.until(EC.visibility_of_element_located((By.ID, "name")))
    name_input.send_keys("Huy Nguyễn")

    # Để trống email
    email_input = wait.until(EC.visibility_of_element_located((By.ID, "email")))
    email_input.clear()  # Đảm bảo trường này trống

    # Nhập số điện thoại
    phone_input = wait.until(EC.visibility_of_element_located((By.NAME, "phone")))
    phone_input.send_keys("0918273411")

    # Nhập mật khẩu
    password_input = wait.until(EC.visibility_of_element_located((By.ID, "password")))
    password_input.send_keys("123456789")

    # Nhập xác nhận mật khẩu
    password_confirmation_input = wait.until(EC.visibility_of_element_located((By.NAME, "password_confirmation")))
    password_confirmation_input.send_keys("123456789")

    # Nhấn nút Register
    register_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit'].inline-flex")))
    register_button.click()

    # Kiểm tra thông báo lỗi của trường email
    email_error_message = None
    try:
        email_error_message = email_input.get_attribute("validationMessage")
        print("Email error message:", email_error_message)
    except Exception as e:
        print("Không thể kiểm tra thông báo lỗi cho email:", e)

    # Xác minh rằng thông báo lỗi tồn tại
    assert email_error_message == "Please fill out this field.", \
        f"Lỗi không chính xác cho email: {email_error_message}"

    # Kiểm tra URL không thay đổi (người dùng không đăng ký thành công)
    current_url = driver.current_url
    assert current_url == "http://127.0.0.1:8000/register", \
        f"URL thay đổi bất thường: {current_url}"

    print("Kiểm tra thành công: Trường email bị để trống.")

# TC4: Điền và gửi biểu mẫu liên hệ với thông tin hợp lệ
def test_contact_us(driver):
    test_valid_login(driver)

    # Chờ và nhấn vào liên kết 'Contact Us'
    contact_us_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[@href='/#reservation']"))
    )
    contact_us_link.click()

    # Nhập thông tin vào các trường
    # Nhập tên
    name_input = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "name"))
    )
    name_input.send_keys("Nguyễn Huy Hoàng")

    # Nhập số điện thoại
    phone_input = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "phone"))
    )
    phone_input.send_keys("0123456245")

    # Nhập ngày đặt bàn
    date_input = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "date"))
    )
    date_input.send_keys("01/12/2023")

    # Nhập email
    email_input = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "email"))
    )
    email_input.send_keys("nguyenhuyhoang@example.com")

    # Chọn số lượng khách từ dropdown
    guests_dropdown = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "number-guests"))
    )
    Select(guests_dropdown).select_by_value("5")

    # Chọn thời gian từ dropdown
    time_dropdown = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "time"))
    )
    Select(time_dropdown).select_by_value("Dinner")

    # Nhập tin nhắn vào ô Message
    message_input = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "message"))
    )
    message_input.send_keys("Đặt bàn cho 5 người vào buổi tối.")

    # Nhấn nút "Make A Reservation"
    submit_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "form-submit"))
    )
    submit_button.click()

    # Kiểm tra sau khi nhấn nút "Make A Reservation", trang có chuyển hướng và URL có chứa "reserve"
    WebDriverWait(driver, 10).until(
        EC.url_contains("reserve")  # Kiểm tra URL chứa từ "reserve"
    )

    # Lấy URL hiện tại và kiểm tra
    current_url = driver.current_url
    assert "reserve" in current_url, f"Không chuyển hướng đến trang đặt bàn. URL hiện tại: {current_url}"
    time.sleep(1)

    print("Đặt bàn thành công!")