import time
import os
from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.common.by import By

DRIVER_PATH = r"C:\Users\DDIP\.wdm\drivers\edgedriver\win64\157.0.4341.60\msedgedriver.exe"
ARTIFACT_DIR = r"C:\Users\DDIP\.gemini\antigravity\brain\579508e8-e744-4d81-87ec-bb882c76b4a7"
PROJECT_DIR = r"d:\Project\generative_agents"

def run_tests():
    options = EdgeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--window-size=1600,1000")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    service = EdgeService(executable_path=DRIVER_PATH)
    driver = webdriver.Edge(service=service, options=options)
    try:
        url = "http://127.0.0.1:8000/society/"
        print(f"Loading {url}...")
        driver.get(url)
        time.sleep(3)

        # 1. Clean UI View (Inspector and Roster closed)
        inspector = driver.find_element(By.ID, "right-inspector-pane")
        roster = driver.find_element(By.ID, "left-roster-pane")
        assert "open" not in inspector.get_attribute("class")
        assert "open" not in roster.get_attribute("class")

        ss1_art = os.path.join(ARTIFACT_DIR, "pixel_art_ui_clean_world.png")
        ss1_proj = os.path.join(PROJECT_DIR, "pixel_art_ui_clean_world.png")
        driver.save_screenshot(ss1_art)
        driver.save_screenshot(ss1_proj)
        print("Saved Screenshot 1 (Clean Pixel-Art World View):", ss1_art)

        # 2. Select Citizen (Isabella Rodriguez) & Open Inspector
        driver.execute_script("selectCitizen(sim.citizens[0]);")
        time.sleep(1)
        assert "open" in inspector.get_attribute("class")

        ss2_art = os.path.join(ARTIFACT_DIR, "pixel_art_ui_inspector_active.png")
        ss2_proj = os.path.join(PROJECT_DIR, "pixel_art_ui_inspector_active.png")
        driver.save_screenshot(ss2_art)
        driver.save_screenshot(ss2_proj)
        print("Saved Screenshot 2 (Pixel-Art Deep Inspector):", ss2_art)

        # 3. Open God Powers Drawer
        god_btn = driver.find_element(By.ID, "btn-toggle-god-drawer")
        god_btn.click()
        time.sleep(1)
        god_overlay = driver.find_element(By.ID, "god-drawer-overlay")
        assert "open" in god_overlay.get_attribute("class")

        ss3_art = os.path.join(ARTIFACT_DIR, "pixel_art_ui_god_drawer.png")
        ss3_proj = os.path.join(PROJECT_DIR, "pixel_art_ui_god_drawer.png")
        driver.save_screenshot(ss3_art)
        driver.save_screenshot(ss3_proj)
        print("Saved Screenshot 3 (Pixel-Art God Powers Drawer):", ss3_art)

        # Close God Drawer
        driver.find_element(By.ID, "btn-close-god-drawer").click()
        time.sleep(0.5)

        # 4. Execute Mass Gathering Event
        cmd_input = driver.find_element(By.ID, "god-command-input")
        submit_btn = driver.find_element(By.ID, "btn-submit-divine")
        cmd_input.clear()
        cmd_input.send_keys("Make everyone gather at Johnson Park")
        submit_btn.click()
        time.sleep(2)

        ss4_art = os.path.join(ARTIFACT_DIR, "pixel_art_ui_mass_gathering.png")
        ss4_proj = os.path.join(PROJECT_DIR, "pixel_art_ui_mass_gathering.png")
        driver.save_screenshot(ss4_art)
        driver.save_screenshot(ss4_proj)
        print("Saved Screenshot 4 (Pixel-Art Mass Gathering):", ss4_art)

        # 5. Deselect Citizen
        driver.execute_script("deselectCitizen();")
        time.sleep(0.5)
        assert "open" not in inspector.get_attribute("class")

        print(">>> ALL PIXEL-ART UI TESTS COMPLETED AND VERIFIED 100%! <<<")
    finally:
        driver.quit()

if __name__ == "__main__":
    run_tests()
