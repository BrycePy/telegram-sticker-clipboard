<script setup>
// This starter template is using Vue 3 <script setup> SFCs
// Check out https://vuejs.org/api/sfc-script-setup.html#script-setup
import StickerPack from './components/StickerPack.vue'
</script>

<template>
  <StickerPack packName="minitwolf" v-bind:copySize="170" />
  <StickerPack packName="glitchcat" showEmoji />
  <StickerPack packName="glitchcat2"/>
  <StickerPack packName="kesufox"/>
</template>

<style>
body{
  margin: 0;
  padding: 0;
}

#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  margin: 0;
  padding: 0;
  color: #2c3e50;
  background-color: #343e66;
}
</style>
