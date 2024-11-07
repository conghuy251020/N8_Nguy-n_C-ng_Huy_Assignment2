import time

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from test_navigation import test_valid_login, test_page_checkout
from test_data_validation import test_checkout_product
from selenium.common.exceptions import UnexpectedAlertPresentException


@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()



# TC1: Kiểm tra thêm một sản phẩm vào giỏ hàng và thanh toán
def test_one_product(driver):
    test_checkout_product(driver)
    time.sleep(3)

# TC2: Kiểm tra thêm nhiều sản phẩm vào giỏ hàng và thanh toán
def test_many_product(driver):
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
        EC.element_to_be_clickable((By.XPATH,
                                    "//form[contains(@action, 'http://127.0.0.1:8000/menu/1')]//button[contains(@class, 'btn-success') and text()='Add to Cart']"))
    )
    add_to_cart_button.click()
    time.sleep(3)

    # Nhấn vào nút "Add to Cart" của sản phẩm "Klassy Pancake"
    add_to_cart_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH,
                                    "//form[contains(@action, 'http://127.0.0.1:8000/menu/2')]//button[contains(@class, 'btn-success') and text()='Add to Cart']"))
    )
    add_to_cart_button.click()
    time.sleep(3)

    # Nhấn vào nút "Add to Cart" của sản phẩm "Klassy Pancake"
    add_to_cart_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH,
                                    "//form[contains(@action, 'http://127.0.0.1:8000/menu/4')]//button[contains(@class, 'btn-success') and text()='Add to Cart']"))
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

    # Chờ đến khi nút Checkout có thể nhấn được và nhấn vào nó
    checkout_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn.btn-success"))
    )
    checkout_button.click()
    time.sleep(3)

    # Chờ radio button "cod" có thể nhấn được và nhấn vào nó
    cod_radio_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "cod"))
    )
    cod_radio_button.click()
    time.sleep(3)

    # Chờ nút "Place Order" có thể nhấn được và nhấn vào nó
    place_order_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//input[@type='submit' and @value='Place Order']"))
    )
    place_order_button.click()
    time.sleep(3)

    # Nhập địa chỉ vào ô "address"
    address_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "address"))
    )
    address_field.clear()
    address_field.send_keys("372 Dương Bá Trạc")
    time.sleep(3)

    # Nhập địa chỉ phụ vào ô "address2"
    address2_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "address2"))
    )
    address2_field.clear()
    address2_field.send_keys("272 An Dương Vương")
    time.sleep(3)

    # Chọn quốc gia "Bangladesh" từ dropdown "country"
    country_dropdown = Select(WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "country"))
    ))
    country_dropdown.select_by_visible_text("Bangladesh")
    time.sleep(3)

    # Chọn bang "Dhaka" từ dropdown "state"
    state_dropdown = Select(WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "state"))
    ))
    state_dropdown.select_by_visible_text("Dhaka")
    time.sleep(3)

    # Nhấn nút "Confirm order"
    confirm_order_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[@class='btn btn-primary' and contains(text(), 'Confirm order')]"))
    )
    confirm_order_button.click()
    time.sleep(3)

    # Truy cập trang chính
    driver.get("http://127.0.0.1:8000")

    # Nhấn vào liên kết "My Order"
    my_order_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[@href='/my-order']"))
    )
    my_order_link.click()
    time.sleep(3)

