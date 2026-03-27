import time
import random
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def boss_search_like_human():
    # 使用 undetected_chromedriver 启动浏览器
    options = uc.ChromeOptions()
    # options.add_argument('--headless') # 绝对不要开无头模式
    
    driver = uc.Chrome(options=options)

    try:
        # 1. 访问首页进行登录
        print("🚀 正在打开首页，请先完成登录...")
        driver.get("https://www.zhipin.com/")
        
        # 预留点时间看一眼有没有滑块，有的话手动滑一下
        input("👉 请先在浏览器里扫码登录。登录成功看到‘推荐职位’后，回来按【回车】...")

        # 2. 模拟人类搜索行为（不要直接跳转 URL）
        print("🔍 正在模拟搜索行为...")
        
        # 寻找搜索框（根据 BOSS 首页结构）
        search_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "ipt-search"))
        )
        
        # 清空并输入 Java
        search_input.clear()
        for char in "Java":  # 模拟打字速度
            search_input.send_keys(char)
            time.sleep(random.uniform(0.1, 0.3))
        
        # 敲回车或者点搜索图标
        search_input.send_keys(Keys.ENTER)
        
        print("⏳ 等待搜索结果加载...")
        time.sleep(5) # 给 Token 生成留出缓冲

        # 3. 检查是否出现了验证码
        if "security-check" in driver.current_url or "验证" in driver.title:
            print("⚠️ 哎呀，还是弹验证码了！请在浏览器里手动过一下。")
            input("👉 过完验证码、看到职位列表后，请按【回车】继续...")

        # 4. 抓取数据
        wait = WebDriverWait(driver, 15)
        # 尝试定位职位列表
        job_elements = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "job-card-wrapper")))
        
        print(f"✅ 抓取成功！当前页面共找到 {len(job_elements)} 个岗位：")
        
        for job in job_elements:
            try:
                name = job.find_element(By.CLASS_NAME, "job-name").text
                salary = job.find_element(By.CLASS_NAME, "salary").text
                com = job.find_element(By.CLASS_NAME, "company-name").text
                print(f"[{com}] {name} · {salary}")
            except:
                continue

    except Exception as e:
        print(f"❌ 运行中出现错误: {e}")
        print(f"当前 URL: {driver.current_url}")
    finally:
        input("\n🏁 任务完成，按回车关闭浏览器...")
        driver.quit()

if __name__ == "__main__":
    boss_search_like_human()