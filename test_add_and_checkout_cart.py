import time

import pytest
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from test_navigation import test_valid_login, test_page_checkout
from test_data_validation import test_checkout_product
from selenium.common.exceptions import UnexpectedAlertPresentException, NoSuchElementException


@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()

def test_check_out(driver):
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

# TC1: Kiểm tra thêm một sản phẩm vào giỏ hàng và thanh toán
def test_one_product(driver):
    test_valid_login(driver)
    time.sleep(1)

    # Nhấn vào nút "Browse All"
    browse_all_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='submit'][value='Browse All']"))
    )
    browse_all_button.click()

    # Chờ chuyển hướng đến trang menu
    WebDriverWait(driver, 10).until(EC.url_to_be("http://127.0.0.1:8000/menu"))

    # Tìm ô nhập số lượng và thay đổi giá trị thành 1 cho sản phẩm Chocolate Cake
    quantity_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, "//h2[contains(text(), 'Chocolate Cake')]//following::input[@type='number'][@name='number']"))
    )
    quantity_input.clear()
    quantity_input.send_keys("1")  # Thay đổi giá trị số lượng thành 1
    quantity = int(quantity_input.get_attribute("value"))  # Lấy giá trị số lượng từ ô nhập liệu

    total_price = 0

    # Nhấn vào nút "Add to Cart" của sản phẩm "Chocolate Cake"
    add_to_cart_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH,
                                    "//form[contains(@action, 'http://127.0.0.1:8000/menu/1')]//button[contains(@class, 'btn-success') and text()='Add to Cart']"))
    )
    add_to_cart_button.click()

    # Lấy giá sản phẩm
    product_price_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, "//td[h2[contains(text(), 'Chocolate Cake')]]//h4[contains(text(), '৳')]"))
    )
    product_price = float(product_price_element.text.replace('৳', '').strip())

    # Nhân giá sản phẩm với số lượng để tính tổng tiền của sản phẩm
    product_total = product_price * quantity
    total_price += product_total

    # In ra tổng tiền của sản phẩm
    print(f"Tổng tiền của {quantity} sản phẩm: {product_total} ৳")

    # Nhấn vào biểu tượng giỏ hàng
    shopping_cart_icon = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "i.fa-shopping-cart"))
    )
    shopping_cart_icon.click()

    # Chờ chuyển hướng đến trang giỏ hàng
    WebDriverWait(driver, 10).until(EC.url_to_be("http://127.0.0.1:8000/cart"))

    cart_row = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//tr[td[text()='Chocolate Cake']]"))
    )
    cart_td_elements = cart_row.find_elements(By.TAG_NAME, "td")

    # Lấy thông tin từ giỏ hàng
    cart_name = cart_td_elements[0].text.strip()
    cart_price = float(cart_td_elements[1].text.strip()[1:])  # Bỏ ký tự '৳'
    cart_quantity = int(cart_td_elements[2].text.strip())
    cart_sub_total = float(cart_td_elements[3].text.strip()[1:])  # Bỏ ký tự '৳'

    # Thông tin sản phẩm từ danh sách
    p_name = "Chocolate Cake"
    price = product_price
    quan = quantity

    # Kiểm tra từng trường
    check_name = p_name == cart_name
    check_price = price == cart_price
    check_quantity = quan == cart_quantity
    check_sub_total = (price * quan) == cart_sub_total

    print(f"Check name: {p_name} - {check_name}")
    print(f"Check price: {price} - {check_price}")
    print(f"Check quantity: {quan} - {check_quantity}")
    print(f"Check sub_total: {price * quan} - {check_sub_total}")

    assert check_name and check_price and check_quantity and check_sub_total, f"Product check failed for {p_name}"

    print("Tất cả sản phẩm đã được kiểm tra thành công trong giỏ hàng.")

    # Lấy phí vận chuyển
    shipping_charge_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//tr[td[text()='Shipping Charge']]//td[contains(text(), '৳')]"))
    )
    shipping_charge = float(shipping_charge_element.text.replace('৳', '').strip())
    total_price += shipping_charge

    # Lấy VAT
    vat_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//tr[td[text()='VAT']]//td[contains(text(), '৳')]"))
    )
    vat = float(vat_element.text.replace('৳', '').strip())
    total_price += vat

    # In thông tin tổng hợp
    print("Phí vận chuyển:", shipping_charge)
    print("VAT:", vat)
    print("Tổng số tiền cuối cùng:", total_price)

    # Kiểm tra URL hiện tại
    assert driver.current_url == "http://127.0.0.1:8000/cart", "Không chuyển hướng đến trang giỏ hàng."

    # Gọi hàm kiểm tra thanh toán
    test_check_out(driver)


