import time
import os
from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.common.by import By

DRIVER_PATH = r"C:\Users\DDIP\.wdm\drivers\edgedriver\win64\157.0.4341.60\msedgedriver.exe"
ARTIFACT_DIR = r"C:\Users\DDIP\.gemini\antigravity\brain\579508e8-e744-4d81-87ec-bb882c76b4a7"

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
        time.sleep(3) # Wait for assets and Phaser to load

        # 1. Verify default clean screen state (Inspector and Roster closed)
        inspector = driver.find_element(By.ID, "right-inspector-pane")
        roster = driver.find_element(By.ID, "left-roster-pane")
        
        inspector_classes = inspector.get_attribute("class")
        roster_classes = roster.get_attribute("class")
        print("Initial Inspector class:", inspector_classes)
        print("Initial Roster class:", roster_classes)
        assert "open" not in inspector_classes, "Inspector should be closed by default!"
        assert "open" not in roster_classes, "Roster should be closed by default!"

        # Screenshot 1: Clean Living 2D World with God's Command Console
        ss1 = os.path.join(ARTIFACT_DIR, "god_simulator_clean_view.png")
        driver.save_screenshot(ss1)
        print("Saved screenshot 1:", ss1)

        # 2. Test Divine Command: "Make Isabella go to cafe"
        cmd_input = driver.find_element(By.ID, "god-command-input")
        submit_btn = driver.find_element(By.ID, "btn-submit-divine")

        cmd_input.clear()
        cmd_input.send_keys("Make Isabella go to cafe")
        submit_btn.click()
        time.sleep(1)

        feedback_card = driver.find_element(By.ID, "command-feedback-card")
        feedback_text = driver.find_element(By.ID, "feedback-text").text
        print("Command Feedback 1:", feedback_text)
        assert "Hobbs Cafe" in feedback_text or "commanded" in feedback_text

        # 3. Test Weather Command: "Make it rain for two hours"
        cmd_input.clear()
        cmd_input.send_keys("Make it rain for two hours")
        submit_btn.click()
        time.sleep(1)

        weather_desc = driver.find_element(By.ID, "weather-desc").text
        print("Weather Desc:", weather_desc)
        assert "Rain" in weather_desc

        # 4. Test Money Command: "Give Maria 500 coins"
        cmd_input.clear()
        cmd_input.send_keys("Give Maria 500 coins")
        submit_btn.click()
        time.sleep(1)

        feedback_text = driver.find_element(By.ID, "feedback-text").text
        print("Money Command Feedback:", feedback_text)
        assert "500" in feedback_text

        # 5. Test Selecting an Agent (Click Roster or direct JS selectCitizen)
        driver.execute_script("selectCitizen(sim.citizens[0]);") # Isabella
        time.sleep(1)

        inspector_classes = inspector.get_attribute("class")
        print("Inspector class after selecting Isabella:", inspector_classes)
        assert "open" in inspector_classes, "Inspector should be open after selecting citizen!"

        inspect_name = driver.find_element(By.ID, "inspect-name").text
        print("Inspecting Citizen Name:", inspect_name)
        assert "Isabella" in inspect_name

        # Screenshot 2: Divine Interventions & Inspector Active with Rain
        ss2 = os.path.join(ARTIFACT_DIR, "god_simulator_inspector_rain.png")
        driver.save_screenshot(ss2)
        print("Saved screenshot 2:", ss2)

        # 6. Test God Powers World Control Drawer
        god_btn = driver.find_element(By.ID, "btn-toggle-god-drawer")
        god_btn.click()
        time.sleep(1)

        god_overlay = driver.find_element(By.ID, "god-drawer-overlay")
        assert "open" in god_overlay.get_attribute("class"), "God drawer should be open!"

        # Screenshot 3: God Powers Drawer
        ss3 = os.path.join(ARTIFACT_DIR, "god_simulator_powers_drawer.png")
        driver.save_screenshot(ss3)
        print("Saved screenshot 3:", ss3)

        # Close God Drawer
        driver.find_element(By.ID, "btn-close-god-drawer").click()
        time.sleep(0.5)

        # 7. Test Mass Event: "Make everyone gather at Johnson Park"
        cmd_input.clear()
        cmd_input.send_keys("Make everyone gather at Johnson Park")
        submit_btn.click()
        time.sleep(2)

        feedback_text = driver.find_element(By.ID, "feedback-text").text
        print("Mass Event Feedback:", feedback_text)
        assert "Johnson Park" in feedback_text

        # Screenshot 4: Mass Gathering in Action
        ss4 = os.path.join(ARTIFACT_DIR, "god_simulator_mass_gathering.png")
        driver.save_screenshot(ss4)
        print("Saved screenshot 4:", ss4)

        # 8. Test Deselecting on empty ground click
        driver.execute_script("deselectCitizen();")
        time.sleep(0.5)
        inspector_classes = inspector.get_attribute("class")
        assert "open" not in inspector_classes, "Inspector should close upon deselecting!"

        print(">>> ALL 8 GOD SIMULATOR TESTS PASSED WITH 100% SUCCESS! <<<")
    finally:
        driver.quit()

if __name__ == "__main__":
    run_tests()
