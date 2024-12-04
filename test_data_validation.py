import time

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from test_navigation import test_valid_login, test_page_checkout


@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()

# TC1: Xác thực dữ liệu sau khi thêm sản phẩm vào giỏ hàng
def test_data_product(driver):
    test_valid_login(driver)
    time.sleep(1)

    # Nhấn vào nút "Browse All"
    browse_all_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='submit'][value='Browse All']"))
    )
    browse_all_button.click()

    # Chờ chuyển hướng đến trang menu
    WebDriverWait(driver, 10).until(EC.url_to_be("http://127.0.0.1:8000/menu"))

    # Nhấn vào nút "Add to Cart" của sản phẩm "Chocolate Cake"
    add_to_cart_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//form[contains(@action, 'http://127.0.0.1:8000/menu/2')]//button[contains(@class, 'btn-success') and text()='Add to Cart']"))
    )
    add_to_cart_button.click()

    # Nhấn vào biểu tượng giỏ hàng
    shopping_cart_icon = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "i.fa-shopping-cart"))
    )
    shopping_cart_icon.click()

    # Chờ chuyển hướng đến trang giỏ hàng
    WebDriverWait(driver, 10).until(EC.url_to_be("http://127.0.0.1:8000/cart"))
    assert driver.current_url == "http://127.0.0.1:8000/cart", "Login failed: Not redirected to expected page."

# TC2: Xác thực dữ liệu sau khi thanh toán đơn hàng
def test_checkout_product(driver):
    test_page_checkout(driver)
    time.sleep(1)

    # Chờ radio button "cod" có thể nhấn được và nhấn vào nó
    cod_radio_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "cod"))
    )
    cod_radio_button.click()

    # Chờ nút "Place Order" có thể nhấn được và nhấn vào nó
    place_order_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//input[@type='submit' and @value='Place Order']"))
    )
    place_order_button.click()

    # Nhập địa chỉ vào ô "address"
    address_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "address"))
    )
    address_field.clear()
    address_field.send_keys("372 Dương Bá Trạc")
    time.sleep(1)

    # Nhập địa chỉ phụ vào ô "address2"
    address2_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "address2"))
    )
    address2_field.clear()
    address2_field.send_keys("272 An Dương Vương")
    time.sleep(1)

    # Chọn quốc gia "Bangladesh" từ dropdown "country"
    country_dropdown = Select(WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "country"))
    ))
    country_dropdown.select_by_visible_text("Bangladesh")
    time.sleep(1)

    # Chọn bang "Dhaka" từ dropdown "state"
    state_dropdown = Select(WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "state"))
    ))
    state_dropdown.select_by_visible_text("Dhaka")
    time.sleep(1)

    # Nhấn nút "Confirm order"
    confirm_order_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[@class='btn btn-primary' and contains(text(), 'Confirm order')]"))
    )
    confirm_order_button.click()
    time.sleep(1)

    # Truy cập trang chính
    driver.get("http://127.0.0.1:8000")

    # Nhấn vào liên kết "My Order"
    my_order_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[@href='/my-order']"))
    )
    my_order_link.click()

# TC3: Xác thực dữ liệu theo dõi đơn hàng
def test_trace_order(driver):
    test_valid_login(driver)
    time.sleep(1)

    # Nhấn vào nút "Browse All"
    browse_all_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='submit'][value='Browse All']"))
    )
    browse_all_button.click()

    # Chờ chuyển hướng đến trang menu
    WebDriverWait(driver, 10).until(EC.url_to_be("http://127.0.0.1:8000/menu"))

    # Nhấn vào nút "Add to Cart" của sản phẩm "Chocolate Cake"
    add_to_cart_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH,
                                    "//form[contains(@action, 'http://127.0.0.1:8000/menu/1')]//button[contains(@class, 'btn-success') and text()='Add to Cart']"))
    )
    add_to_cart_button.click()
    time.sleep(1)

    # Nhấn vào biểu tượng giỏ hàng
    shopping_cart_icon = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "i.fa-shopping-cart"))
    )
    shopping_cart_icon.click()
    time.sleep(1)

    # Chờ chuyển hướng đến trang giỏ hàng
    WebDriverWait(driver, 10).until(EC.url_to_be("http://127.0.0.1:8000/cart"))
    assert driver.current_url == "http://127.0.0.1:8000/cart", "Login failed: Not redirected to expected page."

    # Chờ đến khi nút Checkout có thể nhấn được và nhấn vào nó
    checkout_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn.btn-success"))
    )
    checkout_button.click()
    time.sleep(1)

    # Chờ radio button "cod" có thể nhấn được và nhấn vào nó
    cod_radio_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "cod"))
    )
    cod_radio_button.click()
    time.sleep(1)

    # Chờ nút "Place Order" có thể nhấn được và nhấn vào nó
    place_order_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//input[@type='submit' and @value='Place Order']"))
    )
    place_order_button.click()
    time.sleep(1)

    # Nhập địa chỉ vào ô "address"
    address_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "address"))
    )
    address_field.clear()
    address_field.send_keys("372 Dương Bá Trạc")
    time.sleep(1)

    # Nhập địa chỉ phụ vào ô "address2"
    address2_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "address2"))
    )
    address2_field.clear()
    address2_field.send_keys("272 An Dương Vương")
    time.sleep(1)

    # Chọn quốc gia "Bangladesh" từ dropdown "country"
    country_dropdown = Select(WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "country"))
    ))
    country_dropdown.select_by_visible_text("Bangladesh")
    time.sleep(1)

    # Chọn bang "Dhaka" từ dropdown "state"
    state_dropdown = Select(WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "state"))
    ))
    state_dropdown.select_by_visible_text("Dhaka")
    time.sleep(1)

    # Nhấn nút "Confirm order"
    confirm_order_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[@class='btn btn-primary' and contains(text(), 'Confirm order')]"))
    )
    confirm_order_button.click()
    time.sleep(1)

    # Lấy giá trị của Invoice no từ thẻ <h3>
    invoice_no = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//h3[contains(text(), 'Invoice no -')]"))
    ).text

    # Tách lấy phần giá trị sau dấu gạch ngang
    invoice_no = invoice_no.split(" - ")[1]

    # Kiểm tra giá trị của Invoice no (hoặc lưu lại cho các bước tiếp theo)
    print("Invoice no:", invoice_no)

    # Trở lại trang chủ
    driver.get("http://127.0.0.1:8000")
    time.sleep(1)

    # Nhấn vào nút "Trace Order"
    trace_order_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Trace Order"))
    )
    trace_order_button.click()

    # Nhập Invoice no vào ô nhập
    invoice_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "invoice"))
    )
    invoice_input.clear()
    invoice_input.send_keys(invoice_no)
    time.sleep(1)

    # Nhập số điện thoại vào ô nhập
    phone_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "phone"))
    )
    phone_input.clear()
    phone_input.send_keys("0367195476")  # Nhập số điện thoại theo yêu cầu
    time.sleep(1)

    # Nhấn nút "Submit"
    submit_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "form-submit"))
    )
    submit_button.click()
    time.sleep(1)



