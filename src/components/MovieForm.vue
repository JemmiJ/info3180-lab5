<template>
    <form method="POST" enctype="multipart/form-data" @submit.prevent="saveMovie" id="movieForm">
        <div class="form-group mb-3">
            <label for="title" class="form-label">Movie Title</label>
            <input type="text" id="title" name="title" class="form-control" v-model="formData.title">
        </div>
        <div class="form-group mb-3">
            <label for="description" class="form-label">Description</label>
            <textarea name="description" id="description" class="form-control" v-model="formData.description"></textarea>
        </div >
        <div v-if= "successMsg" class="message success">{{ successMsg }}</div>
        <div v-if="failedMessage.length > 0" class="message error">
            <ul>
                <li v-for="(message, index) in failedMessage" :key="index">{{ message }}</li>
            </ul>
        </div>
        <div class="form-group mb-3">
            <label for="poster" class="form-label">Poster:</label>
            <input type="file" id="poster" name="poster" class="form-control" @change="handleFileChange">
        </div>
        <button type="submit" class="btn btn-primary">Submit</button>
    </form>
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
            successMsg.value = 'File Upload Successfully'
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

    #movieForm{
        margin: 15px 50px 10px 50px;
    }
    .success{
        background-color: green;
        color: white;
        border-radius: 7px;
        font-size: 11px;
        padding: 11px;
        margin-bottom: 10px;
    }
    .error{
        background-color: red;
        color: white;
        border-radius: 7px;
        font-size: 11px;
        padding: 11px;
        margin-bottom: 10px;
    }

</style>