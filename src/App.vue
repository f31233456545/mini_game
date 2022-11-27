<script>
import Navigation from './components/Navigation.vue'
import PlayRoom from './views/PlayRoom.vue'

export default {
    components: { Navigation, PlayRoom },
    mounted() {
        if (this.$store.state !== null) {
            window.addEventListener('beforeunload', () => {
                sessionStorage.setItem('store', JSON.stringify(this.$store.state))
            })

            let oldStore = sessionStorage.getItem('store')
            if (oldStore !== null) {
                console.log(JSON.parse(oldStore))
                this.$store.replaceState(JSON.parse(oldStore))
            }
        }
    },
}

</script>

<template>

    <router-view></router-view>

</template>