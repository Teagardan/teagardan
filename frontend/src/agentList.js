// masterplan/agent-system/src/agentList.js
import React, { useState } from 'react';
import axios from 'axios'; //Import axios


const AgentList = ({ agents, selectAgent, terminateAgent }) => { // Add terminateAgent prop
  const [newAgent, setNewAgent] = useState({ name: '', description: '', skills: [] });

  const handleInputChange = (e) => {
    setNewAgent({ ...newAgent, [e.target.name]: e.target.value });
  };

  const handleAddSkill = () => {
    setNewAgent({...newAgent, skills: [...newAgent.skills, ""]});
  };

  const handleSkillChange = (e, index) => {
    const newSkills = [...newAgent.skills];
    newSkills[index] = e.target.value;
    setNewAgent({ ...newAgent, skills: newSkills });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://localhost:5001/agents', newAgent); // Use correct port
      if (response.status === 201) {
        //Refetch the agent list after successful addition
        const updatedAgents = await agentSystem.loadAgents();
        setAgents(updatedAgents);
      } else {
        console.error("Error adding agent:", response.data);
        alert("Error adding agent. See console for details.");
      }
    } catch (error) {
      console.error("Error adding agent:", error);
      alert("Error adding agent. See console for details.");
    }
    setNewAgent({ name: '', description: '', skills: [] });
  };

  return (
    <div>
      <ul>
        {agents.map((agent) => (
          <li key={agent.id}>
            {agent.name} ({agent.type || 'N/A'}) {/* Handle missing type */}
            <span className="agent-status">{agent.status || 'Idle'}</span> {/* Handle missing status */}
            <button onClick={() => terminateAgent(agent.id)}>Terminate</button> {/* Add Terminate button */}
          </li>
        ))}
      </ul>
      <form onSubmit={handleSubmit}>
        <label>
          Name:
          <input type="text" name="name" value={newAgent.name} onChange={handleInputChange} required />
        </label>
        <br />
        <label>
          Description:
          <input type="text" name="description" value={newAgent.description} onChange={handleInputChange} />
        </label>
        <br />
        <label>Skills:</label>
        <br />
        {newAgent.skills.map((skill, index) => (
          <div key={index}>
            <input type="text" name={`skills-${index}`} value={skill} onChange={(e) => handleSkillChange(e, index)} />
          </div>
        ))}
        <button onClick={handleAddSkill}>Add Skill</button>
        <br />
        <button type="submit">Add Agent</button>
      </form>
    </div>
  );
};

export default AgentList;