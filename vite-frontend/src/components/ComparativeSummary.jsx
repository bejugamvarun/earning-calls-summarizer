/** @jsxImportSource @emotion/react */
import React from 'react';
import styled from '@emotion/styled';

const SummaryContainer = styled.div`
  width: 80%;
  margin: 30px auto;
  display: flex;
  flex-direction: column;
  align-items: center;
  background-color: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  padding: 20px;
`;

const ReportItem = styled.div`
  margin-bottom: 20px;
  text-align: left;
  width: 100%;
`;

const CompanyTitle = styled.h3`
  color: #0070f3;
  font-size: 1.5em;
`;

const ReportText = styled.p`
  color: #333;
  font-size: 1.2em;
  margin-top: 10px;
`;

const ComparativeSummary = ({ report }) => {
  return (
    <SummaryContainer>
      <h2>Comparative Earnings Summary</h2>
      {Object.keys(report).map((company) => (
        <div key={company}>
          <CompanyTitle>{company}</CompanyTitle>
          {Object.keys(report[company]).map((quarter) => (
            <ReportItem key={quarter}>
              <h4>{quarter}</h4>
              <ReportText>{report[company][quarter]}</ReportText>
            </ReportItem>
          ))}
        </div>
      ))}
    </SummaryContainer>
  );
};

export default ComparativeSummary;
