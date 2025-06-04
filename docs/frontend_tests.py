import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import logging
import time

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("frontend_tests.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("frontend_tests")

class FrontendTests(unittest.TestCase):
    """Testes automatizados para o frontend do Sistema de Triagem"""
    
    BASE_URL = "http://localhost:3000"
    
    def setUp(self):
        """Configuração inicial para cada teste"""
        # Inicializar o driver do Chrome
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')  # Executar em modo headless
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        
        self.driver = webdriver.Chrome(options=options)
        self.driver.set_window_size(1366, 768)  # Tamanho padrão de laptop
        logger.info("Driver do Chrome inicializado")
    
    def tearDown(self):
        """Limpeza após cada teste"""
        self.driver.quit()
        logger.info("Driver do Chrome encerrado")
    
    def test_home_page_load(self):
        """Teste de carregamento da página inicial"""
        self.driver.get(self.BASE_URL)
        
        # Verificar se o título da página está correto
        self.assertIn("Sistema de Triagem - HCI", self.driver.title)
        
        # Verificar se o formulário de triagem está presente
        try:
            form = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "form"))
            )
            self.assertIsNotNone(form)
            
            # Verificar se o campo de sintomas está presente
            textarea = self.driver.find_element(By.ID, "symptoms")
            self.assertIsNotNone(textarea)
            
            # Verificar se o botão de envio está presente
            button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            self.assertIsNotNone(button)
            
            logger.info("Teste de carregamento da página inicial concluído com sucesso")
        except TimeoutException:
            self.fail("Timeout ao carregar elementos da página inicial")
    
    def test_triagem_submission(self):
        """Teste de envio do formulário de triagem"""
        self.driver.get(self.BASE_URL)
        
        try:
            # Preencher o campo de sintomas
            textarea = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "symptoms"))
            )
            textarea.send_keys("Paciente com febre alta, tosse seca e dificuldade para respirar há 3 dias.")
            
            # Clicar no botão de envio
            button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            button.click()
            
            # Aguardar o resultado da triagem (pode demorar devido à chamada à API)
            result_container = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.CLASS_NAME, "result-container"))
            )
            
            # Verificar se a classificação está presente
            classification = self.driver.find_element(By.CLASS_NAME, "classification")
            self.assertIsNotNone(classification)
            
            # Verificar se as seções de justificativa e condutas estão presentes
            sections = self.driver.find_elements(By.CLASS_NAME, "section")
            self.assertGreaterEqual(len(sections), 2)
            
            logger.info("Teste de envio do formulário de triagem concluído com sucesso")
        except TimeoutException:
            self.fail("Timeout ao processar triagem")
    
    def test_admin_login(self):
        """Teste de login na área administrativa"""
        self.driver.get(f"{self.BASE_URL}/admin")
        
        try:
            # Verificar se o formulário de login está presente
            form = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "form"))
            )
            
            # Preencher campos de login
            username_input = self.driver.find_element(By.ID, "username")
            password_input = self.driver.find_element(By.ID, "password")
            
            username_input.send_keys("admin")
            password_input.send_keys("admin")
            
            # Clicar no botão de login
            button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            button.click()
            
            # Aguardar redirecionamento para o dashboard
            WebDriverWait(self.driver, 10).until(
                EC.url_contains("/admin/dashboard")
            )
            
            # Verificar se está na página de dashboard
            self.assertIn("/admin/dashboard", self.driver.current_url)
            
            logger.info("Teste de login na área administrativa concluído com sucesso")
        except TimeoutException:
            self.fail("Timeout ao processar login administrativo")
    
    def test_responsive_mobile(self):
        """Teste de responsividade em dispositivo móvel"""
        # Configurar tamanho de tela para simular dispositivo móvel
        self.driver.set_window_size(375, 667)  # iPhone 8
        
        self.driver.get(self.BASE_URL)
        
        try:
            # Verificar se o formulário está visível e utilizável
            form = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "form"))
            )
            
            # Verificar se o campo de sintomas está visível
            textarea = self.driver.find_element(By.ID, "symptoms")
            self.assertTrue(textarea.is_displayed())
            
            # Verificar se o botão de envio está visível
            button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            self.assertTrue(button.is_displayed())
            
            logger.info("Teste de responsividade em dispositivo móvel concluído com sucesso")
        except TimeoutException:
            self.fail("Timeout ao carregar elementos em visualização móvel")
    
    def test_responsive_tablet(self):
        """Teste de responsividade em tablet"""
        # Configurar tamanho de tela para simular tablet
        self.driver.set_window_size(768, 1024)  # iPad
        
        self.driver.get(self.BASE_URL)
        
        try:
            # Verificar se o formulário está visível e utilizável
            form = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "form"))
            )
            
            # Verificar se o campo de sintomas está visível
            textarea = self.driver.find_element(By.ID, "symptoms")
            self.assertTrue(textarea.is_displayed())
            
            # Verificar se o botão de envio está visível
            button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            self.assertTrue(button.is_displayed())
            
            logger.info("Teste de responsividade em tablet concluído com sucesso")
        except TimeoutException:
            self.fail("Timeout ao carregar elementos em visualização de tablet")
    
    def test_user_management(self):
        """Teste de gerenciamento de usuários"""
        # Primeiro fazer login como admin
        self.driver.get(f"{self.BASE_URL}/admin")
        
        try:
            # Login
            username_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "username"))
            )
            password_input = self.driver.find_element(By.ID, "password")
            
            username_input.send_keys("admin")
            password_input.send_keys("admin")
            
            button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            button.click()
            
            # Aguardar redirecionamento para o dashboard
            WebDriverWait(self.driver, 10).until(
                EC.url_contains("/admin/dashboard")
            )
            
            # Navegar para a página de usuários
            self.driver.get(f"{self.BASE_URL}/admin/users")
            
            # Verificar se a lista de usuários está presente
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "table"))
            )
            
            # Clicar no botão de novo usuário
            new_user_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Novo Usuário')]")
            new_user_button.click()
            
            # Aguardar redirecionamento para a página de cadastro
            WebDriverWait(self.driver, 10).until(
                EC.url_contains("/admin/users/new")
            )
            
            # Preencher formulário de cadastro
            name_input = self.driver.find_element(By.ID, "name")
            username_input = self.driver.find_element(By.ID, "username")
            password_input = self.driver.find_element(By.ID, "password")
            confirm_password_input = self.driver.find_element(By.ID, "confirmPassword")
            email_input = self.driver.find_element(By.ID, "email")
            
            timestamp = int(time.time())
            name_input.send_keys("Usuário de Teste Selenium")
            username_input.send_keys(f"teste_selenium_{timestamp}")
            password_input.send_keys("senha123")
            confirm_password_input.send_keys("senha123")
            email_input.send_keys(f"teste_selenium_{timestamp}@example.com")
            
            # Enviar formulário
            submit_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Cadastrar Usuário')]")
            submit_button.click()
            
            # Aguardar mensagem de sucesso
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "alert-success"))
            )
            
            logger.info("Teste de gerenciamento de usuários concluído com sucesso")
        except TimeoutException:
            self.fail("Timeout ao testar gerenciamento de usuários")

if __name__ == "__main__":
    unittest.main()
