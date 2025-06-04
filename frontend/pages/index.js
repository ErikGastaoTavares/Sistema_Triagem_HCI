import React from 'react';
import Head from 'next/head';
import { useState } from 'react';
import axios from 'axios';
import Header from '../components/Header';
import Footer from '../components/Footer';
import Card from '../components/Card';
import Button from '../components/Button';
import FormGroup from '../components/FormGroup';

// Função para renderizar a análise clínica em formato de pontos destacados
const renderAnaliseClinica = (analise) => {
  if (!analise) return null;
  
  // Remover os pontos/marcadores do início de cada linha
  const cleanAnalise = analise
    .replace(/^\s*•\s*/gm, '')  // Remove marcadores • do início das linhas
    .replace(/^\s*\*\s*/gm, '')  // Remove marcadores * do início das linhas
    .replace(/^\s*\.\s*/gm, '')  // Remove pontos do início das linhas
    .replace(/^\s*-\s*/gm, '');  // Remove traços do início das linhas
  
  // Dividir por linhas ou por pontos
  let topicos = [];
  
  if (cleanAnalise.includes('\n')) {
    // Dividir por quebras de linha
    topicos = cleanAnalise.split('\n').filter(t => t.trim());
  } else {
    // Dividir por pontos se não houver quebras de linha
    topicos = cleanAnalise.split(/\s+•\s+|\.\s+(?=[A-Z])/).filter(t => t.trim());
  }
  
  return (
    <div className="analise-clinica-container">
      {topicos.map((topico, index) => (
        <div key={index} className="analise-item">
          <div className="analise-bullet">•</div>
          <div className="analise-text">{topico}</div>
        </div>
      ))}
    </div>
  );
};

// Função para renderizar as condutas recomendadas em formato de pontos destacados
const renderCondutasRecomendadas = (condutas) => {
  if (!condutas) return null;
  
  // Remover os números e pontos do início de cada linha
  const cleanCondutas = condutas
    .replace(/^\s*\d+\.\s*/gm, '')  // Remove números seguidos de ponto no início das linhas
    .replace(/^\s*\d+\s*/gm, '')     // Remove números no início das linhas
    .replace(/^\s*\.\s*/gm, '');     // Remove pontos do início das linhas
  
  // Dividir por linhas ou por pontos
  let topicos = [];
  
  if (cleanCondutas.includes('\n')) {
    // Dividir por quebras de linha
    topicos = cleanCondutas.split('\n').filter(t => t.trim());
  } else {
    // Dividir por pontos se não houver quebras de linha
    topicos = cleanCondutas.split(/\s+\d+\.\s+|\.\s+(?=[A-Z])/).filter(t => t.trim());
  }
  
  return (
    <div className="condutas-container">
      {topicos.map((topico, index) => (
        <div key={index} className="conduta-item-card">
          <div className="conduta-numero">{index + 1}</div>
          <div className="conduta-text">{topico}</div>
        </div>
      ))}
    </div>
  );
};

export default function Home() {
  const [symptoms, setSymptoms] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');
  const [validationSent, setValidationSent] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!symptoms.trim()) {
      setError('Por favor, insira os sintomas do paciente.');
      return;
    }
    
    setLoading(true);
    setError('');
    
    try {
      // Usar diretamente o endpoint de triagem
      const response = await axios.post('http://localhost:8000/api/triagem', {
        sintomas: symptoms
      });
      
      setResult(response.data);
      setValidationSent(true); // Já está salvo no banco
    } catch (err) {
      console.error('Error processing triage:', err);
      if (err.response && err.response.status === 503) {
        setError('O serviço Ollama não está disponível. Por favor, verifique se o Ollama está instalado e em execução.');
      } else {
        setError('Erro ao processar a triagem. Por favor, tente novamente.');
      }
    } finally {
      setLoading(false);
    }
  };

  const getClassificationColor = (classification) => {
    const classLower = classification.toLowerCase();
    if (classLower === 'vermelho') return 'classification-red';
    if (classLower === 'laranja') return 'classification-orange';
    if (classLower === 'amarelo') return 'classification-yellow';
    if (classLower === 'verde') return 'classification-green';
    if (classLower === 'azul') return 'classification-blue';
    return '';
  };

  const getClassificationEmoji = (classification) => {
    const classLower = classification.toLowerCase();
    if (classLower === 'vermelho') return '🔴';
    if (classLower === 'laranja') return '🟠';
    if (classLower === 'amarelo') return '🟡';
    if (classLower === 'verde') return '🟢';
    if (classLower === 'azul') return '🔵';
    return '';
  };

  const getClassificationText = (classification) => {
    const classLower = classification.toLowerCase();
    if (classLower === 'vermelho') return 'EMERGÊNCIA (VERMELHO)';
    if (classLower === 'laranja') return 'MUITO URGENTE (LARANJA)';
    if (classLower === 'amarelo') return 'URGENTE (AMARELO)';
    if (classLower === 'verde') return 'POUCO URGENTE (VERDE)';
    if (classLower === 'azul') return 'NÃO URGENTE (AZUL)';
    return classification.toUpperCase();
  };

  return (
    <div className="bg-light min-h-screen">
      <Head>
        <title>Sistema de Triagem - HCI</title>
        <meta name="description" content="Sistema de Triagem baseado no Protocolo de Manchester - Hospital de Clínicas Ijuí" />
        <link rel="icon" type="image/png" href="/images/favicon.png" />
      </Head>

      <div className="container">
        <Header />

        <main>
          <div className="header-gradient rounded-lg p-4 text-center mb-4">
            <h1>Sistema de Triagem Clínica</h1>
            <p className="text-white">Baseado no Protocolo de Manchester</p>
          </div>

          <Card title="Nova Triagem">
            <form onSubmit={handleSubmit}>
              <FormGroup 
                label="Descreva os sintomas do paciente"
                htmlFor="symptoms"
                error={error}
              >
                <textarea
                  id="symptoms"
                  className="form-textarea"
                  value={symptoms}
                  onChange={(e) => setSymptoms(e.target.value)}
                  placeholder="Exemplo: Paciente masculino apresenta febre alta, tosse seca e dificuldade para respirar."
                  rows={5}
                />
              </FormGroup>
              
              <Button 
                type="submit" 
                disabled={loading}
                className="mt-3"
              >
                {loading ? 'Classificando...' : 'Classificar e gerar conduta'}
              </Button>
            </form>
          </Card>

          {result && (
            <Card title="Resultado da Triagem" className="fade-in">
              <div className={`classification ${getClassificationColor(result.classificacao)}`}>
                <h3>
                  {getClassificationEmoji(result.classificacao)} Classificação: {getClassificationText(result.classificacao)}
                </h3>
              </div>
              
              <div className="resultado-section">
                <h3 className="resultado-title">Análise Clínica</h3>
                {renderAnaliseClinica(result.justificativa)}
              </div>

              <div className="resultado-section">
                <h3 className="resultado-title">Condutas Recomendadas</h3>
                {renderCondutasRecomendadas(result.condutas)}
              </div>
              
              <div className="resultado-success">
                <div className="resultado-success-icon">✅</div>
                <div className="resultado-success-content">
                  <p className="resultado-success-title">Triagem enviada para validação com sucesso!</p>
                  <p className="resultado-success-id">ID de Rastreamento: {result.id}</p>
                  <p className="resultado-success-message">A triagem será revisada por especialistas clínicos para garantir a precisão da classificação e das condutas sugeridas.</p>
                </div>
              </div>
            </Card>
          )}
        </main>

        <Footer />
      </div>
    </div>
  );
}
