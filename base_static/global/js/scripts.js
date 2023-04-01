(() => {
    const forms = document.querySelectorAll('.form-delete');
    for (const form of forms) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            const confirmed = confirm('Are you sure?');
            if(confirmed) {
                form.submit();
            }
        });
    }
    window.addEventListener("beforeunload", function(event) {
        fetch(clearSessionUrl, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken
            }
        });
    });
})();