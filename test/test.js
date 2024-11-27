import React from 'react';
import { render, screen } from '@testing-library/react'; 
import AgentCard from './agentCard';
import '@testing-library/jest-dom';

test('renders agent card correctly', () => {
  const agent = {
    id: 1,
    name: 'Agent A',
    type: 'Analyst',
    skills: ['Web Search', 'Text Summarization'],
    currentTask: 'Analyze Knowledge Graphs'
  };

  render(<AgentCard agent={agent} />);

  // Check for agent name
  expect(screen.getByText('Agent A')).toBeInTheDocument();

  // Check for agent type (Analyst)
  expect(screen.getByText(/Analyst/)).toBeInTheDocument();

  // Check for skills (Web Search, Text Summarization)
  expect(screen.getByText(/Web Search/)).toBeInTheDocument();
  expect(screen.getByText(/Text Summarization/)).toBeInTheDocument();

  // Use a regex for a more flexible match on the current task
  expect(screen.getByText(/Analyze Knowledge Graphs/i)).toBeInTheDocument();
});
