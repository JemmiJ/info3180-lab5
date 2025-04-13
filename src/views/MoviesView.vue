<template>
    <h1 class="movie-head">Movies</h1>
    <div class="movie-list" id="movie-list">
        <div class="movie-container" v-for="m in movies" :key="m.id">
            <img :src="getURL(m.poster)" class="movie-poster" :alt="m.title">
            <div class="movie-details">
                <h4 class="movie-title">{{ m.title }}</h4>
                <p class="movie-description">{{ m.description }}</p>
            </div>
        </div>
    </div>
</template>
<script setup>
    import { ref, onMounted } from 'vue';
    let movies = ref([]);

    onMounted( async function fetchMovies() {
        try{
            const response = await fetch('/api/v1/movies');
            if (!response.ok) {
                throw new Error('Could not fetch movies');
            }
            const data = await response.json();
            movies.value = data.movies;
        }
        catch (error) {
            console.error('Fetching movies error:', error);
        }
    });

    function getURL(filename) {
        return `/api/v1/posters/${filename}`;
    }
</script>
<style scoped>
    .movie-head {
        margin-bottom: 30px;
        font-size: 36px;
        font-weight: 700;
        text-align: center;
        color: #333;
    }
    .movie-list {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        row-gap: 10px;
        column-gap: 70px;
        margin: 15px 50px 10px 50px;
    }
    .movie-container {
        width: auto;
        background: white;
        overflow: hidden;
        border: 1px solid #ccc;
        border-radius: 12px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.08);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        display: grid;
        grid-template-columns: 200px 400px;
        gap: 20px;
        height: 300px;
    }
    .movie-poster {
        width: 100%;
        height: 100%;
        object-fit: cover;
        border-top-left-radius: 10px;
        border-bottom-left-radius: 10px;
    }
    .movie-details {
        padding: 20px;
    }
    .movie-title {
        margin-bottom: 10px;
        font-size: 20px;
        font-weight: bold;
        color: #222;
    }
    .movie-description {
        font-size: 16px;
        line-height: 1.5;
        color: #222;
    }
</style>