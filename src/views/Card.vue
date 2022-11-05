<template>
<div class="card">
    <div v-if="!open" class="back">
    <img :src="back0" alt="">
    </div>
    <div v-if="open" class="front">
    <img :src="cards" alt="">
    </div>
</div>
</template>

<script>
import back0 from "../assets/back.png"
import c1 from "../assets/c1.png"
import c2 from "../assets/c2.png"
import c3 from "../assets/c3.png"
import c4 from "../assets/c4.png"
import c5 from "../assets/c5.png"
import c6 from "../assets/c6.png"
import c7 from "../assets/c7.png"
import c8 from "../assets/c8.png"
import c9 from "../assets/c9.png"
import c10 from "../assets/c10.png"
import c11 from "../assets/c11.png"
import c12 from "../assets/c12.png"
import c13 from "../assets/c13.png"
import d1 from "../assets/d1.png"
import d2 from "../assets/d2.png"
import d3 from "../assets/d3.png"
import d4 from "../assets/d4.png"
import d5 from "../assets/d5.png"
import d6 from "../assets/d6.png"
import d7 from "../assets/d7.png"
import d8 from "../assets/d8.png"
import d9 from "../assets/d9.png"
import d10 from "../assets/d10.png"
import d11 from "../assets/d11.png"
import d12 from "../assets/d12.png"
import d13 from "../assets/d13.png"
import h1 from "../assets/h1.png"
import h2 from "../assets/h2.png"
import h3 from "../assets/h3.png"
import h4 from "../assets/h4.png"
import h5 from "../assets/h5.png"
import h6 from "../assets/h6.png"
import h7 from "../assets/h7.png"
import h8 from "../assets/h8.png"
import h9 from "../assets/h9.png"
import h10 from "../assets/h10.png"
import h11 from "../assets/h11.png"
import h12 from "../assets/h12.png"
import h13 from "../assets/h13.png"
import s1 from "../assets/s1.png"
import s2 from "../assets/s2.png"
import s3 from "../assets/s3.png"
import s4 from "../assets/s4.png"
import s5 from "../assets/s5.png"
import s6 from "../assets/s6.png"
import s7 from "../assets/s7.png"
import s8 from "../assets/s8.png"
import s9 from "../assets/s9.png"
import s10 from "../assets/s10.png"
import s11 from "../assets/s11.png"
import s12 from "../assets/s12.png"
import s13 from "../assets/s13.png"

export default {
  name: 'Card',
  components: {

    },
  props: {
    num: {
      type: Number,
      default: 51
    },
    open: {
      type: Boolean,
      default: true
    }
  },
  computed: {
    cards() {
      switch (this.num) {
        case 1:
            return c1
        case 2:
            return c2
        case 3:
            return c3
        case 4:
            return c4
        case 5:
            return c5
        case 6:
            return c6
        case 7:
            return c7
        case 8:
            return c8
        case 9:
            return c9
        case 10:
            return c10
        case 11:
            return c11
        case 12:
            return c12  
        case 13:
            return c13
        case 14:
            return d1
        case 15:
            return d2
        case 16:
            return d3
        case 17:
            return d4
        case 18:
            return d5
        case 19:
            return d6
        case 20:
            return d7
        case 21:
            return d8
        case 22:
            return d9
        case 23:
            return d10
        case 24:
            return d11
        case 25:
            return d12  
        case 26:
            return d13
        case 27:
            return h1
        case 28:
            return h2
        case 29:
            return h3
        case 30:
            return h4
        case 31:
            return h5
        case 32:
            return h6
        case 33:
            return h7
        case 34:
            return h8
        case 35:
            return h9
        case 36:
            return h10
        case 37:
            return h11
        case 38:
            return h12  
        case 39:
            return h13
        case 40:
            return s1
        case 41:
            return s2
        case 42:
            return s3
        case 43:
            return s4
        case 44:
            return s5
        case 45:
            return s6
        case 46:
            return s7
        case 47:
            return s8
        case 48:
            return s9
        case 49:
            return s10
        case 50:
            return s11
        case 51:
            return s12
        case 52:
            return s13
        default:
            return s12
      }
    }
  },
  data() {
    return {
        back0: back0,
        c1: c1,
        c2: c2,
        c3: c3,
        c4: c4,
        c5: c5,
        c6: c6,
        c7: c7,
        c8: c8,
        c9: c9,
        c10: c10,
        c11: c11,
        c12: c12,
        c13: c13,
        d1: d1,
        d2: d2,
        d3: d3,
        d4: d4,
        d5: d5,
        d6: d6,
        d7: d7,
        d8: d8,
        d9: d9,
        d10: d10,
        d11: d11,
        d12: d12,
        d13: d13,
        h1: h1,
        h2: h2,
        h3: h3,
        h4: h4,
        h5: h5,
        h6: h6,
        h7: h7,
        h8: h8,
        h9: h9,
        h10: h10,
        h11: h11,
        h12: h12,
        h13: h13,
        s1: s1,
        s2: s2,
        s3: s3,
        s4: s4,
        s5: s5,
        s6: s6,
        s7: s7,
        s8: s8,
        s9: s9,
        s10: s10,
        s11: s11,
        s12: s12,
        s13: s13,
    }
  },
}
</script>
