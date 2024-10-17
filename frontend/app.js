// frontend/app.js
document.getElementById("ruleForm").addEventListener("submit", function(event) {
    event.preventDefault();
    
    const rule = document.getElementById("ruleInput").value;
    
    fetch('/create_rule', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ rule: rule }),
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("ruleOutput").innerText = JSON.stringify(data, null, 2);
    })
    .catch(error => {
        console.error('Error:', error);
    });
});
