<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import Button from 'primevue/button'
import InputText from 'primevue/inputtext'
import Tag from 'primevue/tag'
import { useAuthStore } from '../../store/auth'

import api from '../../api/axios'

const router = useRouter()
const auth = useAuthStore()

const documents = ref([])
const loading = ref(false)
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
        const result = await api.get('/api/admin/documents', {
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

const viewChunks = (id) => {
    router.push({ name: 'Chunks', params: { id } })
}

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
    <div class="admin-documents">
        <div class="page-header">
            <h1>Gestione Documenti</h1>
            <p>Visualizza e gestisci i documenti caricati nel sistema.</p>
        </div>

        <DataTable v-model:filters="filters" :value="documents" lazy paginator :rows="rows" :totalRecords="totalRecords"
            :loading="loading" @page="onPage($event)" class="glass-panel main-table" filterDisplay="menu"
            :globalFilterFields="['name_file', 'topic']" responsiveLayout="stack" breakpoint="960px">
            <template #header>
                <div class="table-header">
                    <span class="p-input-icon-left search-input">
                        <i class="pi pi-search" />
                        <InputText v-model="filters['global'].value" placeholder="Ricerca globale..." class="w-full" />
                    </span>
                    <Button icon="pi pi-refresh" rounded raised @click="loadLazyData()" />
                </div>
            </template>

            <Column field="id" header="ID" sortable class="id-column"></Column>
            <Column field="name_file" header="Nome File" sortable filter>
                <template #body="{ data }">
                    <span class="font-bold file-name">{{ data.name_file }}</span>
                </template>
            </Column>
            <Column field="topic" header="Argomento" sortable></Column>
            <Column field="status_file" header="Stato" sortable filter>
                <template #body="{ data }">
                    <Tag :value="data.status_file" :severity="getStatusSeverity(data.status_file)" class="status-tag" />
                </template>
            </Column>
            <Column field="size" header="Dimensione" class="hide-mobile">
                <template #body="{ data }">
                    {{ formatSize(data.size) }}
                </template>
            </Column>
            <Column field="created_at" header="Caricato il" sortable class="hide-mobile">
                <template #body="{ data }">
                    {{ new Date(data.created_at).toLocaleString() }}
                </template>
            </Column>
            <Column header="Azioni" class="actions-column">
                <template #body="{ data }">
                    <Button icon="pi pi-list" label="Chunks" severity="info" text raised rounded
                        @click="viewChunks(data.id)" />
                </template>
            </Column>

            <template #empty> Nessun documento trovato. </template>
        </DataTable>
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
    color: var(--secondary-color);
    font-size: 1.1rem;
}

.main-table {
    border: none;
    overflow: hidden;
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
