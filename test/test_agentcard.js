// agentCard.test.js
import React from 'react';
import { render, screen } from '@testing-library/react';
import AgentCard from './agentCard'; 
import '@testing-library/jest-dom/extend-expect'; // For custom matchers

test('renders agent card correctly', () => {
  const agent = {
    id: 1,
    name: 'Agent A',
    type: 'Analyst',
    skills: ['Web Search', 'Text Summarization'],
    currentTask: 'Analyze Knowledge Graphs' 
  };

  render(<AgentCard agent={agent} />);

  expect(screen.getByText('Agent A')).toBeInTheDocument(); 
  expect(screen.getByText('Analyst')).toBeInTheDocument(); 
  expect(screen.getByText('Web Search')).toBeInTheDocument(); 
  expect(screen.getByText('Analyze Knowledge Graphs')).toBeInTheDocument(); 
});