<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import Button from 'primevue/button'
import InputText from 'primevue/inputtext'
import Tag from 'primevue/tag'
import BlockUI from 'primevue/blockui'
import ProgressBar from 'primevue/progressbar'
import Dialog from 'primevue/dialog'
import { useAuthStore } from '../../store/auth'

import api from '../../api/axios'
import { useToast } from 'primevue/usetoast'

const { t } = useI18n()
const router = useRouter()
const auth = useAuthStore()
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
            // Schedula il prossimo controllo tra 2 secondi
            setTimeout(() => pollStatus(id), 2000)
        }
    } catch (e) {
        console.error('Error polling status:', e)
        isProcessing.value = false
    }
}

// La funzione processDocument è stata rimossa perché l'elaborazione è ora gestita esclusivamente via scheduler


const getStatusSeverity = (status) => {
    switch (status) {
        case 'processed': return 'success'
        case 'pending': return 'warning'
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
    <div class="admin-documents">
        <BlockUI :blocked="isProcessing" fullScreen>
            <div v-if="isProcessing" class="processing-overlay">
                <div class="processing-content glass-panel">
                    <i class="pi pi-cog pi-spin text-4xl mb-3 text-primary"></i>
                    <h3>Elaborazione in corso...</h3>
                    <p class="text-secondary mb-4">Stiamo analizzando il documento e creando i chunk.</p>
                    <ProgressBar mode="indeterminate" style="height: 6px"></ProgressBar>
                </div>
            </div>
        </BlockUI>

        <div class="page-header">
            <h1>{{ t('documents.title') }}</h1>
            <p>{{ t('documents.subtitle') }}</p>
        </div>

        <DataTable v-model:filters="filters" :value="documents" lazy paginator :rows="rows" :totalRecords="totalRecords"
            :loading="loading" @page="onPage($event)" class="glass-panel main-table" filterDisplay="menu"
            :globalFilterFields="['name_file', 'topic']" responsiveLayout="stack" breakpoint="960px">
            <template #header>
                <div class="table-header">
                    <span class="p-icon-field search-input">
                        <i class="pi pi-search p-input-icon" />
                        <InputText v-model="filters['global'].value" :placeholder="t('common.search')" />
                    </span>
                    <Button icon="pi pi-refresh" rounded raised @click="loadLazyData()"
                        v-tooltip.top="t('common.refresh')" />
                </div>
            </template>

            <Column field="id" header="ID" sortable class="id-column"></Column>
            <Column field="name_file" :header="t('documents.name')" sortable filter>
                <template #body="{ data }">
                    <span class="font-bold file-name">{{ data.name_file }}</span>
                </template>
            </Column>
            <Column field="topic" :header="t('upload.topicLabel')" sortable></Column>
            <Column field="status_file" :header="t('documents.status')" sortable filter>
                <template #body="{ data }">
                    <Tag :value="t(`documents.status_${data.status_file}`)"
                        :severity="getStatusSeverity(data.status_file)" class="status-tag" />
                </template>
            </Column>
            <Column field="size" :header="t('documents.size')" class="hide-mobile">
                <template #body="{ data }">
                    {{ formatSize(data.size) }}
                </template>
            </Column>
            <Column field="created_at" :header="t('documents.date')" sortable class="hide-mobile">
                <template #body="{ data }">
                    {{ new Date(data.created_at).toLocaleString() }}
                </template>
            </Column>
            <Column :header="t('common.actions')" class="actions-column">
                <template #body="{ data }">
                    <div class="flex justify-content-center gap-2">
                        <Button v-if="data.status_file === 'processed'" icon="pi pi-list" severity="info" text raised
                            rounded @click="viewChunks(data)" v-tooltip.top="t('common.viewChunks')" />

                        <Button v-if="data.status_file === 'pending'" icon="pi pi-spin pi-spinner" severity="warning"
                            text raised rounded disabled v-tooltip.top="t('documents.status_pending')" />

                        <Button v-if="data.status_file === 'error'" icon="pi pi-exclamation-triangle" severity="warning"
                            text raised rounded @click="viewError(data.id)" v-tooltip.top="t('common.viewError')" />
                    </div>
                </template>
            </Column>

            <template #empty> {{ t('common.noData') }} </template>
        </DataTable>

        <Dialog v-model:visible="showErrorDialog" modal :header="t('errorDialog.title')" :style="{ width: '50vw' }"
            :breakpoints="{ '1199px': '75vw', '575px': '90vw' }">
            <div class="error-detail-content">
                <i class="pi pi-times-circle text-danger text-4xl mb-3"></i>
                <p class="mb-4">{{ t('errorDialog.message') }}</p>
                <div class="error-msg-box glass-panel p-4 text-left font-mono">
                    {{ errorMessage }}
                </div>
            </div>
            <template #footer>
                <Button label="OK" icon="pi pi-check" @click="showErrorDialog = false" autofocus />
            </template>
        </Dialog>
    </div>
</template>

<style scoped>
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

.justify-content-between {
    justify-content: space-between;
}

.align-items-center {
    align-items: center;
}

.w-full {
    width: 100%;
}
</style>
