<script setup>
  import { ref } from 'vue'
  import axios from 'axios'
  // const axios = require('axios').default;

  const props = defineProps({
    packName: String
  })

  const count = ref(0)
  const stickers = ref([])

  axios({
      method: 'post',
      url: `http://127.0.0.1:5000/pack`,
      data: {
        packName: props.packName
      }
    }).then(function (response) {
      // handle success
      stickers.value = response.data.files.map(file => {
        return {name: file, link: `http://localhost:5000/sticker/${file}`}
      })
    })
    .catch(function (error) {
      // handle error
      console.log(error);
    })
    .then(function () {
      // always executed
  });
</script>

<template>
  <div class="app-container">
    <h1 class="header-text">{{ packName }}</h1>

    <div class="sticker-warp">
      <div v-for="sticker in stickers" :key="sticker">
        <div class="sticker-container">
          <img class="sticker-img" :src="sticker.link" @click="copy" ref="test" crossorigin="anonymous">
        </div>
      </div>
    </div>
    <canvas id="blobTemp" style="display:none; position:absloute;" ref="blobTemp" width=512 height=512></canvas>
  </div>
</template>

<script>

export default {
  data() {
    return {};
  },
  methods: {
    copy(img_raw) {
      const img = img_raw.target

      const canvas = this.$refs.blobTemp;

      const asp = img.width / img.height;
      const w = img.width;
      const h = img.height;
      var aw, ah
      var [dx, dy] = [0, 0];
      var scale;

      if(w<h){
        scale = 512 / h;
        aw = Math.floor(h * asp * scale) ;
        ah = Math.floor(h * scale);
        dx = Math.floor((512 - aw) / 2);
      }else{
        scale = 512 / w;
        aw = Math.floor(w * scale);
        ah = Math.floor(w / asp * scale);
        dy = Math.floor((512 - ah) / 2);
      }
      console.log(w, h, asp, scale)
      console.log(aw, ah);

      const draw = canvas.getContext("2d")
      draw.clearRect(0, 0, canvas.width, canvas.height);
      draw.drawImage(img, dx, dy, aw, ah);
      canvas.toBlob((blob) => {
        navigator.clipboard.write([
            new ClipboardItem({ "image/png": blob })
        ]);
      }, "image/png");
    },
  }
};
</script>

<style scoped>

.app-container{
  border-radius: 30px;
  width: fit-content;
  border: 1px solid #ccc;
  margin-bottom: 20px;
  margin-right: auto;
  margin-left: auto;
}

.header-text {
  font-size: 30px;
  font-weight: bold;
  color: #fff;
  padding: 20px;
  margin: 0px;
}

.sticker-warp {
  margin-left: auto;
  margin-right: auto;
  width: fit-content;
  display: grid;
  grid-template-columns: repeat(5, 1fr);
}

.sticker-img {
  width: 100%;
  height: 100%;
  object-fit: contain;  
  cursor: pointer;
}

.sticker-container {
  width: 120px;
  height: 120px;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 5px;
  transition: all 0.1s ease-in-out;
}

.sticker-container:hover {
  border-radius: 10px;
  background-color: rgba(255, 255, 255, 0.1);
}

</style>
