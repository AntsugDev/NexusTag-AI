<template>
    <Dialog v-model:visible="visible" modal position="top" :header="header" maximizable
    style="    min-width: 500px !important;min-height: 400px"
    >
        <slot></slot>
    </Dialog>

</template>

<script lang="js" setup>
import Dialog from 'primevue/dialog';
import { defineComponent } from 'vue';
import PageBase from './PageBase.vue';

const visible = defineModel('visible')
const props = defineProps({
    header: {
        type: String,
        required: false,
        default: ''
    },
    backRoute: {
        type: Object,
        required: false,
        default: null
    }
})

const closeDialog = () => {
    visible.value = false
}



defineComponent({
    name: 'DialogCommon',
    components: [
        Dialog
    ]
})
</script>
<style scoped>
.footer {
    display: flex;
    justify-content: flex-end;
    align-items: center;
    padding: 1rem;
}
</style>
<style>
.p-dialog{
    min-width: 300px!important;
}
.p-dialog-header {
    padding: 10px;
    background-color: #314158;
    border-bottom: 1px solid #99A1AF;
    color: #fff;
}
.p-dialog-header-actions{
    margin-right: 10px;
}

.p-dialog-header-actions>.p-button {
    background-color: #fff!important;
}
</style>