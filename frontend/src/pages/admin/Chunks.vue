<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import Button from 'primevue/button'
import InputText from 'primevue/inputtext'
import Tag from 'primevue/tag'
import { useAuthStore } from '../../store/auth'

import api from '../../api/axios'

const route = useRoute()
const router = useRouter()
const auth = useAuthStore()

const documentId = route.params.id
const chunks = ref([])
const loading = ref(false)
const totalRecords = ref(0)
const rows = ref(10)
const filters = ref({
    global: { value: null, matchMode: 'contains' }
})

const loadLazyData = async (event) => {
    loading.value = true

    const page = event ? Math.floor(event.first / event.rows) + 1 : 1
    const limit = event ? event.rows : rows.value

    try {
        const result = await api.get(`/api/admin/documents/${documentId}/chunks`, {
            params: {
                page: page,
                limit: limit
            }
        })

        const data = result.data.result
        chunks.value = data.items
        totalRecords.value = data.total
    } catch (error) {
        console.error('Error fetching chunks:', error)
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

const goBack = () => {
    router.push({ name: 'Admin' })
}
</script>

<template>
    <div class="admin-chunks">
        <div class="page-header">
            <div class="flex align-items-center gap-3">
                <Button icon="pi pi-arrow-left" text rounded @click="goBack" />
                <h1>Chunk Documento #{{ documentId }}</h1>
            </div>
            <p>Visualizzazione dei segmenti (chunks) estratti dal documento.</p>
        </div>

        <DataTable v-model:filters="filters" :value="chunks" lazy paginator :rows="rows" :totalRecords="totalRecords"
            :loading="loading" @page="onPage($event)" class="glass-panel main-table" responsiveLayout="stack"
            breakpoint="960px">
            <template #header>
                <div class="table-header">
                    <span class="p-input-icon-left search-input">
                        <i class="pi pi-search" />
                        <InputText v-model="filters['global'].value" placeholder="Cerca nel contenuto..."
                            class="w-full" />
                    </span>
                    <Button icon="pi pi-refresh" rounded raised @click="loadLazyData()" />
                </div>
            </template>

            <Column field="order_chunk" header="#" class="order-column"></Column>
            <Column field="content" header="Contenuto">
                <template #body="{ data }">
                    <div class="chunk-content">
                        <code>{{ data.content }}</code>
                    </div>
                </template>
            </Column>
            <Column field="token_count" header="Token" class="hide-mobile"></Column>
            <Column field="strategy_chunk" header="Strategia" class="hide-mobile">
                <template #body="{ data }">
                    <Tag :value="data.strategy_chunk" severity="info" />
                </template>
            </Column>
            <Column field="is_convert_embeded" header="Embedded">
                <template #body="{ data }">
                    <Tag :value="data.is_convert_embeded ? 'Si' : 'No'"
                        :severity="data.is_convert_embeded ? 'success' : 'danger'" />
                </template>
            </Column>

            <template #empty> Nessun chunk trovato per questo documento. </template>
        </DataTable>
    </div>
</template>

<style scoped>
.admin-chunks {
    padding: 1rem 0;
}

.page-header {
    margin-bottom: 2rem;
    padding: 0 0.5rem;
}

.header-title-row {
    display: flex;
    align-items: center;
    gap: 1rem;
}

.page-header h1 {
    font-size: 2.25rem;
    font-weight: 900;
    margin: 0;
    letter-spacing: -1px;
}

.header-subtitle {
    color: var(--secondary-color);
    margin-top: 0.5rem;
    margin-left: 3.5rem;
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

.order-column {
    width: auto;
}

.chunk-content {
    background: rgba(0, 0, 0, 0.03);
    padding: 1rem;
    border-radius: 8px;
    font-size: 0.85rem;
    line-height: 1.6;
    max-height: 200px;
    overflow-y: auto;
    border: 1px solid rgba(0, 0, 0, 0.05);
}

.chunk-content code {
    white-space: pre-wrap;
    word-break: break-all;
    color: var(--dark-color);
}

@media (max-width: 960px) {
    .header-subtitle {
        margin-left: 0;
    }

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

    .order-column {
        width: auto;
    }
}

.w-full {
    width: 100%;
}
</style>
