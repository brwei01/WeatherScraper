from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time

# 配置 Chrome 选项 / set proxy for selenium
chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")  # 连接本地调试端口
chrome_options.add_argument("--proxy-server=http://127.0.0.1:9222")  # 设置代理服务器地址

# 设置 ChromeDriver 服务, 替换为chromedriver 路径(若没有将chromedriver可执行文件放置在python安装目录下)
# chrome_service = Service('/path/to/chromedriver') 

# 启动浏览器
# driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
driver = webdriver.Chrome(options=chrome_options)

# 打开测试页面
driver.get("https://www.aqistudy.cn/html/city_detail.php?v=1.10")
# driver.get("https://www.aqistudy.cn/html/city_realtime.php?v=2.3")

WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "tabs-inner")))
# 定位到“综合”选项卡并点击
comprehensive_tab = driver.find_element(By.XPATH, "//span[text()='综合']/ancestor::a")
comprehensive_tab.click()

# 关闭浏览器
# driver.quit()