# TC2: Kiểm tra thêm nhiều sản phẩm vào giỏ hàng và thanh toán
def test_many_product(driver):
    test_valid_login(driver)

    # Nhấn vào nút "Browse All"
    browse_all_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='submit'][value='Browse All']"))
    )
    browse_all_button.click()

    # Chờ chuyển hướng đến trang menu
    WebDriverWait(driver, 10).until(EC.url_to_be("http://127.0.0.1:8000/menu"))

    total_price = 0

    # Thông tin sản phẩm và kiểm tra
    products = [
        {"name": "Chocolate Cake", "xpath": "//form[contains(@action, 'http://127.0.0.1:8000/menu/1')]//button[contains(@class, 'btn-success') and text()='Add to Cart']"},
        {"name": "Klassy Pancake", "xpath": "//form[contains(@action, 'http://127.0.0.1:8000/menu/2')]//button[contains(@class, 'btn-success') and text()='Add to Cart']"},
        {"name": "Klassy Cup Cake", "xpath": "//form[contains(@action, 'http://127.0.0.1:8000/menu/4')]//button[contains(@class, 'btn-success') and text()='Add to Cart']"}
    ]

    product_details = []

    for product in products:
        # Nhấn vào nút "Add to Cart"
        add_to_cart_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, product["xpath"]))
        )
        add_to_cart_button.click()

        # Lấy giá sản phẩm
        product_price_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, f"//td[h2[contains(text(), '{product['name']}')]]//h4[contains(text(), '৳')]"))
        )
        product_price = float(product_price_element.text.replace('৳', '').strip())
        product_details.append({"name": product["name"], "price": product_price, "quantity": 1})
        total_price += product_price

    # Nhấn vào biểu tượng giỏ hàng
    shopping_cart_icon = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "i.fa-shopping-cart"))
    )
    shopping_cart_icon.click()

    # Chờ chuyển hướng đến trang giỏ hàng
    WebDriverWait(driver, 10).until(EC.url_to_be("http://127.0.0.1:8000/cart"))

    # Xác nhận thông tin trong giỏ hàng
    cart_rows = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, "//table//tr[td]"))
    )

    for i, cart_row in enumerate(cart_rows[:len(product_details)]):
        cart_td_elements = cart_row.find_elements(By.TAG_NAME, "td")

        # Lấy thông tin từ giỏ hàng
        cart_name = cart_td_elements[0].text.strip()
        cart_price = float(cart_td_elements[1].text.strip()[1:])  # Bỏ ký tự '৳'
        cart_quantity = int(cart_td_elements[2].text.strip())
        cart_sub_total = float(cart_td_elements[3].text.strip()[1:])  # Bỏ ký tự '৳'

        # Thông tin sản phẩm từ danh sách
        p_name = product_details[i]["name"]
        price = product_details[i]["price"]
        quantity = product_details[i]["quantity"]

        # Kiểm tra từng trường
        check_name = p_name == cart_name
        check_price = price == cart_price
        check_quantity = quantity == cart_quantity
        check_sub_total = (price * quantity) == cart_sub_total

        print(f"Check name: {p_name} - {check_name}")
        print(f"Check price: {price} - {check_price}")
        print(f"Check quantity: {quantity} - {check_quantity}")
        print(f"Check sub_total: {price * quantity} - {check_sub_total}")

        assert check_name and check_price and check_quantity and check_sub_total, f"Product check failed for {p_name}"

    print("Tất cả sản phẩm đã được kiểm tra thành công trong giỏ hàng.")

    # Lấy và cộng thêm phí vận chuyển và VAT
    shipping_charge_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//tr[td[text()='Shipping Charge']]//td[contains(text(), '৳')]"))
    )
    shipping_charge = float(shipping_charge_element.text.replace('৳', '').strip())
    total_price += shipping_charge

    vat_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//tr[td[text()='VAT']]//td[contains(text(), '৳')]"))
    )
    vat = float(vat_element.text.replace('৳', '').strip())
    total_price += vat

    print("Phí vận chuyển:", shipping_charge)
    print("VAT:", vat)
    print("Tổng số tiền cuối cùng:", total_price)

    test_check_out(driver)


