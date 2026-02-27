<template>
    <PageBase :title="t('listValutazioni.title')"
        :backRoute="documentId ? { name: t('documents.title'), to: 'Valutazione' } : null">
        <template #default>
            {{ items }}
            <div class="fieldset">
                <div class="stat-mini">
                    <span class="label"></span>
                    <span class="value"></span>
                </div>
            </div>

        </template>
    </PageBase>
</template>
<script lang="js" setup>
import { useI18n } from "vue-i18n";
import PageBase from "../common/PageBase.vue";
import { onBeforeMount, ref } from "vue";
import api from '../../api/axios'
import { useRoute } from "vue-router";
import Fieldset from 'primevue/fieldset';

const route = useRoute();
const { t } = useI18n();
const items = ref([])
const documentId = route.params.id;
onBeforeMount(() => {
})

</script>
<style scoped>

.stat-mini {
    display: flex;
    flex-direction: column;
    min-width: 100px;
}

.stat-mini .label {
    font-size: 0.75rem;
    color: var(--text-secondary);
    text-transform: uppercase;
    font-weight: 600;
}

.stat-mini .value {
    font-size: 1.25rem;
    font-weight: 800;
    color: var(--primary-color);
}
</style>