import React from 'react';
import '../css/app.css';


const handleSubmit = (event) => {
  event.preventDefault();
  const data = new FormData(event.target);
  fetch('/store/', {
    method: 'POST',
    headers: {'username': 'abc1'}
  });
}

const App = () => {
  var s = "hello"
  console.log(context.int2k)
  return (
    <form onSubmit={handleSubmit}>
      <label>
        Name:
        <input type="text" value={"hello"} />
      </label>
      <input type="submit" value="Submit"/>
    </form>
  );
}

export default App;
