<script setup>
  import { ref } from 'vue'
  // import axios from 'axios'
  // const axios = require('axios').default;

  const props = defineProps({
    packName: String,
    packs: {
      type: Array,
      required: false,
      default: false
    }
  })

  const newPackName = ref("")

</script>

<template>
  <div class="app-container">
      <div v-for="pack, index in packs">
        <p>
          <span>{{pack}}</span>
          <button @click="removePack(index)">❌</button>
          <button @click="moveDown(index)" v-if="index!=packs.length-1">🔽</button>
          <button @click="moveUp(index)" v-if="index>0">🔼</button>
        </p>
        
      </div>

      <div>
        <input type="text" v-model="newPackName"/>
        <button @click="addPack">Add</button>
      </div>
  </div>
</template>

<script>

export default {
  data() {
    return {};
  },
  methods: {
    addPack(){
      const link = this.newPackName.match(/^https\:\/\/t\.me\/addstickers\/(\w\w+)$/)
      const nonlink = this.newPackName.match(/^(\w\w+)$/)
      
      if(!link && !nonlink){
        this.newPackName = ""
        return
      }
      var packToAdd = link ? link[1] : nonlink[1]

      if(!this.packs.includes(packToAdd))
        this.packs.push(packToAdd)
      this.newPackName = ""
      this.updateURL()
    },
    removePack(index){
      this.packs.splice(index, 1)
      this.updateURL()
    },
    moveUp(index){
      if(index==0) return
      var temp = this.packs[index]
      this.packs[index] = this.packs[index-1]
      this.packs[index-1] = temp
      this.updateURL()
    },
    moveDown(index){
      if(index==this.packs.length-1) return
      var temp = this.packs[index]
      this.packs[index] = this.packs[index+1]
      this.packs[index+1] = temp
      this.updateURL()
    },
    updateURL(){
      var searchParams = this.packs.join("&")
      var newRelativePathQuery = window.location.pathname + '?' + searchParams.toString();
      history.pushState(null, '', newRelativePathQuery);
    }
  }
};
</script>

<style scoped>

.app-container{
  border-radius: 30px;
  max-width: 500px;
  border: 1px solid #ccc;
  margin-bottom: 20px;
  margin-right: auto;
  margin-left: auto;
  background-color: rgba(0,0,0,0.2);
  padding: 10px;
  height: 80vh;
  color: #fff;
}

</style>
