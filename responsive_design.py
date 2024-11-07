import time

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from login_logout import test_valid_login


@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()


# TC1: Kiểm tra giao diện trên các kích thước màn hình khác nhau
def test_screen_size(driver):
    test_valid_login(driver)  # Gọi hàm kiểm tra đăng nhập hợp lệ
    time.sleep(3)

    # Lấy kích thước hiện tại của cửa sổ trình duyệt
    width, height = 800, 600  # Kích thước cửa sổ nhỏ
    driver.set_window_size(width, height)  # Thay đổi kích thước cửa sổ nhỏ
    time.sleep(3)  # Dừng lại để kiểm tra

    # Thay đổi cửa sổ thành kích thước lớn
    width, height = 1920, 1080  # Kích thước cửa sổ lớn
    driver.set_window_size(width, height)  # Thay đổi kích thước cửa sổ lớn
    time.sleep(3)  # Dừng lại để kiểm tra

    # Thay đổi cửa sổ trở lại kích thước ban đầu (nhỏ)
    driver.set_window_size(800, 600)  # Kích thước ban đầu
    time.sleep(3)  # Dừng lại để kiểm tra