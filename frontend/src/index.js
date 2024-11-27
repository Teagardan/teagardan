import React from 'react';
import ReactDOM from 'react-dom/client';
import { Provider } from 'react-redux'; // If using Redux
import { BrowserRouter } from 'react-router-dom'; // If using routing
import App from './App'; // Or your top-level component (e.g., TeagardanApp.js)
import store from './store'; // Your Redux store (if applicable)
import './styles/index.css'; // Import global styles
import reportWebVitals from './reportWebVitals'; //For performance tracking


const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <BrowserRouter> {/* For routing */}
      <Provider store={store}> {/* If using Redux */}
        <App /> 
      </Provider>
    </BrowserRouter>
  </React.StrictMode>
);


reportWebVitals(); //For performance measurements, remove for production.