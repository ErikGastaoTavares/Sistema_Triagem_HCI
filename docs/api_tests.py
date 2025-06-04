import unittest
import requests
import json
import time
import logging

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("api_tests.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("api_tests")

class TriagemAPITests(unittest.TestCase):
    """Testes automatizados para a API do Sistema de Triagem"""
    
    BASE_URL = "http://localhost:8000"
    
    def setUp(self):
        """Configuração inicial para cada teste"""
        # Verificar se a API está online
        try:
            response = requests.get(f"{self.BASE_URL}/api/status")
            if response.status_code != 200:
                self.skipTest("API não está disponível")
            
            # Verificar se o Ollama está disponível
            status_data = response.json()
            if not status_data.get("ollama_available", False):
                self.skipTest("Serviço Ollama não está disponível")
                
        except Exception as e:
            self.skipTest(f"Erro ao verificar disponibilidade da API: {str(e)}")
    
    def test_api_root(self):
        """Teste do endpoint raiz da API"""
        response = requests.get(f"{self.BASE_URL}/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("message", data)
        logger.info("Teste do endpoint raiz concluído com sucesso")
    
    def test_triagem_endpoint(self):
        """Teste do endpoint de triagem"""
        payload = {
            "sintomas": "Paciente masculino, 45 anos, apresenta dor torácica intensa há 30 minutos, irradiando para o braço esquerdo, sudorese e náuseas."
        }
        
        response = requests.post(f"{self.BASE_URL}/api/triagem", json=payload)
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertIn("id", data)
        self.assertIn("classificacao", data)
        self.assertIn("justificativa", data)
        self.assertIn("condutas", data)
        
        # Verificar se a classificação é válida
        valid_classifications = ["VERMELHO", "LARANJA", "AMARELO", "VERDE", "AZUL"]
        self.assertIn(data["classificacao"], valid_classifications)
        
        logger.info(f"Teste de triagem concluído com sucesso: classificação={data['classificacao']}")
    
    def test_triagem_empty_symptoms(self):
        """Teste do endpoint de triagem com sintomas vazios"""
        payload = {
            "sintomas": ""
        }
        
        response = requests.post(f"{self.BASE_URL}/api/triagem", json=payload)
        self.assertEqual(response.status_code, 400)
        logger.info("Teste de triagem com sintomas vazios concluído com sucesso")
    
    def test_login_valid(self):
        """Teste de login com credenciais válidas"""
        payload = {
            "username": "admin",
            "password": "admin"
        }
        
        response = requests.post(f"{self.BASE_URL}/api/login", json=payload)
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertTrue(data["success"])
        self.assertEqual(data["user"], "admin")
        logger.info("Teste de login válido concluído com sucesso")
    
    def test_login_invalid(self):
        """Teste de login com credenciais inválidas"""
        payload = {
            "username": "usuario_inexistente",
            "password": "senha_incorreta"
        }
        
        response = requests.post(f"{self.BASE_URL}/api/login", json=payload)
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertFalse(data["success"])
        logger.info("Teste de login inválido concluído com sucesso")
    
    def test_estatisticas(self):
        """Teste do endpoint de estatísticas"""
        response = requests.get(f"{self.BASE_URL}/api/estatisticas")
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertIn("total", data)
        self.assertIn("validadas", data)
        self.assertIn("pendentes", data)
        logger.info("Teste de estatísticas concluído com sucesso")
    
    def test_listar_triagens(self):
        """Teste do endpoint de listagem de triagens"""
        response = requests.get(f"{self.BASE_URL}/api/triagens")
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertIn("triagens", data)
        self.assertIsInstance(data["triagens"], list)
        logger.info(f"Teste de listagem de triagens concluído com sucesso: {len(data['triagens'])} triagens")
    
    def test_usuarios_endpoint(self):
        """Teste do endpoint de usuários"""
        # Primeiro fazer login como admin para obter credenciais
        login_payload = {
            "username": "admin",
            "password": "admin"
        }
        
        login_response = requests.post(f"{self.BASE_URL}/api/login", json=login_payload)
        self.assertEqual(login_response.status_code, 200)
        
        # Testar listagem de usuários
        response = requests.get(f"{self.BASE_URL}/api/usuarios")
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertIn("usuarios", data)
        self.assertIsInstance(data["usuarios"], list)
        logger.info(f"Teste de listagem de usuários concluído com sucesso: {len(data['usuarios'])} usuários")
        
        # Testar criação de usuário
        user_payload = {
            "nome": "Usuário de Teste",
            "username": f"teste_{int(time.time())}",  # Garantir username único
            "password": "senha123",
            "email": f"teste_{int(time.time())}@example.com",  # Garantir email único
            "role": "enfermeiro"
        }
        
        response = requests.post(f"{self.BASE_URL}/api/usuarios", json=user_payload)
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertTrue(data["success"])
        self.assertIn("id", data)
        
        # Guardar ID para testes subsequentes
        user_id = data["id"]
        logger.info(f"Teste de criação de usuário concluído com sucesso: id={user_id}")
        
        # Testar obtenção de usuário específico
        response = requests.get(f"{self.BASE_URL}/api/usuarios/{user_id}")
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertTrue(data["success"])
        self.assertEqual(data["usuario"]["nome"], user_payload["nome"])
        logger.info("Teste de obtenção de usuário específico concluído com sucesso")
        
        # Testar atualização de usuário
        update_payload = {
            "nome": "Usuário de Teste Atualizado",
            "email": f"teste_atualizado_{int(time.time())}@example.com"
        }
        
        response = requests.put(f"{self.BASE_URL}/api/usuarios/{user_id}", json=update_payload)
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertTrue(data["success"])
        logger.info("Teste de atualização de usuário concluído com sucesso")
        
        # Testar exclusão de usuário
        response = requests.delete(f"{self.BASE_URL}/api/usuarios/{user_id}")
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertTrue(data["success"])
        logger.info("Teste de exclusão de usuário concluído com sucesso")

if __name__ == "__main__":
    unittest.main()
