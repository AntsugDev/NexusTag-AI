<script setup>
import { ref, onMounted, onUnmounted, watch, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import BlockUI from 'primevue/blockui'
import ProgressBar from 'primevue/progressbar'
import { useAuthStore } from '../../store/auth'
import { useSchedulerStore } from '../../store/scheduler'
import TableComponent from '../common/TableComponent.vue'
import PageBase from '../common/PageBase.vue'
import Tag from 'primevue/tag'
import Badge from 'primevue/badge'
import IconsTable from '../common/IconsTable.vue'
import api from '../../api/axios'
import { useToast } from 'primevue/usetoast'

const { t } = useI18n()
const router = useRouter()
const auth = useAuthStore()
const schedulerStore = useSchedulerStore()
const toast = useToast()

const documents = ref([])
const loading = ref(false)
const isProcessing = ref(false)
const showErrorDialog = ref(false)
const errorMessage = ref('')
const totalRecords = ref(0)
const rows = ref(10)
const first = ref(0)
const filters = ref({
    global: { value: null, matchMode: 'contains' },
    name_file: { value: null, matchMode: 'contains' },
    status_file: { value: null, matchMode: 'equals' }
})

// Auto-refresh lista quando lo scheduler parte
watch(() => schedulerStore.isRunning, (newValue, oldValue) => {
    if (newValue === true && oldValue === false) {
        console.log('Scheduler started, refreshing documents list...')
        loadLazyData()
    }
})


const loadLazyData = async (event) => {
    loading.value = true

    // Pagination params
    const page = event ? Math.floor(event.first / event.rows) + 1 : 1
    const limit = event ? event.rows : rows.value

    try {
        const result = await api.get('/api/documents/documents', {
            params: {
                page: page,
                limit: limit
            }
        })

        const data = result.data.result
        documents.value = data.items
        totalRecords.value = data.total
    } catch (error) {
        console.error('Error fetching documents:', error)
    } finally {
        loading.value = false
    }
}

onMounted(() => {
    loadLazyData()
    schedulerStore.startPolling()
})

onUnmounted(() => {
    // Optionally stop polling if you only want it on this page, 
    // but the user wants it global, so we might want to keep it running
    // or start it in App.vue instead.
})

const onPage = (event) => {
    loadLazyData(event)
}

const viewChunks = (data) => {
    router.push({
        name: 'Chunks',
        params: { id: data.id },
        query: { name: data.name_file }
    })
}

const viewEvaluation = (data) => {
    router.push({
        name: 'Valutazione',
        params: { id: data.id },
        query: { name: data.name_file }
    })
}

const viewError = async (id) => {
    try {
        const result = await api.get(`/api/jobs/job_failed/${id}/error`)
        errorMessage.value = result.data.result.error
        showErrorDialog.value = true

    } catch (e) {
        console.error('Error fetching error details:', e)
        toast.add({
            severity: 'error',
            summary: t('common.error'),
            detail: 'Impossibile recuperare i dettagli dell\'errore',
            life: 3000
        })
    }
}

const reprocessDocument = async (id) => {
    try {
        await api.delete(`/api/documents/rework/${id}`)
        loadLazyData()
        toast.add({
            severity: 'success',
            summary: t('common.success'),
            detail: t('documents.rework'),
            life: 3000
        })
    } catch (e) {
        console.error('Error fetching error details:', e)
        toast.add({
            severity: 'error',
            summary: t('common.error'),
            detail: 'Impossibile recuperare i dettagli dell\'errore',
            life: 3000
        })
    }
}

const pollStatus = async (id) => {
    try {
        const result = await api.get(`/api/documents/documents/${id}/status`)
        const status = result.data.result.status_file

        if (status === 'processed') {
            isProcessing.value = false
            toast.add({
                severity: 'success',
                summary: t('common.success'),
                detail: 'Elaborazione completata',
                life: 3000
            })
            loadLazyData()
        } else if (status === 'error') {
            isProcessing.value = false
            toast.add({
                severity: 'error',
                summary: t('common.error'),
                detail: 'Errore durante l\'elaborazione del documento',
                life: 3000
            })
            loadLazyData()
        } else {
            setTimeout(() => pollStatus(id), 2000)
        }
    } catch (e) {
        console.error('Error polling status:', e)
        isProcessing.value = false
    }
}

const getStatusSeverity = (status) => {
    switch (status) {
        case 'processed': return 'success'
        case 'pending': return 'warning'
        case 'uploaded': return 'info'
        case 'error':
        case 'reprocessed':
            return 'danger'
        default: return 'secondary'
    }
}
const formatDate = (date) => {
    return new Date(date).toLocaleDateString()
}

const formatSize = (bytes) => {
    if (!bytes) return '0 B'
    const k = 1024
    const sizes = ['B', 'KB', 'MB', 'GB']
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

const header = computed(() => {

    return [
        { label: t('documents.name'), sortable: true, field: 'name_file' },
        { label: t('documents.ext'), sortable: true, field: 'mime_type' },
        { label: t('documents.status'), sortable: true, field: 'status_file_name' },
        { label: t('documents.size'), sortable: true, field: 'size' },
        { label: t('documents.date'), sortable: true, field: 'created_at' },
        { label: t('documents.topic'), sortable: true, field: 'topic_name' },
        { label: t('documents.is_chunked'), sortable: true, field: 'is_chunked' },
        { label: t('common.actions_column'), sortable: false, field: 'actions' },
    ]

})

</script>

<template>
    <PageBase :title="t('documents.title')">
        <template #default>
            <TableComponent :items="documents" :columns="header" :rows="rows" :totalRecords="totalRecords" @refresh="loadLazyData"
                :loading="loading" :globalFilterFields="['name_file', 'status_file', 'topic_name']">
                
                <template #content_name_file="{ item }">
                    {{ item.name_file ? item.name_file.toString().split('.')[0] : "" }}
                </template>
                <template #content_status_file_name="{ item }">
                    <Tag :value="item.status_file_name" :severity="getStatusSeverity(item.status_file_name)"></Tag>
                </template>

                <template #content_created_at="{ item }">
                    {{ formatDate(item.created_at) }}
                </template>

                <template #content_size="{ item }">
                    {{ formatSize(item.size) }}
                </template>
                 <template #content_is_chunked="{ item }">
                    <Badge :severity="item.is_chunked ? 'success' : 'danger'" size="xlarge" v-tooltip="item.is_chunked ? t('documents.text_chunked') : t('documents.text_not_chunked')"></Badge>
                </template>
                <template #content_actions="{item}">
                    <IconsTable v-if="item.status_file_name !== 'uploaded'" :icons="[
                        {
                            class: 'pi pi-eye',
                            action: () => viewChunks(item),
                            color: '#178236',
                            tooltip: t('documents.view_chunks'),
                            is_view: item.status_file_name === 'processed'
                        },
                        {
                            class: 'pi pi-chart-bar',
                            action: () => viewEvaluation(item),
                            color: '#314158',
                            tooltip: t('documents.view_evaluation'),
                            is_view: item.status_file_name === 'processed'
                        },
                        {
                            class: 'pi pi-trash',
                            action: () => deleteDocument(item.id),
                            color: '#9F0712',
                            tooltip: t('documents.delete'),
                            is_view: item.status_file_name === 'reprocessed' || item.status_file === 'error'
                        }
                    ]"></IconsTable>
                </template>
            </TableComponent>
        </template>
    </PageBase>
</template>

<style scoped>
.list {
    display: flex;
    flex-direction: row;
    gap: 1rem;
    justify-content: start;
    align-content: center;
    padding: 5px;
    margin: 5px;
    border-radius: 5px;
    background-color: var(--surface-ground);
    border-bottom: 1px solid var(--surface-border);
}

.admin-documents {
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

.page-header p {
    color: var(--text-secondary);
    font-size: 1.1rem;
}

.italic {

    font-style: italic;
}

.line-height-1 {
    line-height: 1.2;
}

.main-table {
    border: none;
}


.table-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 1rem;
    padding: 0.5rem;
}

.search-input {
    flex: 1;
    max-width: 400px;
}

.id-column {
    width: 5rem;
}

.file-name {
    color: var(--primary-color);
}

.processing-overlay {
    position: fixed;
    inset: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
    pointer-events: none;
}

.processing-content {
    width: 100%;
    max-width: 400px;
    padding: 3rem;
    text-align: center;
    pointer-events: auto;
}

.actions-column {
    width: 10rem;
    text-align: center;
}

@media (max-width: 960px) {

    .id-column,
    .hide-mobile {
        display: none;
    }

    .table-header {
        flex-direction: column;
        align-items: stretch;
    }

    .search-input {
        max-width: none;
    }

    .actions-column {
        width: 100%;
        text-align: left;
    }
}
</style>
