<template>
    <div class="flex-icons">
        <i v-for="icon,index in icons" :key="index" v-if="showIcon(icon)" :class="icon.class + ' icon-cust'" @click="icon?.action" :style="getStyle(icon)"
        v-tooltip="icon.tooltip" v-tooltip-position="Bottom"
        ></i>
    </div>

</template>
<script setup>
import { defineComponent } from 'vue'

defineComponent({
    name: 'IconsTable',
    components: {
    }
})

defineProps({
    icons: {
        Array,
        required: true
    }
})

const showIcon = (icon) => {
    console.log(icon?.is_view)
    return icon?.is_view ?? true
}

const getStyle = (icon) => {
    if (icon?.color){
        return `color: ${icon.color};font-size: 1.2rem;`
    }
}

</script>
<style lang="css" scoped>
.flex-icons {
    display: flex;
    flex-direction: row;
    gap: 1rem;
    justify-content: center;
    align-items: center;
}
.icon-cust{
    cursor: pointer;
}
</style>
