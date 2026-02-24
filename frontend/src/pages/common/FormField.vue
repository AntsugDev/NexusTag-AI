<template>
    <div class="form-field">
        <InputText v-model="model" :name="name" class="w-full p-inputtext-lg" :placeholder="placeholder" />
        <slot name="append"></slot>
        <Message v-if="form[key] && form[key]?.invalid" severity="error" size="small" variant="simple">{{
            form[key].error.message }}</Message>


    </div>

</template>
<script lang="js" setup>
import { defineComponent } from 'vue';
import InputText from 'primevue/inputtext';
import Message from 'primevue/message';

defineComponent({
    name: 'InputForm',
    components: {
        InputText,
        Message
    }
})

const model = defineModel('model')

const props = defineProps({
    name: {
        type: String,
        required: true
    },
    placeholder: {
        type: String,
        required: true
    },
    form: {
        type: Object,
        required: true
    },
    key: {
        type: String,
        required: true
    }
})
</script>
<style>
.form-field {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    width: 100%;
    padding-inline: 3px !important;
    margin-bottom: 10px;
}

.w-full {
    width: 100%;
}
</style>
