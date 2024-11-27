// Import the SQLite library
const sqlite3 = require('sqlite3'); 
// Or if you're using 'better-sqlite3':
// const sqlite = require('better-sqlite3');

// Function to load agent data from the database
function loadAgents(callback) {
  const db = new sqlite3.Database('agentData.db'); // Connect to the database
  db.all('SELECT * FROM agents', (err, rows) => { // Load agents
    if (err) {
      console.error('Error loading agents:', err);
      callback([]); // Return an empty array on error 
    } else {
      callback(rows);
    }
    db.close();
  });
}

// Function to update an agent's status in the database 
function updateAgentStatus(agentId, newStatus) {
  const db = new sqlite3.Database('agentData.db');
  db.run('UPDATE agents SET status = ? WHERE id = ?', 
        [newStatus, agentId], (err) => {
    if (err) {
      console.error('Error updating agent status:', err);
    }
    db.close();
  });
}

// Function to save agent data to the database
function saveAgents(agents) {
  const db = new sqlite3.Database('agentData.db');
  db.run('DELETE FROM agents'); // Clear existing agents
  agents.forEach((agent) => {
    db.run('INSERT INTO agents (name, type, skills) VALUES (?, ?, ?)', 
            [agent.name, agent.type, agent.skills]);
  });
  db.close();
}

// Function to load conversation history
function loadConversations(agentId, callback) {
  const db = new sqlite3.Database('agentData.db');
  db.all('SELECT * FROM conversations WHERE agentId = ?', 
          [agentId], (err, rows) => {
    if (err) {
      console.error('Error loading conversations:', err);
      callback([]);
    } else {
      callback(rows);
    }
    db.close();
  });
}

// Function to save a new conversation message
function saveConversationMessage(agentId, message) {
  const db = new sqlite3.Database('agentData.db');
  db.run('INSERT INTO conversations (agentId, message) VALUES (?, ?)', 
          [agentId, message]);
  db.close();
}

// Function to update a task's status in the database
function updateTaskStatus(agentId, taskIndex, newStatus) {
  const db = new sqlite3.Database('agentData.db');
  // Assume you have a 'tasks' table with columns: id, agentId, task, status
  db.run('UPDATE tasks SET status = ? WHERE agentId = ? AND id = ?', 
          [newStatus, agentId, taskIndex], (err) => {
    if (err) {
      console.error('Error updating task status:', err);
    }
    db.close();
  });
}

// Export the database interaction functions
module.exports = {
  loadAgents, 
  saveAgents, 
  loadConversations, 
  saveConversationMessage,
  updateAgentStatus,
  updateTaskStatus
};