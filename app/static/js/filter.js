document.addEventListener('DOMContentLoaded', function() {
    const filterForm = document.getElementById('filter-form');
    if (filterForm) {
        filterForm.addEventListener('submit', function(event) {
            event.preventDefault();

            const formData = new FormData(this);
            const params = new URLSearchParams();
            for (const pair of formData) {
                params.append(pair[0], pair[1]);
            }

            fetch('/database?' + params.toString(), {
                headers: {
                    'Accept': 'application/json'
                }
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                const tbody = document.getElementById('vacancy-list');
                tbody.innerHTML = '';
                data.forEach(vacancy => {
                    const tr = document.createElement('tr');
                    tr.innerHTML = `
                        <td>${vacancy.id}</td>
                        <td>${vacancy.name}</td>
                        <td><a href="${vacancy.alternate_url}" target="_blank">${vacancy.alternate_url}</a></td>
                        <td>${vacancy.salary}</td>
                        <td>${vacancy.employer}</td>
                        <td>${vacancy.requirement}</td>
                    `;
                    tbody.appendChild(tr);
                });
            })
            .catch(error => {
                console.error('Error during fetch:', error);
            });
        });
    }
});
