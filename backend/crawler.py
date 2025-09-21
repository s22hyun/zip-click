import time
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException

def setup_driver():
    options = uc.ChromeOptions()
    options.binary_location = "/usr/bin/chromium"
    options.add_argument('--headless=new')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("window-size=1920x1080")
    driver = uc.Chrome(
        options=options,
        driver_executable_path="/usr/bin/chromedriver"
    )
    return driver

def scrape_site(driver, site_info):
    portal_url = site_info.get("portal_url")
    target_url = site_info["target_url"]
    site_name = site_info["name"]
    iframe_id = site_info.get("iframe_id")
    selector = site_info["selector"]

    print(f"\n✅ {site_name} 크롤링 시작...")
    
    try:
        if portal_url:
            print(f"   - 포털 방문: {portal_url}")
            driver.get(portal_url)
            time.sleep(2)

        print(f"   - 목표 페이지로 이동: {target_url}")
        driver.get(target_url)

        if iframe_id:
            WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.ID, iframe_id)))
            print(f"   - '{iframe_id}' iframe으로 전환 완료")

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
        elements = driver.find_elements(By.CSS_SELECTOR, selector)
        
        print(f"\n--- {site_name} 공고 ({len(elements)}개) ---")
        for el in elements:
            title = el.text
            link = el.get_attribute('href')
            if title.strip():
                print(f"   - 제목: {title.strip()}")
                print(f"     링크: {link}")
        
        print("--------------------")

    except TimeoutException:
        print(f"   - 🚨 오류: '{selector}' 요소를 찾는 데 시간이 초과되었습니다.")
        screenshot_path = f"{site_name}_error.png"
        html_path = f"{site_name}_error.html"
        driver.save_screenshot(screenshot_path)
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        print(f"   - 디버깅 파일 저장 완료: {screenshot_path}, {html_path}")
    except Exception as e:
        print(f"   - 🚨 오류: {site_name} 크롤링 중 예측하지 못한 문제가 발생했습니다: {e}")
    finally:
        if iframe_id:
            driver.switch_to.default_content()
        print(f"🏁 {site_name} 크롤링 완료.")


if __name__ == "__main__":
    lh_info = {
        "name": "LH 청약플러스",
        "target_url": "https://apply.lh.or.kr/lhapply/apply/wt/wrtanc/selectWrtancList.do?mi=1026",
        "selector": "#sub_cont > div > table > tbody > tr > td.txt_l > a" 
    }
    
    sh_info = {
        "name": "SH 인터넷청약시스템",
        "target_url": "https://www.i-sh.co.kr/main/lay2/program/S1T294C295/www/brd/m_241/list.do",
        "selector": "#listTb td.txtL > a"
    }

    driver = setup_driver()
    try:
        scrape_site(driver, lh_info)
        scrape_site(driver, sh_info)
    finally:
        driver.quit()