# TC3: Kiểm tra thanh toán sản phẩm với số lượng nhiều
def test_quantity_product(driver):
    test_valid_login(driver)

    # Nhấn vào nút "Browse All"
    browse_all_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='submit'][value='Browse All']"))
    )
    browse_all_button.click()

    # Chờ chuyển hướng đến trang menu
    WebDriverWait(driver, 10).until(EC.url_to_be("http://127.0.0.1:8000/menu"))

    # Tìm ô nhập số lượng và thay đổi giá trị thành 1 cho sản phẩm Chocolate Cake
    quantity_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, "//h2[contains(text(), 'Chocolate Cake')]//following::input[@type='number'][@name='number']"))
    )
    quantity_input.clear()
    quantity_input.send_keys("3")  # Thay đổi giá trị số lượng thành 3
    quantity = int(quantity_input.get_attribute("value"))  # Lấy giá trị số lượng từ ô nhập liệu

    total_price = 0

    # Nhấn vào nút "Add to Cart" của sản phẩm "Chocolate Cake"
    add_to_cart_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//form[contains(@action, 'http://127.0.0.1:8000/menu/1')]//button[contains(@class, 'btn-success') and text()='Add to Cart']"))
    )
    add_to_cart_button.click()

    # Lấy giá sản phẩm
    product_price_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//td[h2[contains(text(), 'Chocolate Cake')]]//h4[contains(text(), '৳')]"))
    )
    product_price = float(product_price_element.text.replace('৳', '').strip())

    # Nhân giá sản phẩm với số lượng để tính tổng tiền của sản phẩm
    product_total = product_price * quantity
    total_price += product_total

    # In ra tổng tiền của sản phẩm
    print(f"Tổng tiền của {quantity} sản phẩm: {product_total} ৳")

    # Nhấn vào biểu tượng giỏ hàng
    shopping_cart_icon = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "i.fa-shopping-cart"))
    )
    shopping_cart_icon.click()

    # Chờ chuyển hướng đến trang giỏ hàng
    WebDriverWait(driver, 10).until(EC.url_to_be("http://127.0.0.1:8000/cart"))

    cart_row = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//tr[td[text()='Chocolate Cake']]"))
    )
    cart_td_elements = cart_row.find_elements(By.TAG_NAME, "td")

    # Lấy thông tin từ giỏ hàng
    cart_name = cart_td_elements[0].text.strip()
    cart_price = float(cart_td_elements[1].text.strip()[1:])  # Bỏ ký tự '৳'
    cart_quantity = int(cart_td_elements[2].text.strip())
    cart_sub_total = float(cart_td_elements[3].text.strip()[1:])  # Bỏ ký tự '৳'

    # Thông tin sản phẩm từ danh sách
    p_name = "Chocolate Cake"
    price = product_price
    quan = quantity

    # Kiểm tra từng trường
    check_name = p_name == cart_name
    check_price = price == cart_price
    check_quantity = quan == cart_quantity
    check_sub_total = (price * quan) == cart_sub_total

    print(f"Check name: {p_name} - {check_name}")
    print(f"Check price: {price} - {check_price}")
    print(f"Check quantity: {quan} - {check_quantity}")
    print(f"Check sub_total: {price * quan} - {check_sub_total}")

    assert check_name and check_price and check_quantity and check_sub_total, f"Product check failed for {p_name}"

    print("Tất cả sản phẩm đã được kiểm tra thành công trong giỏ hàng.")

    # Lấy phí vận chuyển
    shipping_charge_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//tr[td[text()='Shipping Charge']]//td[contains(text(), '৳')]"))
    )
    shipping_charge = float(shipping_charge_element.text.replace('৳', '').strip())
    total_price += shipping_charge

    # Lấy VAT
    vat_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//tr[td[text()='VAT']]//td[contains(text(), '৳')]"))
    )
    vat = float(vat_element.text.replace('৳', '').strip())
    total_price += vat

    # In thông tin tổng hợp
    print("Phí vận chuyển:", shipping_charge)
    print("VAT:", vat)
    print("Tổng số tiền cuối cùng:", total_price)

    # Kiểm tra URL hiện tại
    assert driver.current_url == "http://127.0.0.1:8000/cart", "Không chuyển hướng đến trang giỏ hàng."

    # Gọi hàm kiểm tra thanh toán
    test_check_out(driver)