# TC3: Kiểm tra thanh toán sản phẩm với số lượng nhiều
def test_quantity_product(driver):
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

    # Tìm ô nhập số lượng và thay đổi giá trị thành 3
    quantity_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='number'][name='number']"))
    )
    quantity_input.clear()
    quantity_input.send_keys("3")
    time.sleep(3)

    # Nhấn vào nút "Add to Cart" của sản phẩm "Chocolate Cake"
    add_to_cart_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH,
                                    "//form[contains(@action, 'http://127.0.0.1:8000/menu/1')]//button[contains(@class, 'btn-success') and text()='Add to Cart']"))
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

    # Chờ đến khi nút Checkout có thể nhấn được và nhấn vào nó
    checkout_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn.btn-success"))
    )
    checkout_button.click()
    time.sleep(3)

    # Chờ radio button "cod" có thể nhấn được và nhấn vào nó
    cod_radio_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "cod"))
    )
    cod_radio_button.click()
    time.sleep(3)

    # Chờ nút "Place Order" có thể nhấn được và nhấn vào nó
    place_order_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//input[@type='submit' and @value='Place Order']"))
    )
    place_order_button.click()
    time.sleep(3)

    # Nhập địa chỉ vào ô "address"
    address_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "address"))
    )
    address_field.clear()
    address_field.send_keys("372 Dương Bá Trạc")
    time.sleep(3)

    # Nhập địa chỉ phụ vào ô "address2"
    address2_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "address2"))
    )
    address2_field.clear()
    address2_field.send_keys("272 An Dương Vương")
    time.sleep(3)

    # Chọn quốc gia "Bangladesh" từ dropdown "country"
    country_dropdown = Select(WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "country"))
    ))
    country_dropdown.select_by_visible_text("Bangladesh")
    time.sleep(3)

    # Chọn bang "Dhaka" từ dropdown "state"
    state_dropdown = Select(WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "state"))
    ))
    state_dropdown.select_by_visible_text("Dhaka")
    time.sleep(3)

    # Nhấn nút "Confirm order"
    confirm_order_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[@class='btn btn-primary' and contains(text(), 'Confirm order')]"))
    )
    confirm_order_button.click()
    time.sleep(3)

    # Truy cập trang chính
    driver.get("http://127.0.0.1:8000")

    # Nhấn vào liên kết "My Order"
    my_order_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[@href='/my-order']"))
    )
    my_order_link.click()
    time.sleep(3)

# TC4: Kiểm tra thanh toán sản phẩm với số lượng âm
def test_quantity_negative_product(driver):
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

    # Tìm ô nhập số lượng và thay đổi giá trị thành 3
    quantity_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='number'][name='number']"))
    )
    quantity_input.clear()
    quantity_input.send_keys("-3")
    time.sleep(3)

    # Nhấn vào nút "Add to Cart" của sản phẩm "Chocolate Cake"
    add_to_cart_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH,
                                    "//form[contains(@action, 'http://127.0.0.1:8000/menu/1')]//button[contains(@class, 'btn-success') and text()='Add to Cart']"))
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

    # Chờ đến khi nút Checkout có thể nhấn được và nhấn vào nó
    checkout_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn.btn-success"))
    )
    checkout_button.click()
    time.sleep(3)

    # Chờ radio button "cod" có thể nhấn được và nhấn vào nó
    cod_radio_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "cod"))
    )
    cod_radio_button.click()
    time.sleep(3)

    # Chờ nút "Place Order" có thể nhấn được và nhấn vào nó
    place_order_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//input[@type='submit' and @value='Place Order']"))
    )
    place_order_button.click()
    time.sleep(3)

    # Nhập địa chỉ vào ô "address"
    address_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "address"))
    )
    address_field.clear()
    address_field.send_keys("372 Dương Bá Trạc")
    time.sleep(3)

    # Nhập địa chỉ phụ vào ô "address2"
    address2_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "address2"))
    )
    address2_field.clear()
    address2_field.send_keys("272 An Dương Vương")
    time.sleep(3)

    # Chọn quốc gia "Bangladesh" từ dropdown "country"
    country_dropdown = Select(WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "country"))
    ))
    country_dropdown.select_by_visible_text("Bangladesh")
    time.sleep(3)

    # Chọn bang "Dhaka" từ dropdown "state"
    state_dropdown = Select(WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "state"))
    ))
    state_dropdown.select_by_visible_text("Dhaka")
    time.sleep(3)

    # Nhấn nút "Confirm order"
    confirm_order_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[@class='btn btn-primary' and contains(text(), 'Confirm order')]"))
    )
    confirm_order_button.click()
    time.sleep(3)

    # Truy cập trang chính
    driver.get("http://127.0.0.1:8000")

    # Nhấn vào liên kết "My Order"
    my_order_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[@href='/my-order']"))
    )
    my_order_link.click()
    time.sleep(3)

