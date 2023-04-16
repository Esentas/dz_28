import pytest
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
import settings

# RT-01
def test_open_page_auth(browser):
    auth = browser.find_element(By.CLASS_NAME, 'card-container__title')
    assert auth.text == 'авторизация', 'Fail'
# RT-02
def test_change_tab_on_mail(browser):
    browser.find_element(By.ID, 'username').send_keys(settings.mail)
    browser.find_element(By.ID, 'password').click()
    assert browser.find_element(By.XPATH, '//div[contains(@class, "rt-tab--active")]').text == 'почта'
# RT-03
def test_change_tab_on_login(browser):
    browser.find_element(By.ID, 'username').send_keys(settings.login)
    browser.find_element(By.ID, 'password').click()
    assert browser.find_element(By.XPATH, '//div[contains(@class, "rt-tab--active")]').text == 'логин'

# RT-04
def test_change_tab_on_personal_account(browser):
    browser.find_element(By.ID, 'username').send_keys('123456789012')
    browser.find_element(By.ID, 'password').click()
    assert browser.find_element(By.XPATH, '//div[contains(@class, "rt-tab--active")]').text == 'лицевой счёт', 'FAIL'
# RT-05
def test_redirect_reset_credentials(browser):
    browser.find_element(By.ID, 'forgot_password').click()
    assert browser.find_element(By.CLASS_NAME, 'card-container__title').text == 'восстановление пароля'
# RT-06
def test_agreement(browser):
    browser.find_element(By.XPATH, '//div[@class="auth-policy"]/a').click()
    browser.switch_to.window(browser.window_handles[1])
    title = browser.find_element(By.XPATH, '//div[@id="title"]/h1').text
    assert title.startswith('публичная оферта'), 'FAIL'
# RT-07
def test_auth_vk(browser):
    browser.find_element(By.ID, 'oidc_vk').click()
    assert 'vk.com' in browser.find_element(By.XPATH, '//div[@class="oauth_head"]/a').get_attribute('href')
    assert 'vk' in browser.current_url
# RT-08
def test_auth_ok(browser):
    browser.find_element(By.ID, 'oidc_ok').click()
    assert 'Одноклассники' == browser.find_element(By.XPATH, '//div[@class="ext-widget_h_tx"]').text
    assert 'ok' in browser.current_url
# RT-09
def test_auth_mail(browser):
    browser.find_element(By.ID, 'oidc_mail').click()
    assert 'mail.ru' in browser.find_element(By.XPATH, '//span[@class="header__logo"]').text.lower()
    assert 'mail' in browser.current_url
# RT-10
def test_auth_google(browser):
    browser.find_element(By.ID, 'oidc_google').click()
    assert 'google' in browser.current_url
# RT-11
def test_auth_yandex(browser):
    browser.find_element(By.ID, 'oidc_ya').click()
    WebDriverWait(browser, 15).until(EC.presence_of_element_located((By.ID, 'passp:sign-in')))
    assert 'yandex' in browser.current_url
# RT-12
def test_redirect_registration(browser):
    browser.find_element(By.ID, 'kc-register').click()
    assert browser.find_element(By.XPATH, '//h1[@class="card-container__title"]').text == 'регистрация'
# RT-13
def test_privacy_policy_footer(browser):
    browser.find_elements(By.XPATH, '//a[@id="rt-footer-agreement-link"]/span')[0].click()
    browser.switch_to.window(browser.window_handles[1])
    title = browser.find_element(By.XPATH, '//div[@id="title"]/h1').text
    assert title.startswith('публичная оферта'), 'FAIL'
# RT-14
def test_agreements_footer(browser):
    browser.find_elements(By.XPATH, '//a[@id="rt-footer-agreement-link"]/span')[1].click()
    browser.switch_to.window(browser.window_handles[1])
    title = browser.find_element(By.XPATH, '//div[@id="title"]/h1').text
    assert title.startswith('публичная оферта'), 'FAIL'
# RT-15
@pytest.mark.xfail(reason='аккаунт уже зарегистрирован')
def test_registration(browser):
    browser.find_element(By.ID, 'kc-register').click()
    inputs = browser.find_elements(By.XPATH, '//input[contains(@class, "rt-input__input")]')
    inputs[0].send_keys('Есентас')
    inputs[1].send_keys('Жексибаев')
    inputs[2].send_keys('Екатеринбург')
    inputs[3].send_keys('polamilsa@mail.ru')
    inputs[4].send_keys('Qwerty1234!')
    inputs[5].send_keys('Qwerty1234!')
    browser.find_element(By.NAME, 'register').click()
    assert browser.find_element(By.XPATH, '//h1[@class="card-container__title"]').text == 'подтверждение email', 'такой пользователь зарегистрирован'
# RT-16
@pytest.mark.xfail(reason='Не разгадана капча')
def test_reset_password_by_mail(browser):
    browser.find_element(By.ID, 'forgot_password').click()
    browser.find_element(By.ID, 'username').send_keys(settings.mail)
    browser.find_element(By.ID, 'captcha').send_keys()
    browser.find_element(By.ID, 'reset')
    assert browser.find_element(By.XPATH, '//h1[@class="card-container__title"]').text == 'восстановление пароля'
# RT-17
def test_auth_by_mail(browser):
    browser.find_element(By.ID, 'username').send_keys(settings.mail)
    browser.find_element(By.ID, 'password').send_keys(settings.password)
    browser.find_element(By.ID, 'kc-login').click()
    assert browser.find_element(By.ID, 'logout-btn')
# RT-18
def test_empty_form(browser):
    browser.find_element(By.ID, 'kc-register').click()
    browser.find_element(By.NAME, 'register').click()
    err = browser.find_elements(By.XPATH, '//span[contains(@class, "rt-input-container__meta--error")]')
    assert len(err) == 5
# RT-19
@pytest.mark.xfail(reason='появилась капча')
def test_auth_incorrect_mail(browser):
    inputs = browser.find_elements(By.XPATH, '//input[contains(@class, "rt-input__input")]')
    inputs[0].send_keys('notvalid@ru.ru')
    inputs[1].send_keys(settings.password)
    browser.find_element(By.ID, 'kc-login').click()
    assert browser.find_element(By.ID, 'form-error-message').text == 'неверный логин или пароль'