# TC4: Kiểm tra thanh toán sản phẩm với số lượng âm
def test_quantity_negative_product(driver):
    test_valid_login(driver)
    time.sleep(1)

    # Nhấn vào nút "Browse All"
    browse_all_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='submit'][value='Browse All']"))
    )
    browse_all_button.click()
    time.sleep(1)

    # Chờ chuyển hướng đến trang menu
    WebDriverWait(driver, 10).until(EC.url_to_be("http://127.0.0.1:8000/menu"))

    # Tìm ô nhập số lượng và thay đổi giá trị thành -1 cho sản phẩm Chocolate Cake
    quantity_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, "//h2[contains(text(), 'Chocolate Cake')]//following::input[@type='number'][@name='number']"))
    )
    quantity_input.clear()
    quantity_input.send_keys("-1")  # Thay đổi giá trị số lượng thành 1
    quantity = int(quantity_input.get_attribute("value"))  # Lấy giá trị số lượng từ ô nhập liệu

    # Nhấn vào nút "Add to Cart" của sản phẩm "Chocolate Cake"
    add_to_cart_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH,
                                    "//form[contains(@action, 'http://127.0.0.1:8000/menu/1')]//button[contains(@class, 'btn-success') and text()='Add to Cart']"))
    )
    add_to_cart_button.click()
    time.sleep(1)

    # Kiểm tra thông báo lỗi nếu số lượng sản phẩm âm
    try:
        # Kiểm tra thông báo lỗi xuất hiện khi nhập số lượng âm
        error_message = driver.find_element(By.CSS_SELECTOR, "input:invalid")
        check_negative = error_message is not None
        if check_negative:
            print("Error is displayed successfully")
        else:
            print("Error is not displayed as expected")
    except NoSuchElementException:
        print("Error is displayed unsuccessfully")

    # Nhấn vào biểu tượng giỏ hàng
    shopping_cart_icon = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "i.fa-shopping-cart"))
    )
    shopping_cart_icon.click()
    time.sleep(1)

    # Chờ chuyển hướng đến trang giỏ hàng
    WebDriverWait(driver, 10).until(EC.url_to_be("http://127.0.0.1:8000/cart"))
    assert driver.current_url == "http://127.0.0.1:8000/cart", "Login failed: Not redirected to expected page."


