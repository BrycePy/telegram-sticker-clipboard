<script setup>

import StickerPack from './components/StickerPack.vue'
import { ref } from 'vue'
import {Tabs, Tab} from 'vue3-tabs-component';

const packs = ref([])
packs.value.push("minitwolf")
packs.value.push("glitchcat")
packs.value.push("glitchcat2")
packs.value.push("kesufox")

</script>

<template>
  <Tabs :options="{ useUrlFragment: false }">
    <Tab v-for="pack in packs" v-bind:name="pack">
      <StickerPack v-bind:packName="pack" showEmoji/>
    </Tab>
  </Tabs>
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
  min-height: 100vh;
}


.tabs-component {
  padding-top: 20px;
  margin-top: 0;
  margin-right: auto;
  margin-left: auto;
}

.tabs-component-tabs {
  border: 0;
  align-items: stretch;
  display: flex;
  justify-content: center;
  margin-bottom: 0;
  margin-top: 0;
  color: #fff;
  font-size: 14px;
  font-weight: 600;
  list-style: none;
  overflow-y: hidden;
  overflow-x: scroll;
  margin-left: auto;
  margin-right: auto;
  padding-bottom: 5px;
  margin-bottom: 5px;
}

/* width */
.tabs-component-tabs::-webkit-scrollbar {
  height: 10px;
}

/* Track */
.tabs-component-tabs::-webkit-scrollbar-track {
  display: none;
}

/* Handle */
.tabs-component-tabs::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 10px;
  background-clip: content-box;
}

/* Handle on hover */
.tabs-component-tabs::-webkit-scrollbar-thumb:hover {
  background: #555;
}

.tabs-component-tab:hover {
    color: #666;
}

.tabs-component-tab {
  background-color: #888;
  border: solid 1px #ddd;
  border-radius: 5px;
  margin-right: .5em;
}

.tabs-component-tab.is-active {
    background-color: #fff;
    color: #000;
    border-bottom: solid 1px #fff;
    z-index: 2;
}

.tabs-component-tab-a {
    align-items: center;
    color: inherit;
    display: flex;
    padding: .75em 1em;
    text-decoration: none;
}

.tabs-component-panels {
}

</style>
