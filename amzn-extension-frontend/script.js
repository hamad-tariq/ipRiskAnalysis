// document.getElementById('formLinkButton').addEventListener('click', function() {
//     document.getElementById('page1').style.display = 'none';
//     document.getElementById('page2').style.display = 'block';
// });

// document.getElementById('submitButton').addEventListener('click', function() {
//     const formLink = document.getElementById('formLinkInput').value;
//     const errorMessage = document.getElementById('errorMessage');
    
//     if (formLink.includes('responded') || formLink.includes('alreadyresponded')) {
//         document.getElementById('page2').style.display = 'none';
//         document.getElementById('loginPage').style.display = 'block';
//         errorMessage.style.display = 'none';
//     } else {
//         errorMessage.style.display = 'block';
//     }
// });

// document.getElementById('loginButton').addEventListener('click', function() {
//     const email = document.getElementById('email').value;
//     const password = document.getElementById('password').value;
//     const loginErrorMessage = document.getElementById('loginErrorMessage');

//     // Simulate API call for login validation
//     // const isValidLogin = (email === 'test@example.com' && password === 'password'); // Replace with actual API call
//     const isValidLogin = true;

//     if (isValidLogin) {
//         document.getElementById('loginPage').style.display = 'none';
//         document.getElementById('ipRiskPage').style.display = 'block';
//         loginErrorMessage.style.display = 'none';
//     } else {
//         loginErrorMessage.style.display = 'block';
//     }
// });

// document.getElementById('signUpLink').addEventListener('click', function() {
//     document.getElementById('loginPage').style.display = 'none';
//     document.getElementById('signUpPage').style.display = 'block';
// });

// document.getElementById('signUpButton').addEventListener('click', function() {
//     const email = document.getElementById('signUpEmail').value;
//     const password = document.getElementById('signUpPassword').value;
//     const signUpErrorMessage = document.getElementById('signUpErrorMessage');

//     // Simulate API call for sign-up validation
//     const isSignUpSuccessful = (email !== '' && password !== ''); // Replace with actual API call

//     if (isSignUpSuccessful) {
//         document.getElementById('signUpPage').style.display = 'none';
//         document.getElementById('loginPage').style.display = 'block';
//         signUpErrorMessage.style.display = 'none';
//     } else {
//         signUpErrorMessage.style.display = 'block';
//     }
// });

// document.getElementById('loginLink').addEventListener('click', function() {
//     document.getElementById('signUpPage').style.display = 'none';
//     document.getElementById('loginPage').style.display = 'block';
// });

// document.getElementById('logoutButton').addEventListener('click', function() {
//     // Simulate API call for logout
//     alert('Logged out successfully.');
//     document.getElementById('ipRiskPage').style.display = 'none';
// document.getElementById('loginPage').style.display = 'block';
// });

// document.getElementById('checkIpRiskButton').addEventListener('click', function() {
// const loader = document.getElementById('loader');
// const ipRiskResult = document.getElementById('ipRiskResult');
// const riskTable = document.getElementById('riskTable');
// const exportCsvButton = document.getElementById('exportCsvButton');
// loader.style.display = 'block';
// ipRiskResult.textContent = '';
// riskTable.style.display = 'none';
// exportCsvButton.style.display = 'none';

// // Simulate API call for IP risk checking
// setTimeout(() => {
//     loader.style.display = 'none';
//     const hasIpRisk = true; // Replace with actual API response

//     ipRiskResult.textContent = hasIpRisk ? 'Yes' : 'No';
//     riskTable.style.display = 'table';
//     exportCsvButton.style.display = 'inline-block';

//     // Populate table with API response
//     const riskData = [
//         { associated: 'Risk 1', severity: 'High', description: 'Description 1', graph: 'Graph 1' },
//         { associated: 'Risk 2', severity: 'Medium', description: 'Description 2', graph: 'Graph 2' },
//         // Add more data as needed
//     ];

//     const tbody = document.querySelector('#riskTable tbody');
//     tbody.innerHTML = '';

//     riskData.forEach(risk => {
//         const row = document.createElement('tr');
//         row.innerHTML = `
//             <td>${risk.associated}</td>
//             <td>${risk.severity}</td>
//             <td>${risk.description}</td>
//             <td>${risk.graph}</td>
//         `;
//         tbody.appendChild(row);
//     });
// }, 2000); // Simulate 2 seconds API response time
// });

// document.getElementById('exportCsvButton').addEventListener('click', function() {
// const rows = Array.from(document.querySelectorAll('#riskTable tr'));
// const csvContent = rows.map(row => {
// const cells = Array.from(row.querySelectorAll('th, td'));
// return cells.map(cell => cell.textContent).join(',');
// }).join('\n');
// const blob = new Blob([csvContent], { type: 'text/csv' });
// const url = URL.createObjectURL(blob);
// const a = document.createElement('a');
// a.href = url;
// a.download = 'ip_risk_data.csv';
// a.click();
// URL.revokeObjectURL(url);
// });




