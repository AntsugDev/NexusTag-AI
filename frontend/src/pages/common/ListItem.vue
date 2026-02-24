<template>
    <Row>
       {{ text }} 
    </Row>
</template>
<script lang="js" setup>
import Row from 'primevue/row';
const props = defineProps({
    text: {
        String,
        required: true
    }
})

</script>
<style lang="css" scoped>
.list-item {
    padding: 6px;
    margin-right: 2px;
}
</style>