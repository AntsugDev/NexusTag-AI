<template>
    <Card class="page">
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
</style>
