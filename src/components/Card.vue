<template>
    <div class="card-container">
        <div :class="['card', size + '-card']">
            <div class="nocheck" />
            <div v-if="!open" class="back">
                <img :src="back">
            </div>
            <div
            v-show="open"
            :class="['card-num-left', size + '-num']"
            :style="{ color: cardColor }"
            >
                {{ cards }}
            </div>
            <div v-show="open"><img :src="cardType" class="card-type"></div>
            <div
            v-show="open"
            :class="['card-num-right', size + '-num']"
            :style="{ color: cardColor }"
            >
                {{ cards }}
            </div>
        </div>
    </div>

</template>

<script>
import back from '../assets/back.png'
import club from '../assets/club.png'
import diamond  from '../assets/diamond.png'
import heart from '../assets/heart.png'
import spade from '../assets/spade.png'

export default {
    name: 'Card',
    props: {
        value: {
            type: Number,
            default: 0
        },
        size: {
            type: String,
            default: 'small'
        },
    },
    computed: {
        open() {
            return (this.value!=0)
        },
        type() {
            let type=""
            if((this.value-1)/13 < 1){
                type="club"
            }
            else if((this.value-1)/13 < 2){
                type="diamond"
            }
            else if((this.value-1)/13 < 3){
                type="heart"
            }
            else{
                type="spade"
            }
            return type
        },
        back() {
            return back
        },
        cardType() {
            switch(this.type){
            case "club":
                return club
            case "diamond":
                return diamond
            case "heart":
                return heart
            case "spade":
                return spade
            }
        },
        cardColor() {
            const color = {
                heart: '#f00',
                diamond: '#f00',
                spade: '#000',
                club: '#000'
            }
            return color[this.type]
        },
        cards() {
            let tmp = ''
            let num = (this.value-1)%13 + 1
            switch (num.toString()) {
            case '1':
                tmp = 'A'
                break
            case '11':
                tmp = 'J'
                break
            case '12':
                tmp = 'Q'
                break
            case '13':
                tmp = 'K'
                break
            default:
                tmp = num.toString()
            }
            return tmp
        }
    }
}
</script>

<style scoped>
.card {
  position: relative;
  border-width: 1px;  
  border-style: solid;
  border-image: initial;
  border-color: #ccc;
  background: #ffffff;
  border-radius: 4px;
  font-family: monospace;
  text-align: center;
}
.big-card {
  width: 100px;
  height: 150px;
  font-weight: 600;
  font-size: 40px;
}
.small-card {
  width: 55px;
  height: 80px;
  font-weight: 200;
  font-size: 20px;
}
.card-num-left {
  text-align: left;
  padding-left: 2px;
}
.big-num {
  height: 50px;
  line-height: 50px;
}
.small-num {
  height: 24px;
  line-height: 24px;
}
.card-num-right {
  position: absolute;
  bottom: 0px;
  right: 2px;
  transform:rotate(180deg);
}
.card-type {
  height: 50%;
  width: 50%;
}
.back {
  height: 90%;
  width: 90%;
  margin: 5%;
  /* border: 1px dashed rgb(218, 107, 107); */
  background-color: #9999a3;
}
.back img {
  width: 100%;
  height: 100%;
}
.nocheck {
  position: absolute;
  height: 100%;
  width: 100%;
}
.card-container {
    display: flex;
    float: left;
}
</style>
