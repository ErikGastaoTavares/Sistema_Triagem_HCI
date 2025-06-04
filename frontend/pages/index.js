import React from 'react';
import Head from 'next/head';
import { useState } from 'react';
import axios from 'axios';
import Header from '../components/Header';
import Footer from '../components/Footer';
import Card from '../components/Card';
import Button from '../components/Button';
import FormGroup from '../components/FormGroup';

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
              
              <div className="section">
                <h3 className="section-title">Análise Clínica</h3>
                <p>{result.justificativa}</p>
              </div>
              
              <div className="section">
                <h3 className="section-title">Condutas Recomendadas</h3>
                <p>{result.condutas}</p>
              </div>
              
              <Card type="success" className="mt-3">
                <p>✅ Triagem enviada para validação com sucesso!</p>
                <p>🔍 ID de Rastreamento: {result.id}</p>
                <p>👨‍⚕️ A triagem será revisada por especialistas clínicos para garantir a precisão da classificação e das condutas sugeridas.</p>
              </Card>
            </Card>
          )}
        </main>

        <Footer />
      </div>
    </div>
  );
}
