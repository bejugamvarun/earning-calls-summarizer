/** @jsxImportSource @emotion/react */
import React from 'react';
import styled from '@emotion/styled';

const SummaryContainer = styled.div`
  width: 80%;
  margin: 20px auto;
  background-color: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  padding: 20px;
  text-align: left;
`;

const SummaryTitle = styled.h2`
  color: #0070f3;
  font-size: 1.8em;
  margin-bottom: 20px;
`;

const SummaryText = styled.p`
  color: #333;
  font-size: 1.2em;
`;

const EarningsSummary = ({ summary }) => {
  return (
    <SummaryContainer>
      <SummaryTitle>Summary</SummaryTitle>
      <SummaryText>{summary}</SummaryText>
    </SummaryContainer>
  );
};

export default EarningsSummary;
