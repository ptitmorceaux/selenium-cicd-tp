import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import os

from calculator_page import CalculatorPage

class TestCalculator:
    @pytest.fixture(scope="class")
    def driver(self):
        """Configuration du driver Chrome pour les tests"""
        chrome_options = Options()
        # Configuration pour environnement CI/CD
        if os.getenv('CI'):
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--window-size=1920,1080')
        
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.implicitly_wait(10)
        yield driver
        driver.quit()

    def test_page_loads(self, driver):
        """Test 1: Vérifier que la page se charge correctement"""
        page = CalculatorPage(driver)
        page.load_page()
        
        # Vérifier le titre
        assert "Calculatrice Simple" in driver.title
        
        # Vérifier la présence des éléments principaux
        assert driver.find_element(By.ID, "num1").is_displayed()
        assert driver.find_element(By.ID, "num2").is_displayed()
        assert driver.find_element(By.ID, "operation").is_displayed()
        assert driver.find_element(By.ID, "calculate").is_displayed()

    def test_addition(self, driver):
        """Test 2: Tester l'addition"""
        page = CalculatorPage(driver)
        page.load_page()
        
        # Saisir les valeurs
        page.enter_first_number("10")
        page.enter_second_number("5")
        
        # Sélectionner l'addition
        page.select_operation("add")
        
        # Cliquer sur calculer
        page.click_calculate()
        
        # Vérifier le résultat
        result = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "result"))
        )
        assert "Résultat: 15" in result.text

    def test_division_by_zero(self, driver):
        """Test 3: Tester la division par zéro"""
        page = CalculatorPage(driver)
        page.load_page()
        
        # Saisir les valeurs
        page.enter_first_number("10")
        page.enter_second_number("0")
        
        # Sélectionner la division
        page.select_operation("divide")
        
        page.click_calculate()
        
        # Vérifier le message d'erreur
        result = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "result"))
        )
        assert "Erreur: Division par zéro" in result.text

    def test_all_operations(self, driver):
        """Test 4: Tester toutes les opérations"""
        page = CalculatorPage(driver)
        page.load_page()
        
        operations = [
            ("add", "8", "2", "10"),
            ("subtract", "8", "2", "6"),
            ("multiply", "8", "2", "16"),
            ("divide", "8", "2", "4")
        ]
        
        for op, num1, num2, expected in operations:
            # Nettoyer les champs
            page.clear_fields()
            
            # Saisir les valeurs
            page.enter_first_number(num1)
            page.enter_second_number(num2)
            
            # Sélectionner l'opération
            page.select_operation(op)
            
            # Calculer
            page.click_calculate()
            
            # Vérifier le résultat
            result = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "result"))
            )
            assert expected in result.text
            time.sleep(1)

    def test_all_operations_with_decimals(self, driver):
        """Test 4: Tester toutes les opérations avec des nombres décimaux"""
        page = CalculatorPage(driver)
        page.load_page()
        
        operations = [
            ("add", "8.5", "2.3", "10.8"),
            ("subtract", "8.5", "2.3", "6.2"),
            ("multiply", "8.5", "2.3", "19.55"),
            ("divide", "12.4", "1.2", "10.33")
        ]
        
        for op, num1, num2, expected in operations:
            # Nettoyer les champs
            page.clear_fields()
            
            # Saisir les valeurs
            page.enter_first_number(num1)
            page.enter_second_number(num2)
            
            # Sélectionner l'opération
            page.select_operation(op)
            
            # Calculer
            page.click_calculate()
            
            # Vérifier le résultat
            result = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "result"))
            )
            assert expected in result.text
            time.sleep(1)

    def test_all_operations_with_negative_numbers(self, driver):
        """Test 4: Tester toutes les opérations avec des nombres négatifs"""
        page = CalculatorPage(driver)
        page.load_page()
        
        operations = [
            ("add", "-8", "2", "-6"),
            ("add", "-8", "-2", "-10"),
            ("add", "8", "-2", "6"),
            ("subtract", "8", "-2", "10"),
            ("subtract", "-8", "-2", "-6"),
            ("subtract", "-8", "2", "-10"),
            ("multiply", "8", "-2", "-16"),
            ("multiply", "-8", "-2", "16"),
            ("multiply", "-8", "2", "-16"),
            ("divide", "-12", "2", "-6"),
            ("divide", "-12", "-2", "6"),
            ("divide", "12", "-2", "-6")
        ]
        
        for op, num1, num2, expected in operations:
            # Nettoyer les champs
            page.clear_fields()
            
            # Saisir les valeurs
            page.enter_first_number(num1)
            page.enter_second_number(num2)
            
            # Sélectionner l'opération
            page.select_operation(op)
            
            # Calculer
            page.click_calculate()
            
            # Vérifier le résultat
            result = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "result"))
            )
            assert expected in result.text
            time.sleep(1)

    def test_page_load_time(self, driver):
        """Test 5: Mesurer le temps de chargement de la page"""
        start_time = time.time()

        page = CalculatorPage(driver)
        page.load_page()
        
        # Attendre que la page soit complètement chargée
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "calculator"))
        )
        
        load_time = time.time() - start_time
        print(f"Temps de chargement: {load_time:.2f} secondes")
        
        # Vérifier que le chargement prend moins de 3 secondes
        assert load_time < 3.0, f"Page trop lente à charger: {load_time:.2f}s"

if __name__ == "__main__":
    pytest.main(["-v", "--html=report.html", "--self-contained-html"])