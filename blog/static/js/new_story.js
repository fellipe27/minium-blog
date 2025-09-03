let imageChanged = false

document.addEventListener('DOMContentLoaded', () => {
    const titleInput = document.querySelector('input[name="title"]')
    const storyTextarea = document.querySelector('textarea[name="story"]')
    const image = document.getElementById('selected_image')
    const submitBtn = document.querySelector('#publish_btn')

    const originalTitle = titleInput.dataset.original
    const originalStory = storyTextarea.dataset.original
    const originalImage = image.dataset.original

    if (originalImage) {
        image.style.backgroundImage = `url('data:image/jpeg;base64,${originalImage}')`
    }

    function toggleButton() {
        const currentTitle = titleInput.value.trim()
        const currentStory = storyTextarea.value.trim()
        let allFilled = true

        if (
            (currentTitle.length === 0 || currentStory.length === 0) ||
            (currentTitle === originalTitle && currentStory === originalStory)
        ) {
            allFilled = false
        }

        submitBtn.disabled = !allFilled

        if (imageChanged) {
            submitBtn.disabled = false
        }
    }

    toggleButton()
    titleInput.addEventListener('input', toggleButton)
    storyTextarea.addEventListener('input', toggleButton)
})

document.querySelector('#publish_btn').addEventListener('click', () => {
    document.querySelector('button[type="submit"]').click()
})

document.getElementById('image').addEventListener('change', (event) => {
    const previewImage = document.getElementById('preview')
    const selectedImage = document.getElementById('selected_image')
    const titleInput = document.querySelector('input[name="title"]')
    const storyTextarea = document.querySelector('textarea[name="story"]')
    const submitBtn = document.querySelector('#publish_btn')
    const file = event.target.files[0]

    if (file) {
        const reader = new FileReader()

        reader.onload = (e) => {
            previewImage.style.display = 'none'
            selectedImage.style.backgroundImage = `url(${e.target.result})`
            selectedImage.style.display = 'block'
        }

        reader.readAsDataURL(file)

        if (titleInput.value.trim().length > 0 && storyTextarea.value.trim().length > 0) {
            submitBtn.disabled = false
            imageChanged = true
        }
    }
})
