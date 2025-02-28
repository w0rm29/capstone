import React from 'react';
import Form  from './components/Form';
import Submit from './components/Submit';
import ViewTasks from './components/ViewTasks';

function App() {
  return (
    <div>
      <h1>Welcome to Chronoplan</h1>
      {/* <Form/> */}
      <Submit/>
      <ViewTasks/>
    </div>
  );
}

export default App;
