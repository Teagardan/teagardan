// masterplan/agent-system/src/AgentDetails.js
import React from 'react';

const AgentDetails = ({ agent, onClose }) => {
  return (
    <div className="agent-details-panel">
      <h2>Agent Details</h2>
      <button onClick={onClose}>Close</button>
      <div>Name: {agent.name}</div>
      <div>Description: {agent.description}</div>
      <div>Skills: {agent.skills.join(', ')}</div>
    </div>
  );
};

export default AgentDetails;