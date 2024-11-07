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



# TC1: Điều hướng từ trang chính đến trang đăng nhập và ngược lại
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

# TC2: Điều hướng từ trang thông tin sản phẩm đến giỏ hàng
def test_page_product(driver):
    test_valid_login(driver)

    # Chờ 3 giây
    time.sleep(3)

    # Nhấn vào nút "Browse All"
    browse_all_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='submit'][value='Browse All']"))
    )
    browse_all_button.click()
    time.sleep(3)

    # Chờ chuyển hướng đến trang menu
    WebDriverWait(driver, 10).until(EC.url_to_be("http://127.0.0.1:8000/menu"))

    # Nhấn vào nút "Add to Cart" của sản phẩm "Chocolate Cake"
    add_to_cart_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//form[contains(@action, 'http://127.0.0.1:8000/menu/1')]//button[contains(@class, 'btn-success') and text()='Add to Cart']"))
    )
    add_to_cart_button.click()
    time.sleep(3)

    # Nhấn vào biểu tượng giỏ hàng
    shopping_cart_icon = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "i.fa-shopping-cart"))
    )
    shopping_cart_icon.click()
    time.sleep(3)

    # Chờ chuyển hướng đến trang giỏ hàng
    WebDriverWait(driver, 10).until(EC.url_to_be("http://127.0.0.1:8000/cart"))
    assert driver.current_url == "http://127.0.0.1:8000/cart", "Login failed: Not redirected to expected page."

# TC3: Điều hướng từ trang giỏ hàng đến trang thanh toán
def test_page_checkout(driver):
    test_page_product(driver)
    time.sleep(3)

    # Chờ đến khi nút Checkout có thể nhấn được và nhấn vào nó
    checkout_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn.btn-success"))
    )
    checkout_button.click()
    time.sleep(3)


