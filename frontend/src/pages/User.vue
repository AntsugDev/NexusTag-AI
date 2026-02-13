<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import Button from 'primevue/button'
import Tag from 'primevue/tag'
import api from '../api/axios'

const { t } = useI18n()
const router = useRouter()

const documents = ref([])
const loading = ref(false)
const totalRecords = ref(0)
const rows = ref(10)

const loadLazyData = async (event) => {
    loading.value = true
    const page = event ? Math.floor(event.first / event.rows) + 1 : 1
    const limit = event ? event.rows : rows.value

    try {
        const result = await api.get('/api/user/documents', {
            params: { page, limit }
        })
        const data = result.data.result
        documents.value = data.items
        totalRecords.value = data.total
    } catch (error) {
        console.error('Error fetching user documents:', error)
    } finally {
        loading.value = false
    }
}

onMounted(() => loadLazyData())

const getStatusSeverity = (status) => {
    switch (status) {
        case 'processed': return 'success'
        case 'uploaded': return 'info'
        case 'error': return 'danger'
        default: return 'secondary'
    }
}

const formatSize = (bytes) => {
    if (!bytes) return '0 B'
    const k = 1024
    const sizes = ['B', 'KB', 'MB', 'GB']
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}
</script>

<template>
    <div class="user-documents">
        <div class="page-header flex justify-content-between align-items-center">
            <div>
                <h1>{{ t('documents.title') }}</h1>
                <p>{{ t('documents.subtitle') }}</p>
            </div>
            <Button :label="t('menu.upload')" icon="pi pi-upload" @click="router.push({ name: 'Upload' })" />
        </div>

        <DataTable :value="documents" lazy paginator :rows="rows" :totalRecords="totalRecords" :loading="loading"
            @page="loadLazyData($event)" class="glass-panel main-table" responsiveLayout="stack" breakpoint="960px">

            <Column field="name_file" :header="t('documents.name')">
                <template #body="{ data }">
                    <span class="font-bold file-name">{{ data.name_file }}</span>
                </template>
            </Column>
            <Column field="topic" :header="t('upload.topicLabel')"></Column>
            <Column field="status_file" :header="t('documents.status')">
                <template #body="{ data }">
                    <Tag :value="t(`documents.status_${data.status_file}`)"
                        :severity="getStatusSeverity(data.status_file)" />
                </template>
            </Column>
            <Column field="size" :header="t('documents.size')" class="hide-mobile">
                <template #body="{ data }">
                    {{ formatSize(data.size) }}
                </template>
            </Column>
            <Column field="created_at" :header="t('documents.date')" class="hide-mobile">
                <template #body="{ data }">
                    {{ new Date(data.created_at).toLocaleString() }}
                </template>
            </Column>

            <template #empty> {{ t('common.noData') }} </template>
        </DataTable>
    </div>
</template>

<style scoped>
.user-documents {
    padding: 1rem 0;
}

.page-header {
    margin-bottom: 2rem;
    padding: 0 0.5rem;
}

.page-header h1 {
    font-size: 2.25rem;
    font-weight: 900;
    margin-bottom: 0.5rem;
    letter-spacing: -1px;
}

.file-name {
    color: var(--primary-color);
}

@media (max-width: 960px) {
    .hide-mobile {
        display: none;
    }
}
</style>
