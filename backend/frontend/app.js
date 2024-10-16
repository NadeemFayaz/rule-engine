import React, { useState } from 'react';

function App() {
    const [age, setAge] = useState('');
    const [income, setIncome] = useState('');

    const handleSubmit = async () => {
        const response = await fetch('http://localhost:5000/evaluate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ age, income }),
        });

        const data = await response.json();
        alert(`Eligibility: ${data.eligibility}`);
    };

    return (
        <div>
            <h1>User Eligibility</h1>
            <label>
                Age: <input type="number" value={age} onChange={e => setAge(e.target.value)} />
            </label>
            <br />
            <label>
                Income: <input type="number" value={income} onChange={e => setIncome(e.target.value)} />
            </label>
            <br />
            <button onClick={handleSubmit}>Check Eligibility</button>
        </div>
    );
}

export default App;
