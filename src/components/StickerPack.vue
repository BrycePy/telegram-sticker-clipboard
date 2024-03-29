<script setup>
  import { ref } from 'vue'
  import axios from 'axios'
  // const axios = require('axios').default;

  const props = defineProps({
    packName: String,
    showEmoji: {
      type: Boolean,
      required: false,
      default: false
    },
    copySize: {
      type: Number,
      required: false,
      default: 512
    },
    numOfCol: {
      type: Number,
      required: false,
      default: 5
    },
    previewSize: {
      type: String,
      required: false,
      default: "120px"
    }
  })

  const stickers = ref([])
  const status = ref({success: true, error_message: ""})

  axios({
      method: 'post',
      url: `https://sticker.dfg87dcbvse44.xyz/pack`,
      data: {
        packName: props.packName
      }
    }).then(async function (response) {
      // handle success
      response.data.forEach((sticker) => {
        sticker["image_link"] = `https://sticker.dfg87dcbvse44.xyz/sticker/${sticker.file_id}`
      })
      if(response.data[0].is_animated){
        status.value = {success: false, error_message: "Animated stickers are not supported yet."}
      }else{
        for(var sticker of response.data) {
          await new Promise(resolve => setTimeout(resolve, 5));
          stickers.value.push(sticker)
        }
      }
    })
    .catch(function (error) {
      // handle error
      status.value = {success: false, error_message: error}
      console.log(error);

      if(error.response.status == 500){
        status.value["error_message"] += "\n(unable to load sticker pack)"
      }

    })
    .then(function () {
      // always executed
  });
</script>

<template>
  <div class="app-container">
    <div v-if="!status.success" class="error_message_warp">
      <p class="error_message_text">{{status.error_message}}</p>
    </div>
    <div class="sticker-warp">
      <div v-for="sticker in stickers" :key="sticker" class="sticker-container">
        <img class="sticker-img" :src="sticker.image_link" @click="copy" crossorigin="anonymous"/>
        <span v-if="showEmoji" class="sticker-emote">{{sticker.emoji}}</span>
      </div>
    </div>
    <canvas id="blobTemp" style="display:none;" ref="blobTemp"></canvas>
  </div>
</template>

<script>

function playShakeAnimation(element){
  element.classList.add('shake-animation');
  setTimeout(() => {
    element.classList.remove('shake-animation');
  }, 100);
}

export default {
  data() {
    return {};
  },
  methods: {
    copy(img_raw) {
      const img = img_raw.target

      const canvas = this.$refs.blobTemp;

      const TARGETWIDTH = this.copySize;

      canvas.width = TARGETWIDTH;
      canvas.height = TARGETWIDTH;
      const w = img.width;
      const h = img.height;
      const asp = w / h;

      var aw, ah
      var [dx, dy] = [0, 0];
      var scale;

      if(w<h){
        scale = TARGETWIDTH / h;
        aw = Math.floor(h * scale * asp) ;
        ah = Math.floor(h * scale);
        dx = Math.floor((TARGETWIDTH - aw) / 2);
      }else{
        scale = TARGETWIDTH / w;
        aw = Math.floor(w * scale);
        ah = Math.floor(w * scale / asp);
        dy = Math.floor((TARGETWIDTH - ah) / 2);
      }

      console.log(w, h, asp, scale)
      console.log(aw, ah);
      console.log(dx, dy);

      const draw = canvas.getContext("2d")
      draw.clearRect(0, 0, canvas.width, canvas.height);
      draw.drawImage(img, dx, dy, aw, ah);
      canvas.toBlob((blob) => {
        navigator.clipboard.write([
            new ClipboardItem({ "image/png": blob })
        ]);
        playShakeAnimation(img.parentElement);
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
  background-color: rgba(0,0,0,0.2);
  padding: 10px;
  height: 80vh;
  overflow-y: scroll;
  overflow-x: hidden;
}

/* width */
.app-container::-webkit-scrollbar {
  width: 10px;
}

/* Track */
.app-container::-webkit-scrollbar-track {
  display: none;
}

/* Handle */
.app-container::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 10px;
  background-clip: content-box;
}

/* Handle on hover */
.app-container::-webkit-scrollbar-thumb:hover {
  background: #555;
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
  grid-template-columns: repeat(v-bind(numOfCol), 1fr);
}

.sticker-img {
  max-width: 100%;
  max-height: 100%;
  cursor: pointer;
}

.sticker-container {
  max-width: v-bind(previewSize);
  max-height: v-bind(previewSize);
  aspect-ratio: 1/1;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 5px;
  border-radius: 100%;
  transition: all 0.1s ease-in-out;
  position: relative;
  caret-color: transparent;
}

.sticker-container:hover {
  border-radius: 10px;
  background-color: rgba(255, 255, 255, 0.1);
}

.sticker-emote{
  bottom: 0;
  right: 0;
  position: absolute;
  font-size: 25px;
  transition: all 0.1s ease-in-out;
  text-shadow: 0px 0px 8px black;
}

.sticker-container:hover > .sticker-emote{
  opacity: 0.5;
}

.error_message_warp{
  width: 80%;
  margin-left: auto;
  margin-right: auto;
  padding: 10px;
  border-radius: 10px;
  background-color: rgba(255, 0, 0, 0.2);
}

.error_message_text{
  color: #fff;
  font-size: 20px;
}

.shake-animation{
  animation: shake 0.1s 1;
}

@keyframes shake {
  0% { transform: translate(1px, 1px) rotate(0deg); }
  10% { transform: translate(-1px, -2px) rotate(-1deg); }
  20% { transform: translate(-3px, 0px) rotate(1deg); }
  30% { transform: translate(3px, 2px) rotate(0deg); }
  40% { transform: translate(1px, -1px) rotate(1deg); }
  50% { transform: translate(-1px, 2px) rotate(-1deg); }
  60% { transform: translate(-3px, 1px) rotate(0deg); }
  70% { transform: translate(3px, 1px) rotate(-1deg); }
  80% { transform: translate(-1px, -1px) rotate(1deg); }
  90% { transform: translate(1px, 2px) rotate(0deg); }
  100% { transform: translate(1px, -2px) rotate(-1deg); }
}

</style>
