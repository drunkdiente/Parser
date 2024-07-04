document.addEventListener('DOMContentLoaded', function() {
    const searchForm = document.getElementById('search-form');
    if (searchForm) {
        searchForm.addEventListener('submit', function(event) {
            event.preventDefault();

            const formData = new FormData(this);
            const params = new URLSearchParams();
            for (const pair of formData) {
                params.append(pair[0], pair[1]);
            }

            fetch('/search', {
                method: 'POST',
                body: params
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                const resultsDiv = document.getElementById('results');
                resultsDiv.innerHTML = '<h2>Results</h2>';
                const ul = document.createElement('ul');
                data.forEach(vacancy => {
                    const li = document.createElement('li');
                    li.innerHTML = `
                        <strong>${vacancy.name}</strong><br>
                        <a href="${vacancy.alternate_url}" target="_blank">${vacancy.alternate_url}</a><br>
                        ${vacancy.salary ? `Salary: ${vacancy.salary}<br>` : ''}
                        Employer: ${vacancy.employer}<br>
                        Requirement: ${vacancy.requirement}
                    `;
                    ul.appendChild(li);
                });
                resultsDiv.appendChild(ul);
            })
            .catch(error => {
                console.error('Error during fetch:', error);
            });
        });
    }
});
