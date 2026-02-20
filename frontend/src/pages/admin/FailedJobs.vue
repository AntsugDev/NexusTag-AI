<script setup>
import { ref, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import Button from 'primevue/button'
import InputText from 'primevue/inputtext'
import Tag from 'primevue/tag'
import Dialog from 'primevue/dialog'
import api from '../../api/axios'

const { t } = useI18n()

const failedJobs = ref([])
const loading = ref(false)
const totalRecords = ref(0)
const rows = ref(10)
const filters = ref({
    global: { value: null, matchMode: 'contains' }
})

const showErrorDialog = ref(false)
const selectedError = ref('')

const loadLazyData = async (event) => {
    loading.value = true
    const page = event ? Math.floor(event.first / event.rows) + 1 : 1
    const limit = event ? event.rows : rows.value

    try {
        const result = await api.get('/api/jobs/failed', {
            params: {
                page: page,
                limit: limit
            }
        })


        const data = result.data.result
        failedJobs.value = data.items
        totalRecords.value = data.total
    } catch (error) {
        console.error('Error fetching failed jobs:', error)
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

const viewDetails = (exception) => {
    selectedError.value = exception
    showErrorDialog.value = true
}

const formatDate = (dateStr) => {
    if (!dateStr) return '-'
    return new Date(dateStr).toLocaleString()
}
</script>

<template>
    <div class="failed-jobs-page">
        <div class="page-header">
            <h1>{{ t('failedJobs.title') }}</h1>
            <p>{{ t('failedJobs.subtitle') }}</p>
        </div>

        <DataTable v-model:filters="filters" :value="failedJobs" lazy paginator :rows="rows"
            :totalRecords="totalRecords" :loading="loading" @page="onPage($event)" class="glass-panel main-table"
            filterDisplay="menu" responsiveLayout="stack" breakpoint="960px">

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

            <Column field="id" header="ID" class="id-column"></Column>
            <Column field="document_id" :header="t('failedJobs.doc_id')" sortable></Column>
            <Column field="row_id" :header="t('failedJobs.row_id')" sortable></Column>

            <Column field="exception" :header="t('failedJobs.exception')">
                <template #body="{ data }">
                    <div class="exception-cell" @click="viewDetails(data.exception)">
                        {{ data.exception }}
                    </div>
                </template>
            </Column>

            <Column field="created_at" :header="t('documents.date')" sortable>
                <template #body="{ data }">
                    {{ formatDate(data.created_at) }}
                </template>
            </Column>

            <template #empty> {{ t('common.noData') }} </template>
        </DataTable>

        <Dialog v-model:visible="showErrorDialog" modal :header="t('errorDialog.title')" :style="{ width: '50vw' }"
            :breakpoints="{ '1199px': '75vw', '575px': '90vw' }">
            <div class="error-detail-content">
                <i class="pi pi-times-circle text-danger text-4xl mb-3"></i>
                <div class="error-msg-box glass-panel p-4 text-left font-mono whitespace-pre-wrap">
                    {{ selectedError }}
                </div>
            </div>
            <template #footer>
                <Button label="OK" icon="pi pi-check" @click="showErrorDialog = false" autofocus />
            </template>
        </Dialog>
    </div>
</template>

<style scoped>
.failed-jobs-page {
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

.exception-cell {
    max-width: 300px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    cursor: pointer;
    color: var(--danger-color);
    font-family: monospace;
    font-size: 0.9rem;
}

.exception-cell:hover {
    text-decoration: underline;
}

.error-msg-box {
    background: rgba(220, 53, 69, 0.05);
    border: 1px solid rgba(220, 53, 69, 0.2);
    max-height: 400px;
    overflow-y: auto;
}

.whitespace-pre-wrap {
    white-space: pre-wrap;
}

@media (max-width: 960px) {
    .table-header {
        flex-direction: column;
        align-items: stretch;
    }

    .search-input {
        max-width: none;
    }
}
</style>
