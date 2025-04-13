<template>
    <div class="form-wrapper">
        <div class="form-container">
            <div v-if= "successMsg" class="message success">{{ successMsg }}</div>
            <div v-if="failedMessage.length > 0" class="message error">
                <ul>
                    <li v-for="(message, index) in failedMessage" :key="index">{{ message }}</li>
                </ul>
            </div>
            <form method="POST" enctype="multipart/form-data" @submit.prevent="saveMovie" id="movieForm">
                <div class="form-group mb-3">
                    <label for="title" class="form-label">Movie Title</label>
                    <input type="text" id="title" name="title" class="form-control" v-model="formData.title">
                </div>
                <div class="form-group mb-3">
                    <label for="description" class="form-label">Description</label>
                    <textarea name="description" id="description" class="form-control" v-model="formData.description"></textarea>
                </div >
                <div class="form-group mb-3">
                    <label for="poster" class="form-label">Movie Poster</label>
                    <input type="file" id="poster" name="poster" class="form-control" @change="handleFileChange">
                </div>
                <button type="submit" class="btn btn-primary">Submit</button>
            </form>
        </div>
    </div>
</template>
<script setup>
    import {ref, onMounted} from 'vue';

    let csrf_token = ref('');
    const successMsg = ref('');
    const failedMessage =ref([]);

    const formData = ref({
        title: '',
        description: '',
        poster: null
    });

    function getCsrfToken() {
        fetch('/api/v1/csrf-token')
            .then((response) => response.json())
            .then((data) => {
                console.log(data);
                csrf_token.value = data.csrf_token;
            })
            .catch(error => {
                console.error('Error fetching CSRF token:', error);
            });
    }

    onMounted(() => {
        getCsrfToken();
    });
    function handleFileChange(event) {
        formData.poster = event.target.files[0];
    }

    function saveMovie(){
        let movieForm = document.getElementById('movieForm');
        let form_data = new FormData(movieForm);

        form_data.append('title', formData.title);
        form_data.append('description', formData.description);
        form_data.append('poster', formData.poster);

        fetch('/api/v1/movies', {
            method: 'POST',
            body: form_data,
            headers: {
                'X-CSRFToken': csrf_token.value
            }
        })
        .then(function (response) {
            if (!response.ok) {
                throw new Error('Network Error! Network did not respond properly.');
            }
            return response.json();
        })
        .then(function (data) {
            console.log(data);
            formData.value = {
                title: '',
                description: '',
                poster: null
            };
            movieForm.reset();
            successMsg.value = '';
            failedMessage.value = [];
            successMsg.value = 'File Upload Successfully';
        })
        .catch(function (error) {
            console.error('Problem with the fetch operation', error);
            successMsg.value = '';
            failedMessage.value = [];

            if (!formData.value.title.trim()){
                failedMessage.value.push('Title field not filled - This field is required');
            }
            if (!formData.value.description.trim()){
                failedMessage.value.push('Description field not filled - This field is required');
            }
            if (!formData.poster){
                failedMessage.value.push('No file attached for the poster field - This field is required');
            }
        });
    }

</script>
<style scoped>
    .form-wrapper {
        flex: 1;
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 3rem 1rem;
        background: #f5f7fa; 
    }

    .form-container {
        background: #ffffff;
        padding: 2.5rem;
        border-radius: 1rem;
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.1);
        width: 100%;
        max-width: 700px; 
    }

    .form-group {
        margin-bottom: 1.5rem;
    }

    .form-label {
        display: block;
        margin-bottom: 0.5rem;
        font-weight: bold;
        color: #333333;
    }

    .form-control {
        width: 100%;
        padding: 0.75rem;
        border: 1px solid #cccccc;
        border-radius: 0.5rem;
        font-size: 1rem;
        transition: border-color 0.3s ease;
    }

    .form-control:focus {
        border-color: #4a90e2;
        outline: none;
    }

    .message {
        margin-bottom: 1rem;
        padding:  1rem;
        border-radius: 0.5rem;
        font-weight: 500;
        text-align: center;
    }

    .success {
        background-color: #e0f7e9;
        color: #2e7d32;
        border: 1px solid #2e7d32;
    }

    .error {
        background-color: #fdecea;
        color: #c62828;
        border: 1px solid #c62828;
    }

    textarea.form-control {
        min-height: 100px;
        resize: vertical;
    }

</style>