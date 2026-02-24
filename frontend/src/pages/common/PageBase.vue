<template>
    <Card class="page glass-panel">
        <template #header>
            <div class="title">
                <h2>{{ title }}</h2>
            </div>
        </template>
        <template #content>
            <slot />
        </template>
    </Card>
</template>
<script lang="js" setup>
import { defineComponent, defineProps } from 'vue';
import Card from 'primevue/card';
defineComponent({
    name: 'PageBase',
    components: {
        Card
    }
})

const props = defineProps({
    title: {
        type: String,
        required: true
    }
})

</script>
<style lang="css" scoped>
.page {
    padding: 1rem;
    margin: 1rem;

}

.title {
    display: flex;
    flex: 1;
    justify-content: center;
    align-items: center;

}

.title>h2 {
    color: #ffff;
    text-transform: capitalize;
}
</style>
<style>
.p-card-header {
    background-color: #314158;
    border-bottom: 1px solid #99A1AF;
    border-bottom-left-radius: 5px;
    border-bottom-right-radius: 5px;
}

.p-fileupload-basic-content {
    border: 1px solid #E6E6E6;
    padding: 10px;
    border-radius: 7px;
}
.p-fileupload-basic-content:hover {
    border-color: var(--p-green-500)
}
</style>