// -------------------------------------------------------------



// document.addEventListener('DOMContentLoaded', function () {
//     loadPage('page1.html');

//     document.addEventListener('click', function (e) {
//         if (e.target && e.target.id === 'formLinkButton') {
//             loadPage('page2.html');
//         } else if (e.target && e.target.id === 'submitButton') {
//             const formLinkInput = document.getElementById('formLinkInput').value;
//             if (formLinkInput.includes('responded') || formLinkInput.includes('alreadyresponded')) {
//                 loadPage('login.html');
//             } else {
//                 document.getElementById('errorMessage').style.display = 'block';
//             }
//         } else if (e.target && e.target.id === 'signUpLink') {
//             loadPage('signup.html');
//         } else if (e.target && e.target.id === 'loginLink') {
//             loadPage('login.html');
//         } else if (e.target && e.target.id === 'loginButton') {
//             // Handle login logic here
//             const email = document.getElementById('email').value;
//             const password = document.getElementById('password').value;
//             // Assume a local API call to validate the credentials
//             if (email === 'user@gmail.com' && password === 'user123') {
//                 loadPage('iprisk.html');
//             } else {
//                 document.getElementById('loginErrorMessage').style.display = 'block';
//             }
//         } else if (e.target && e.target.id === 'signUpButton') {
//             // Handle sign-up logic here
//             const email = document.getElementById('signUpEmail').value;
//             const password = document.getElementById('signUpPassword').value;
//             // Assume a local API call to create the account
//             if (email && password) {
//                 loadPage('login.html');
//             } else {
//                 document.getElementById('signUpErrorMessage').style.display = 'block';
//             }
//         } else if (e.target && e.target.id === 'checkIpRiskButton') {
//             const loader = document.getElementById('loader');
//             loader.style.display = 'flex';
//             // Simulate API call to fetch IP risk data
//             setTimeout(() => {
//                 loader.style.display = 'none';
//                 document.getElementById('ipRiskScore').textContent = 'Yes';
//                 const tableBody = document.querySelector('#riskTable tbody');
//                 tableBody.innerHTML = `
//                     <tr>
//                         <td>High Risk</td>
//                         <td>Severe</td>
//                         <td>Possible infringement</td>
//                         <td>[Graph]</td>
//                     </tr>
//                     <tr>
//                         <td>Low Risk</td>
//                         <td>Moderate</td>
//                         <td>Minor issues</td>
//                         <td>[Graph]</td>
//                     </tr>
//                 `;
//             }, 2000);
//         } else if (e.target && e.target.id === 'exportCsvButton') {
//             // Simulate exporting data to CSV
//             const data = [
//                 ['Risk Associated', 'Risk Severity', 'Risk Description', 'Graph Representation'],
//                 ['High Risk', 'Severe', 'Possible infringement', '[Graph]'],
//                 ['Low Risk', 'Moderate', 'Minor issues', '[Graph]']
//             ];
//             const csvContent = data.map(e => e.join(",")).join("\n");
//             const blob = new Blob([csvContent], { type: 'text/csv' });
//             const url = URL.createObjectURL(blob);
//             const a = document.createElement('a');
//             a.href = url;
//             a.download = 'ip_risk_data.csv';
//             a.click();
//             URL.revokeObjectURL(url);
//         } else if (e.target && e.target.id === 'logoutButton') {
//             // Handle logout logic here
//             loadPage('login.html');
//         }
//     });

//     function loadPage(page) {
//         fetch(`pages/${page}`)
//             .then(response => response.text())
//             .then(html => {
//                 document.getElementById('content').innerHTML = html;
//             })
//             .catch(error => {
//                 console.error('Error loading page:', error);
//             });
//     }
// });



// ----------- Backend Integrated Code -----------------------

// document.addEventListener('DOMContentLoaded', function () {
//     // Check if the user is already logged in
//     const userId = sessionStorage.getItem('user_id');
//     console.log(userId);
//     if (userId) {
//         // Call the already logged in API
//         fetch(`http://localhost:5000/already_loggedin/${userId}`, {
//             method: 'GET',
//             credentials: 'include',  // Include credentials with the request
//         })
//         .then(response => response.json())
//         .then(data => {
//             if (data.message === 'User is already logged in') {
//                 loadPage('iprisk.html');
//             } else {
//                 loadPage('page1.html');
//             }
//         })
//         .catch(error => {
//             console.error('Error:', error);
//             loadPage('page1.html');
//         });
//     } else {
//         loadPage('page1.html');
//     }

