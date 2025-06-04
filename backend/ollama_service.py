import requests
import json
import logging
import time
from typing import Dict, Any, Tuple, Optional

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ollama_service")
handler = logging.FileHandler("ollama_service.log")
handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)

class OllamaService:
    def __init__(self, url: str = "http://localhost:11434", model: str = "mistral", max_retries: int = 3 ):
        self.url = url
        self.model = model
        self.max_retries = max_retries
        logger.info(f"Serviço Ollama inicializado: modelo={model}, max_retries={max_retries}")

    async def generate_response(self, symptoms: str) -> str:
        """Gera uma resposta do modelo Ollama com base nos sintomas fornecidos."""
        prompt = self._create_prompt(symptoms)
        
        for attempt in range(1, self.max_retries + 1):
            try:
                logger.info(f"Enviando prompt para Ollama (tentativa {attempt}/{self.max_retries})")
                response = requests.post(
                    f"{self.url}/api/generate",
                    json={
                        "model": self.model,
                        "prompt": prompt,
                        "stream": False,
                        "options": {
                            "temperature": 0.2,
                            "top_p": 0.9
                        }
                    },
                    timeout=60
                )
                
                if response.status_code == 200:
                    result = response.json()
                    response_text = result.get("response", "")
                    logger.info(f"Resposta gerada com sucesso: {len(response_text)} caracteres")
                    return response_text
                else:
                    logger.error(f"Erro na API Ollama: {response.status_code} - {response.text}")
            except Exception as e:
                logger.error(f"Erro ao chamar API Ollama: {str(e)}")
            
            # Esperar antes de tentar novamente (backoff exponencial)
            if attempt < self.max_retries:
                wait_time = 2 ** attempt
                logger.info(f"Aguardando {wait_time}s antes da próxima tentativa...")
                time.sleep(wait_time)
        
        # Se todas as tentativas falharem, retornar uma resposta de fallback
        logger.error("Todas as tentativas de chamar a API Ollama falharam")
        return self._generate_fallback_response()

    def format_prompt(self, symptoms: str, similar_cases=None) -> str:
        """Cria um prompt estruturado para o modelo Ollama."""
        return f"""Você é um sistema especializado em triagem hospitalar baseado no Protocolo de Manchester.
        
    Sua tarefa é analisar os sintomas do paciente e fornecer:
    1. Uma classificação de urgência (VERMELHO, LARANJA, AMARELO, VERDE ou AZUL)
    2. Uma justificativa clínica detalhada para a classificação
    3. Condutas recomendadas específicas para o caso

    SINTOMAS DO PACIENTE:
    {symptoms}

    PROTOCOLO DE MANCHESTER:
    - VERMELHO (Emergência): Risco imediato à vida. Atendimento imediato.
    - LARANJA (Muito Urgente): Risco alto. Atendimento em até 10 minutos.
    - AMARELO (Urgente): Risco moderado. Atendimento em até 60 minutos.
    - VERDE (Pouco Urgente): Risco baixo. Atendimento em até 120 minutos.
    - AZUL (Não Urgente): Sem risco. Atendimento em até 240 minutos.

    Forneça sua resposta no seguinte formato exato:

    CLASSIFICAÇÃO: [COR]

    ANÁLISE CLÍNICA:
    [Forneça uma análise detalhada dos sintomas, explicando por que eles se enquadram na classificação escolhida. Inclua possíveis diagnósticos diferenciais e fatores de risco. Mínimo de 3 parágrafos.]

    CONDUTAS RECOMENDADAS:
    [Liste pelo menos 5 condutas específicas recomendadas para este caso, incluindo exames, medicações e orientações. Seja específico e detalhado.]

    É ESSENCIAL que você forneça uma análise clínica detalhada e condutas específicas, não apenas a classificação.
    """

    def _create_prompt(self, symptoms: str, similar_cases=None) -> str:
        """Alias para format_prompt para manter compatibilidade."""
        return self.format_prompt(symptoms, similar_cases)

    def _generate_fallback_response(self) -> str:
        """Gera uma resposta de fallback quando a API Ollama falha."""
        return """CLASSIFICAÇÃO: AMARELO

ANÁLISE CLÍNICA:
Não foi possível realizar uma análise detalhada devido a problemas técnicos. Por precaução, o paciente recebeu classificação AMARELO (Urgente).

CONDUTAS RECOMENDADAS:
1. Avaliação médica em até 60 minutos
2. Monitoramento de sinais vitais
3. Reavaliação da classificação por profissional de saúde
4. Documentação do caso como incidente técnico
5. Verificação manual dos sintomas relatados"""

    def parse_response(self, response: str) -> tuple:
        """Analisa a resposta do modelo para extrair classificação, justificativa e condutas."""
        try:
            # Extrair classificação
            classification = ""
            if "CLASSIFICAÇÃO:" in response:
                classification_line = response.split("CLASSIFICAÇÃO:")[1].split("\n")[0].strip()
                if "VERMELHO" in classification_line:
                    classification = "VERMELHO"
                elif "LARANJA" in classification_line:
                    classification = "LARANJA"
                elif "AMARELO" in classification_line:
                    classification = "AMARELO"
                elif "VERDE" in classification_line:
                    classification = "VERDE"
                elif "AZUL" in classification_line:
                    classification = "AZUL"
            
            # Extrair justificativa
            justification = ""
            if "ANÁLISE CLÍNICA:" in response:
                parts = response.split("ANÁLISE CLÍNICA:")[1].split("CONDUTAS RECOMENDADAS:")
                if len(parts) > 0:
                    justification = parts[0].strip()
            
            # Extrair condutas
            recommendations = ""
            if "CONDUTAS RECOMENDADAS:" in response:
                recommendations = response.split("CONDUTAS RECOMENDADAS:")[1].strip()
            
            logger.info(f"Resposta processada: classificação={classification}, justificativa={len(justification)} caracteres, condutas={len(recommendations)} caracteres")
            return classification, justification, recommendations
        except Exception as e:
            logger.error(f"Erro ao processar resposta: {str(e)}")
            return "AMARELO", "", ""  # Fallback para classificação AMARELO em caso de erro
        
    def process_response(self, response: str) -> tuple:
        """Alias para parse_response para manter compatibilidade."""
        return self.parse_response(response)
