from playwright.sync_api import sync_playwright

def scrape_titles():
    url = "https://www.mayikt.com/showcoulist.html"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # 无头模式
        page = browser.new_page()
        
        page.goto(url)

        # 等待页面加载（关键！）
        page.wait_for_timeout(5000)

        # 根据页面结构抓取标题（需要你确认具体class）
        titles = page.locator(".a-tittile").all_text_contents()

        for i, title in enumerate(titles, 1):
            print(f"{i}. {title}")

        # 保存到csv文件，表头为序号，标题
        with open("titles.csv", "w", encoding="utf-8") as f:  
            f.write("序号,标题\n")
            for i, title in enumerate(titles, 1):
                f.write(f"{i},{title}\n")

        browser.close()


if __name__ == "__main__":
    scrape_titles()