document.querySelector('form').addEventListener('submit', async function(e) {
    e.preventDefault()
    const form = e.target
    const formData = new FormData(form)
    const reqData = Object.fromEntries(formData.entries())
    
    const resp = await fetch('/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(reqData)
    })

    let success = false

    if (resp.status == 200)
        success = true

    const json = await resp.json()
    const submissionStatus = document.querySelector('#status')
    
    submissionStatus.innerText = json.message

    submissionStatus.classList.remove('alert-primary')
    submissionStatus.classList.toggle('alert-success', success)
    submissionStatus.classList.toggle('alert-danger', !success)

    if (success) {
        window.location.href = '/'
    }
});