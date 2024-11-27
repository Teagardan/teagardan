// frontend/src/tests/App.test.js
import React from 'react';
import { render, screen } from '@testing-library/react';
import App from '../App'; // Make sure path is correct


test('renders Teagardan title', () => {
    render(<App />);
    const titleElement = screen.getByText(/Teagardan/i); //Or appropriate element in your app
    expect(titleElement).toBeInTheDocument();

});


// frontend/src/tests/components/AgentList.test.js (Example)
import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react'; // Import fireEvent for events
import { Provider } from 'react-redux'; //If using redux.
import { configureStore } from '@reduxjs/toolkit';
import agentReducer from '../../redux/agentSlice';
import AgentList from '../../components/AgentList';
import { BrowserRouter as Router } from 'react-router-dom'; // Or your router


const store = configureStore({
    reducer: {
        agents: agentReducer,
      },

  });

  //Mock agentService for your tests.  You don't want to make actual API calls when unit testing components.
  jest.mock('../../services/agentService', () => ({
    loadAgents: jest.fn(() => Promise.resolve([  //Example mock agents.
        { id: 1, name: 'Agent 1', skills: ['skill1'] },
        { id: 2, name: 'Agent 2', skills: ['skill2', 'skill3'] },

      ])),
      //Add any other functions as needed, for adding, updating, deleting, activating, etc.
  }));

test('renders agent list and handles terminate', async () => {  //Make this test async to handle Promises correctly.

  render(
      <Provider store={store}>
            <Router> <AgentList /></Router>
        </Provider>

    );  //Wrap component in providers if needed.



  //Check agents have been loaded.
  expect(await screen.findByText("Agent 1")).toBeInTheDocument();  // Use findBy* for asynchronous elements.
  expect(screen.getByText("Agent 2")).toBeInTheDocument(); // Use getByText if they've already been loaded.


  const terminateButton = screen.getAllByRole('button', { name: /Terminate/i })[0];
  fireEvent.click(terminateButton);

  //Assertions after termination
  // (e.g. check if the agent is removed, API is called.)
  // ... Add more assertions as needed.
});