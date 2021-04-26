from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy
from selenium.webdriver.common.proxy import ProxyType

# proxy = Proxy(
#      {
#           'proxyType': ProxyType.MANUAL,
#           'httpProxy': 'ip_or_host:port'
#      }
# )
desired_capabilities = webdriver.DesiredCapabilities.PHANTOMJS.copy()
# proxy.add_to_capabilities(desired_capabilities)
driver = webdriver.PhantomJS(desired_capabilities=desired_capabilities,executable_path="G:\\WeatherReact\\test\\phantom\\bin\\phantomjs.exe")
driver.get('https://www.boredpanda.com/')
print(driver.page_source)