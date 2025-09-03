document.addEventListener('DOMContentLoaded', () => {
    const bioInput = document.querySelector('input[name="bio"]')
    const submitBtn = document.querySelector('button[type="submit"]')

    const originalBio = bioInput.dataset.original

    function toggleButton() {
        let allFilled = true

        if (bioInput.value.trim().length === 0 || bioInput.value.trim() === originalBio) {
            allFilled = false
        }

        submitBtn.disabled = !allFilled
    }

    toggleButton()
    bioInput.addEventListener('input', toggleButton)
})

document.getElementById('image').addEventListener('change', (event) => {
    const userImage = document.getElementById('user_image')
    const userDefaultImage = document.getElementById('user_default_image')
    const submitBtn = document.querySelector('button[type="submit"]')
    const file = event.target.files[0]

    if (file) {
        const reader = new FileReader()

        reader.onload = (e) => {
            if (userImage && !userDefaultImage) {
                userImage.style.backgroundImage = `url(${e.target.result})`
            } else if (!userImage && userDefaultImage) {
                userDefaultImage.src = e.target.result
            }
        }

        reader.readAsDataURL(file)
        submitBtn.disabled = false
    }
})