//     document.addEventListener('click', function (e) {
//         if (e.target && e.target.id === 'formLinkButton') {
//             loadPage('page2.html');
//         } else if (e.target && e.target.id === 'submitButton') {
//             const formLinkInput = document.getElementById('formLinkInput').value;
//             if (formLinkInput.includes('responded') || formLinkInput.includes('alreadyresponded')) {
//                 loadPage('login.html');
//             } else {
//                 document.getElementById('errorMessage').style.display = 'block';
//             }
//         } else if (e.target && e.target.id === 'signUpLink') {
//             loadPage('signup.html');
//         } else if (e.target && e.target.id === 'loginLink') {
//             loadPage('login.html');
//         } else if (e.target && e.target.id === 'loginButton') {
//             // Handle login logic here
//             const email = document.getElementById('email').value;
//             const password = document.getElementById('password').value;
//             // Call the login API
//             fetch('http://localhost:5000/login', {
//                 method: 'POST',
//                 headers: {
//                     'Content-Type': 'application/json',
//                 },
//                 credentials: 'include',  // Include credentials with the request
//                 body: JSON.stringify({ email, password }),
//             })
//             .then(response => response.json())
//             .then(data => {
//                 if (data.message === 'Login successful') {
//                     sessionStorage.setItem('user_id', data.user.id);
//                     loadPage('iprisk.html');
//                 } else {
//                     document.getElementById('loginErrorMessage').style.display = 'block';
//                 }
//             })
//             .catch(error => console.error('Error:', error));
//         } else if (e.target && e.target.id === 'signUpButton') {
//             // Handle sign-up logic here
//             const email = document.getElementById('signUpEmail').value;
//             const password = document.getElementById('signUpPassword').value;
//             // Call the signup API
//             fetch('http://localhost:5000/signup', {
//                 method: 'POST',
//                 headers: {
//                     'Content-Type': 'application/json',
//                 },
//                 credentials: 'include',  // Include credentials with the request
//                 body: JSON.stringify({ email, password }),
//             })
//             .then(response => {
//                 if (!response.ok) {
//                     throw new Error('Sign up failed. Please try again.');
//                 }
//                 return response.json();
//             })
//             .then(data => {
//                 if (data.message === 'Signup successful') {
//                     loadPage('login.html');
//                 } else {
//                     document.getElementById('signUpErrorMessage').style.display = 'block';
//                 }
//             })
//             .catch(error => {
//                 console.error('Error:', error);
//                 document.getElementById('signUpErrorMessage').style.display = 'block';
//             });
//         } else if (e.target && e.target.id === 'checkIpRiskButton') {
//             const loader = document.getElementById('loader');
//             loader.style.display = 'flex';
//             // Simulate API call to fetch IP risk data
//             setTimeout(() => {
//                 loader.style.display = 'none';
//                 document.getElementById('ipRiskScore').textContent = 'Yes';
//                 const tableBody = document.querySelector('#riskTable tbody');
//                 tableBody.innerHTML = `
//                     <tr>
//                         <td>High Risk</td>
//                         <td>Severe</td>
//                         <td>Possible infringement</td>
//                         <td>[Graph]</td>
//                     </tr>
//                     <tr>
//                         <td>Low Risk</td>
//                         <td>Moderate</td>
//                         <td>Minor issues</td>
//                         <td>[Graph]</td>
//                     </tr>
//                 `;
//             }, 2000);
//         } else if (e.target && e.target.id === 'exportCsvButton') {
//             // Simulate exporting data to CSV
//             const data = [
//                 ['Risk Associated', 'Risk Severity', 'Risk Description', 'Graph Representation'],
//                 ['High Risk', 'Severe', 'Possible infringement', '[Graph]'],
//                 ['Low Risk', 'Moderate', 'Minor issues', '[Graph]']
//             ];
//             const csvContent = data.map(e => e.join(",")).join("\n");
//             const blob = new Blob([csvContent], { type: 'text/csv' });
//             const url = URL.createObjectURL(blob);
//             const a = document.createElement('a');
//             a.href = url;
//             a.download = 'ip_risk_data.csv';
//             a.click();
//             URL.revokeObjectURL(url);
//         } else if (e.target && e.target.id === 'logoutButton') {
//             // Handle logout logic here
//             fetch(`http://localhost:5000/logout/${sessionStorage.getItem('user_id')}`, {
//                 method: 'GET',
//                 credentials: 'include',  // Include credentials with the request
//             })
//             .then(response => response.json())
//             .then(data => {
//                 if (data.message === 'Logged out successfully') {
//                     sessionStorage.removeItem('user_id');
//                     loadPage('login.html');
//                 } else {
//                     console.error('Logout failed');
//                 }
//             })
//             .catch(error => console.error('Error:', error));
//         }
//     });

