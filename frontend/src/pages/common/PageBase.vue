<template>
    <Card class="page glass-panel">
        <template #header>
            <div class="title">
                <i class="pi pi-arrow-left cursor-pointer mr-2" @click="back" :alt="computedBackRoute"
                    :title="computedBackRoute" v-if="backRoute?.to"></i>
                <h2>{{ title }}</h2>
            </div>
        </template>
        <template #content>
            <slot />
        </template>
    </Card>
</template>
<script lang="js" setup>
import { defineComponent, defineProps, computed } from 'vue';
import Card from 'primevue/card';
import { useRouter } from 'vue-router';
import { useI18n } from 'vue-i18n';
defineComponent({
    name: 'PageBase',
    components: {
        Card
    }
})
const { t } = useI18n()
const router = useRouter()
const props = defineProps({
    title: {
        type: String,
        required: true
    },
    backRoute: {
        type: String,
        required: false
    }
})
const computedBackRoute = computed(() => {
    if (props.backRoute?.name) return t('common.back', { backroute: props.backRoute?.name })
    return t('common.back')
})

const back = () => {
    if (props.backRoute?.to) router.push({ name: props.backRoute.to })
    else router.back()
}
</script>
<style lang="css" scoped>
.page {
    padding: 1rem;
    margin: 1rem;

}

.title {
    display: flex;
    flex: 1;
    flex-direction: row;
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
