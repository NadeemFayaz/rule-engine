document.getElementById("ruleForm").addEventListener("submit", function(event) {
    event.preventDefault();
    
    const rule = document.getElementById("ruleInput").value.trim();
    
    if (!rule) {
        alert("Rule cannot be empty!");
        return;
    }

    fetch('http://localhost:5000/create_rule', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ rule_string: rule }),  // Ensure the body is correct
    })
    
    .then(response => {
        if (!response.ok) {
            throw new Error("Error creating rule: " + response.statusText);
        }
        return response.json();
    })
    .then(data => {
        document.getElementById("ruleOutput").innerText = JSON.stringify(data, null, 2);
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById("ruleOutput").innerText = "Error creating rule: " + error.message;
    });
});


document.getElementById("combineForm").addEventListener("submit", function(event) {
    event.preventDefault();
    
    const rules = document.getElementById("rulesInput").value.split(',');
    
    fetch('http://localhost:5000/combine_rules', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ rule_strings: rules.map(rule => rule.trim()) }),  // Ensure rules are trimmed and sent correctly
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("combineOutput").innerText = JSON.stringify(data, null, 2);
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById("combineOutput").innerText = "Error combining rules.";
    });
});

document.getElementById("evaluateForm").addEventListener("submit", function(event) {
    event.preventDefault();
    
    const ruleId = document.getElementById("ruleIdInput").value;
    const userData = JSON.parse(document.getElementById("userDataInput").value);
    
    fetch('http://localhost:5000/evaluate_rule', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ rule_id: ruleId, user_data: userData }),
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("evaluateOutput").innerText = JSON.stringify(data, null, 2);
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById("evaluateOutput").innerText = "Error evaluating rule.";
    });
});