# TC5: Kiểm tra cập nhật số lượng sản phẩm và thanh toán
def test_update_product(driver):
    test_valid_login(driver)

    # Nhấn vào nút "Browse All"
    browse_all_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='submit'][value='Browse All']"))
    )
    browse_all_button.click()

    # Chờ chuyển hướng đến trang menu
    WebDriverWait(driver, 10).until(EC.url_to_be("http://127.0.0.1:8000/menu"))

    total_price = 0

    # Thêm sản phẩm "Chocolate Cake"
    product_name = "Chocolate Cake"
    quantity_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, f"//h2[contains(text(), '{product_name}')]//following::input[@type='number'][@name='number']")
        )
    )
    quantity_input.clear()
    quantity_input.send_keys("1")
    quantity = int(quantity_input.get_attribute("value"))

    add_to_cart_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH,
                                    f"//form[contains(@action, 'http://127.0.0.1:8000/menu/1')]//button[contains(@class, 'btn-success') and text()='Add to Cart']"))
    )
    add_to_cart_button.click()

    product_price_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, f"//td[h2[contains(text(), '{product_name}')]]//h4[contains(text(), '৳')]")
        )
    )
    product_price = float(product_price_element.text.replace('৳', '').strip())
    product_total = product_price * quantity
    total_price_1 = product_total

    print(f"Tổng tiền của {quantity} {product_name}: {product_total} ৳")

    shopping_cart_icon = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "i.fa-shopping-cart"))
    )
    shopping_cart_icon.click()

    # Chờ chuyển hướng đến trang giỏ hàng
    WebDriverWait(driver, 10).until(EC.url_to_be("http://127.0.0.1:8000/cart"))

    cart_row = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//tr[td[text()='Chocolate Cake']]"))
    )
    cart_td_elements = cart_row.find_elements(By.TAG_NAME, "td")

    # Lấy thông tin từ giỏ hàng
    cart_name = cart_td_elements[0].text.strip()
    cart_price = float(cart_td_elements[1].text.strip()[1:])  # Bỏ ký tự '৳'
    cart_quantity = int(cart_td_elements[2].text.strip())
    cart_sub_total = float(cart_td_elements[3].text.strip()[1:])  # Bỏ ký tự '৳'

    # Thông tin sản phẩm từ danh sách
    p_name = "Chocolate Cake"
    price = product_price
    quan = quantity

    # Kiểm tra từng trường
    check_name = p_name == cart_name
    check_price = price == cart_price
    check_quantity = quan == cart_quantity
    check_sub_total = (price * quan) == cart_sub_total

    print(f"Check name: {p_name} - {check_name}")
    print(f"Check price: {price} - {check_price}")
    print(f"Check quantity: {quan} - {check_quantity}")
    print(f"Check sub_total: {price * quan} - {check_sub_total}")

    assert check_name and check_price and check_quantity and check_sub_total, f"Product check failed for {p_name}"

    print("Tất cả sản phẩm đã được kiểm tra thành công trong giỏ hàng.")

    # Thêm sản phẩm "Klassy Pancake"
    continue_shopping_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "a.btn.btn-warning"))
    )
    continue_shopping_button.click()

    product_name = "Klassy Pancake"
    quantity_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, f"//h2[contains(text(), '{product_name}')]//following::input[@type='number'][@name='number']")
        )
    )
    quantity_input.clear()
    quantity_input.send_keys("1")
    quantity = int(quantity_input.get_attribute("value"))

    add_to_cart_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH,
                                    f"//form[contains(@action, 'http://127.0.0.1:8000/menu/2')]//button[contains(@class, 'btn-success') and text()='Add to Cart']"))
    )
    add_to_cart_button.click()

    product_price_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, f"//td[h2[contains(text(), '{product_name}')]]//h4[contains(text(), '৳')]")
        )
    )
    product_price = float(product_price_element.text.replace('৳', '').strip())
    product_total = product_price * quantity
    total_price_2 = product_total

    print(f"Tổng tiền của {quantity} {product_name}: {product_total} ৳")

    shopping_cart_icon = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "i.fa-shopping-cart"))
    )
    shopping_cart_icon.click()

    # Chờ chuyển hướng đến trang giỏ hàng
    WebDriverWait(driver, 10).until(EC.url_to_be("http://127.0.0.1:8000/cart"))

    cart_row = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//tr[td[text()='Klassy Pancake']]"))
    )
    cart_td_elements = cart_row.find_elements(By.TAG_NAME, "td")

    # Lấy thông tin từ giỏ hàng
    cart_name = cart_td_elements[0].text.strip()
    cart_price = float(cart_td_elements[1].text.strip()[1:])  # Bỏ ký tự '৳'
    cart_quantity = int(cart_td_elements[2].text.strip())
    cart_sub_total = float(cart_td_elements[3].text.strip()[1:])  # Bỏ ký tự '৳'

    # Thông tin sản phẩm từ danh sách
    p_name = "Klassy Pancake"
    price = product_price
    quan = quantity

    # Kiểm tra từng trường
    check_name = p_name == cart_name
    check_price = price == cart_price
    check_quantity = quan == cart_quantity
    check_sub_total = (price * quan) == cart_sub_total

    print(f"Check name: {p_name} - {check_name}")
    print(f"Check price: {price} - {check_price}")
    print(f"Check quantity: {quan} - {check_quantity}")
    print(f"Check sub_total: {price * quan} - {check_sub_total}")

    assert check_name and check_price and check_quantity and check_sub_total, f"Product check failed for {p_name}"

    print("Tất cả sản phẩm đã được kiểm tra thành công trong giỏ hàng.")

    total_price = total_price_1 + total_price_2

    # Lấy phí vận chuyển
    shipping_charge_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//tr[td[text()='Shipping Charge']]//td[contains(text(), '৳')]"))
    )
    shipping_charge = float(shipping_charge_element.text.replace('৳', '').strip())
    total_price += shipping_charge

    # Lấy VAT
    vat_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//tr[td[text()='VAT']]//td[contains(text(), '৳')]"))
    )
    vat = float(vat_element.text.replace('৳', '').strip())
    total_price += vat

    # In thông tin tổng hợp
    print("Phí vận chuyển:", shipping_charge)
    print("VAT:", vat)
    print("Tổng số tiền cuối cùng:", total_price)

    # Kiểm tra URL hiện tại
    assert driver.current_url == "http://127.0.0.1:8000/cart", "Không chuyển hướng đến trang giỏ hàng."

    test_check_out(driver)


# TC6: Kiểm tra xóa sản phẩm ra khỏi giỏ hàng
def test_remove_cart(driver):
    test_valid_login(driver)
    time.sleep(1)

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
    time.sleep(1)

    # Nhấn vào nút "Browse All"
    browse_all_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='submit'][value='Browse All']"))
    )
    browse_all_button.click()

    # Chờ chuyển hướng đến trang menu
    WebDriverWait(driver, 10).until(EC.url_to_be("http://127.0.0.1:8000/menu"))

    # Nhấn vào nút "Out of Stock" của sản phẩm "BlueBerry Cake"
    out_of_stock_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//p[contains(@class, 'btn-danger') and text()='Out of Stock']"))
    )
    out_of_stock_element.click()
    time.sleep(1)

    # Kiểm tra thông báo xuất hiện
    out_of_stock_message = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//p[@class='btn btn-danger' and text()='Out of Stock']"))
    )
    if "Out of Stock" in out_of_stock_message.text:
        print("Thông báo: Sản phẩm này đã hết hàng.")
    else:
        raise AssertionError("Out of stock message not displayed.")