# TC5: Kiểm tra cập nhật số lượng sản phẩm và thanh toán
def test_update_product(driver):
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
        EC.element_to_be_clickable((By.XPATH,
                                    "//form[contains(@action, 'http://127.0.0.1:8000/menu/1')]//button[contains(@class, 'btn-success') and text()='Add to Cart']"))
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

    # Chờ đến khi liên kết Continue Shopping có thể nhấn được và nhấn vào nó
    continue_shopping_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "a.btn.btn-warning"))
    )
    continue_shopping_button.click()
    time.sleep(3)

    # Nhấn vào nút "Add to Cart" của sản phẩm "Chocolate Cake"
    add_to_cart_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH,
                                    "//form[contains(@action, 'http://127.0.0.1:8000/menu/1')]//button[contains(@class, 'btn-success') and text()='Add to Cart']"))
    )
    add_to_cart_button.click()
    time.sleep(3)

    # Nhấn vào biểu tượng giỏ hàng
    shopping_cart_icon = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "i.fa-shopping-cart"))
    )
    shopping_cart_icon.click()
    time.sleep(3)

    # Chờ đến khi nút Checkout có thể nhấn được và nhấn vào nó
    checkout_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn.btn-success"))
    )
    checkout_button.click()
    time.sleep(3)

    # Chờ radio button "cod" có thể nhấn được và nhấn vào nó
    cod_radio_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "cod"))
    )
    cod_radio_button.click()
    time.sleep(3)

    # Chờ nút "Place Order" có thể nhấn được và nhấn vào nó
    place_order_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//input[@type='submit' and @value='Place Order']"))
    )
    place_order_button.click()
    time.sleep(3)

    # Nhập địa chỉ vào ô "address"
    address_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "address"))
    )
    address_field.clear()
    address_field.send_keys("372 Dương Bá Trạc")
    time.sleep(3)

    # Nhập địa chỉ phụ vào ô "address2"
    address2_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "address2"))
    )
    address2_field.clear()
    address2_field.send_keys("272 An Dương Vương")
    time.sleep(3)

    # Chọn quốc gia "Bangladesh" từ dropdown "country"
    country_dropdown = Select(WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "country"))
    ))
    country_dropdown.select_by_visible_text("Bangladesh")
    time.sleep(3)

    # Chọn bang "Dhaka" từ dropdown "state"
    state_dropdown = Select(WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "state"))
    ))
    state_dropdown.select_by_visible_text("Dhaka")
    time.sleep(3)

    # Nhấn nút "Confirm order"
    confirm_order_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[@class='btn btn-primary' and contains(text(), 'Confirm order')]"))
    )
    confirm_order_button.click()
    time.sleep(3)

    # Truy cập trang chính
    driver.get("http://127.0.0.1:8000")

    # Nhấn vào liên kết "My Order"
    my_order_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[@href='/my-order']"))
    )
    my_order_link.click()
    time.sleep(3)

# TC6: Kiểm tra xóa sản phẩm ra khỏi giỏ hàng
def test_remove_cart(driver):
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
        EC.element_to_be_clickable((By.XPATH,
                                    "//form[contains(@action, 'http://127.0.0.1:8000/menu/1')]//button[contains(@class, 'btn-success') and text()='Add to Cart']"))
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

    # Nhấn vào biểu tượng xóa sản phẩm trong giỏ hàng
    delete_icon = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "i.fa-trash"))
    )
    delete_icon.click()
    time.sleep(3)

    # Xử lý alert nếu có
    try:
        alert = WebDriverWait(driver, 10).until(EC.alert_is_present())
        alert.accept()  # Nhấn vào nút "Ok" trên alert
        time.sleep(5)
    except UnexpectedAlertPresentException:
        print("Alert không tồn tại hoặc không thể xử lý.")

    # Kiểm tra lại chuyển hướng sang trang giỏ hàng
    WebDriverWait(driver, 10).until(EC.url_to_be("http://127.0.0.1:8000/cart"))
    assert driver.current_url == "http://127.0.0.1:8000/cart", "Not redirected to the cart page after deletion."

    # Kiểm tra nếu sản phẩm đã được xóa khỏi giỏ hàng
    WebDriverWait(driver, 10).until(
        EC.invisibility_of_element_located((By.XPATH, "//tr[contains(., 'Chocolate Cake')]"))
    )
    assert "Chocolate Cake" not in driver.page_source, "Product was not removed from cart."

# TC7: Kiểm tra thêm sản phẩm đã hết hàng vào giỏ hàng
def test_out_of_stock(driver):
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

    # Nhấn vào nút "Out of Stock" của sản phẩm "BlueBerry Cake"
    out_of_stock_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//p[contains(@class, 'btn-danger') and text()='Out of Stock']"))
    )
    out_of_stock_element.click()
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