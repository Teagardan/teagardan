// masterplan/agent-system/src/orgChart.js
import React, { useState, useEffect } from 'react';
import AgentList from './agentList';
import Thread from './thread';
import TaskInput from './taskInput';
import AgentDetails from './agentDetails';
import agentSystem from './agentSystem';

const OrgChart = () => {
  const [agents, setAgents] = useState([]);
  const [selectedAgent, setSelectedAgent] = useState(null);
  const [messages, setMessages] = useState([]);
  const [showAgentDetails, setShowAgentDetails] = useState(false);

  useEffect(() => {
    const fetchAgents = async () => {
      try {
        const response = await agentSystem.loadAgents();
        setAgents(response);
      } catch (error) {
        console.error("Error fetching agents:", error);
      }
    };
    fetchAgents();
  }, []);

  // Remove unnecessary functions - they are handled by the API now.
  const handleTerminateAgent = async (agentId) => {
    try {
        const response = await axios.delete(`http://localhost:5001/agents/${agentId}`); //Call DELETE endpoint
        if (response.status === 200) {
            // Update UI state after successful deletion
            const updatedAgents = agents.filter((agent) => agent.id !== agentId);
            setAgents(updatedAgents);
        } else {
            console.error('Failed to terminate agent:', response.data);
            alert('Failed to terminate agent. Check console for details.');
        }
    } catch (error) {
        console.error('Error terminating agent:', error);
        alert('Error terminating agent. Check console for details.');
    }
};

  const handleAgentSelect = (agent) => {
    setSelectedAgent(agent);
    setShowAgentDetails(true);
  };

  const handleCloseAgentDetails = () => {
    setShowAgentDetails(false);
  };

  return (
    <div>
      <div id="agent-list-container">
        <AgentList agents={agents} selectAgent={handleAgentSelect} />
      </div>
      <div id="thread-container">
        {selectedAgent && <Thread agent={selectedAgent} messages={messages} />}
      </div>
      <div id="task-input-container">
        <TaskInput />
      </div>
      {showAgentDetails && <AgentDetails agent={selectedAgent} onClose={handleCloseAgentDetails} />}
    </div>
  );
};

export default OrgChart;