<template>
    <form method="POST" enctype="multipart/form-data" @submit.prevent="saveMovie" id="movieform">
        <div class="form-group mb-3">
            <label for="title" class="form-label">Movie Title</label>
            <input type="text" name="title" id="title" class="form-control" v-model="formData.title">
        </div>
        <div class="form-group mb-3">
            <label for="description" class="form-label">Description</label>
            <textarea name="description" id="description" class="form-control" v-model="formData.description"></textarea>
        </div>
        <div class="form-group mb-3">
            <label for="poster" class="form-label">Poster:</label>
            <input type="file" name="poster" id="poster" class="form-control" @change="handleFileChange">
        </div>
    </form>
</template>
<script>
    import {ref, onMounted} from 'vue';

    let crsf_token = ref('');

    const formData = ref({
        title: '',
        description: '',
        poster: null
    });

    function getCsrfToken() {
        fetch('/api/v1/csrf-token')
            .then(response => response.json())
            .then(data => {
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

    function saveMovie(){
        let movieform = document.getElementById('movieform')
        let form_date = new FormData(movieform)

        form_data.append('title'. formData.title)
        form_data.append('description'. formData.description)
        form_data.append('poster'. formData.poster)

        fetch('/api/v1/movies', {
            method: 'POST',
            body: form_data,
            headers: {
                'X-CSRFToken': crsf_token.value
            }
        })
        .then(function(response){
            return response.json();
        })
        .then(function(data){
            console.log(data);
        })
        .catch(function(error){
            console.log(error);
        });
    }
</script>