//     function loadPage(page) {
//         fetch(`pages/${page}`)
//             .then(response => response.text())
//             .then(html => {
//                 document.getElementById('content').innerHTML = html;
//             })
//             .catch(error => {
//                 console.error('Error loading page:', error);
//             });
//     }
// });


document.addEventListener('DOMContentLoaded', function () {
    // Determine which page to load based on the state
    if (localStorage.getItem('login') === 'true') {
        loadPage('iprisk.html');
    } else if (localStorage.getItem('page2') === 'true') {
        loadPage('login.html');
    } else if (localStorage.getItem('page1') === 'true') {
        loadPage('page2.html');
    } else {
        loadPage('page1.html');
    }

    document.addEventListener('click', function (e) {
        if (e.target && e.target.id === 'formLinkButton') {
            loadPage('page2.html');
            localStorage.setItem('page1', 'true');
        } else if (e.target && e.target.id === 'submitButton') {
            const formLinkInput = document.getElementById('formLinkInput').value;
            if (formLinkInput.includes('responded') || formLinkInput.includes('alreadyresponded')) {
                loadPage('login.html');
                localStorage.setItem('page2', 'true');
            } else {
                document.getElementById('errorMessage').style.display = 'block';
            }
        } else if (e.target && e.target.id === 'signUpLink') {
            loadPage('signup.html');
        } else if (e.target && e.target.id === 'loginLink') {
            loadPage('login.html');
        } else if (e.target && e.target.id === 'loginButton') {
            // Handle login logic here
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            // Assume a local API call to validate the credentials
            if (email === 'user@gmail.com' && password === 'user123') {
                loadPage('iprisk.html');
                localStorage.setItem('login', 'true');
            } else {
                document.getElementById('loginErrorMessage').style.display = 'block';
            }
        } else if (e.target && e.target.id === 'signUpButton') {
            // Handle sign-up logic here
            const email = document.getElementById('signUpEmail').value;
            const password = document.getElementById('signUpPassword').value;
            // Assume a local API call to create the account
            if (email && password) {
                loadPage('login.html');
            } else {
                document.getElementById('signUpErrorMessage').style.display = 'block';
            }
        } else if (e.target && e.target.id === 'checkIpRiskButton') {
            const loader = document.getElementById('loader');
            loader.style.display = 'flex';

            // Extract ASIN from the current tab's URL
            chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
                const tab = tabs[0];
                try {
                    const url = new URL(tab.url);
                    let asin;
                    if (url.pathname.includes('/dp/')) {
                        asin = url.pathname.split('/dp/')[1].split('/')[0];
                    } else if (url.pathname.includes('/gp/product/')) {
                        asin = url.pathname.split('/gp/product/')[1].split('/')[0];
                    } else {
                        throw new Error('ASIN not found in the URL');
                    }

                    // Make a POST request to the local Flask API with the extracted ASIN
                    fetch('http://127.0.0.1:5000/analyze_data', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({ asin: asin })
                    })
                        .then(response => {
                            if (!response.ok) throw new Error('API request failed');
                            return response.json();
                        })
                        .then(data => {
                            loader.style.display = 'none';
                            document.getElementById('ipRiskScore').textContent = data.total_score;

                            const tableBody = document.querySelector('#riskTable tbody');
                            tableBody.innerHTML = '';
                            data.risk_factors.forEach(factor => {
                                const row = `
                                    <tr>
                                        <td>${factor.description}</td>
                                    </tr>
                                `;
                                tableBody.innerHTML += row;
                            });
                        })
                        .catch(error => {
                            loader.style.display = 'none';
                            alert(`Error: ${error.message}`);
                        });
                } catch (error) {
                    loader.style.display = 'none';
                    alert('Error parsing ASIN: ' + error.message);
                }
            });
        } else if (e.target && e.target.id === 'exportCsvButton') {
            const tableBody = document.querySelector('#riskTable tbody');
            const rows = tableBody.querySelectorAll('tr');
            const data = [['Risk Associated']];
            
            rows.forEach(row => {
                const cells = row.querySelectorAll('td');
                const rowData = Array.from(cells).map(cell => cell.textContent);
                data.push(rowData);
            });
            
            const csvContent = data.map(e => e.join(",")).join("\n");
            const blob = new Blob([csvContent], { type: 'text/csv' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'ip_risk_data.csv';
            a.click();
            URL.revokeObjectURL(url);
        } else if (e.target && e.target.id === 'logoutButton') {
            // Handle logout logic here
            loadPage('login.html');
            localStorage.setItem('login', 'false');
        }
    });

    function loadPage(page) {
        fetch(`pages/${page}`)
            .then(response => response.text())
            .then(html => {
                document.getElementById('content').innerHTML = html;
            })
            .catch(error => {
                console.error('Error loading page:', error);
            });
    }
});
