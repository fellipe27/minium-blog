document.addEventListener('DOMContentLoaded', () => {
    const form = document.querySelector('form')
    const inputs = form.querySelectorAll('input')
    const submitBtn = form.querySelector('button[type="submit"]')

    function toggleButton() {
        let allFilled = true

        inputs.forEach(input => {
            if (!input.value.trim()) {
                allFilled = false
            }
        })

        submitBtn.disabled = !allFilled
    }

    toggleButton()
    inputs.forEach(input => input.addEventListener('input', toggleButton))
})
