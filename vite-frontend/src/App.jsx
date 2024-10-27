/** @jsxImportSource @emotion/react */
import React, { useState } from 'react';
import ComparativeSummary from './components/ComparativeSummary';
import ComparativeChart from './components/ComparativeChart';
import EarningsSummary from './components/EarningsSummary';
import styled from '@emotion/styled';
import ApiService from './services/apiService';  // Import the ApiService class

const Container = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
  background-color: #f5f5f5;
  height: 100vh;
  font-family: Arial, sans-serif;
`;

const Title = styled.h1`
  color: #333;
  font-size: 2.5em;
  margin-bottom: 20px;
`;

const Input = styled.input`
  padding: 10px;
  font-size: 1.2em;
  border-radius: 8px;
  border: 2px solid #ddd;
  width: 300px;
  margin-bottom: 20px;
  &:focus {
    outline: none;
    border-color: #0070f3;
  }
`;

const Button = styled.button`
  padding: 12px 20px;
  font-size: 1.2em;
  color: #fff;
  background-color: #0070f3;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s;
  &:hover {
    background-color: #005bb5;
  }
`;

const App = () => {
  const [companyList, setCompanyList] = useState('');
  const [year, setYear] = useState('');
  const [comparativeReport, setComparativeReport] = useState({});
  const [singleSummary, setSingleSummary] = useState('');  // State for single company summary

  const handleCompareSummary = async () => {
    const companies = companyList.split(',').map(company => company.trim());
    try {
      const report = await ApiService.compareEarnings(companies, parseInt(year, 10));
      setComparativeReport(report);
    } catch (error) {
      console.error('Error fetching comparative report:', error);
    }
  };

  const handleSingleSummary = async () => {
    try {
      const summary = await ApiService.summarizeEarnings(companyList.trim(), parseInt(year, 10));
      setSingleSummary(summary);
    } catch (error) {
      console.error('Error fetching single company summary:', error);
    }
  };

  return (
    <Container>
      <Title>Earnings Call Summary Tool</Title>
      <Input
        type="text"
        value={companyList}
        onChange={(e) => setCompanyList(e.target.value)}
        placeholder="Enter comma-separated company tickers"
      />
      <Input
        type="text"
        value={year}
        onChange={(e) => setYear(e.target.value)}
        placeholder="Enter year (e.g., 2024)"
      />
      
      <Button onClick={handleSingleSummary}>Get Single Company Summary</Button>
      {singleSummary && <EarningsSummary summary={singleSummary} />}
      
      <Button onClick={handleCompareSummary} style={{ marginTop: '20px' }}>
        Get Comparative Report
      </Button>
      {Object.keys(comparativeReport).length > 0 && (
        <>
          <ComparativeSummary report={comparativeReport} />
          <ComparativeChart report={comparativeReport} />
        </>
      )}
    </Container>
  );
};

export default App;
