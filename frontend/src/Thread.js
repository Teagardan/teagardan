// masterplan/agent-system/src/Thread.js
import React from 'react';

const Thread = ({ agent, messages }) => {
  return (
    <div>
      <h2>Thread with {agent.name}</h2>
      <ul>
        {messages.map((message, index) => (
          <li key={index}>{message}</li> //Simplified - no timestamp for now
        ))}
      </ul>
      {/* Add message input and submission here later */}
    </div>
  );
};

export default Thread;