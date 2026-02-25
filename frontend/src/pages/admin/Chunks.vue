<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import Tag from 'primevue/tag'
import { useAuthStore } from '../../store/auth'
import PageBase from '../common/PageBase.vue'
import api from '../../api/axios'
import TableComponent from '../common/TableComponent.vue'
import Editor from 'primevue/editor';

const { t } = useI18n()
const route = useRoute()
const router = useRouter()
const auth = useAuthStore()

const documentId = route.params.id
const fileName = ref(route.query.name || null)
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
        const result = await api.get(`/api/documents/documents/${documentId}/chunks`, {
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
    <PageBase :title="t('chunks.title', { fileName: fileName || `Document #${documentId}` })"
        :backRoute="documentId ? { name: t('documents.title'), to: 'Admin' } : null">

        <TableComponent :items="chunks" :columns="[
            {
                field: 'order_chunk',
                label: t('chunks.order'),
                sortable: true
            },
            {
                field: 'content',
                label: t('chunks.content'),
                sortable: true
            },
            {
                field: 'token_count',
                label: t('chunks.tokens'),
                sortable: true
            },
            {
                field: 'strategy_chunk_name',
                label: t('chunks.strategy'),
                sortable: false
            },
            {
                field: 'is_convert_embeded',
                label: t('chunks.embedded'),
                sortable: true
            }
        ]" @refresh="loadLazyData" :rows="rows" :totalRecords="totalRecords">
            <template #content_content="{ item }">
                <Editor :modelValue="item.content" :readonly="true">
                    <template v-slot:toolbar>
                        <span class="ql-formats">
                        </span>
                    </template>

                </Editor>
            </template>
            <template #content_order_chunk="{ item }">
                <strong>{{ parseInt(item.order_chunk) + 1 ?? item.order_chunk }}</strong>
            </template>
            <template #content_is_convert_embeded="{ item }">
                <Tag :value="item.is_convert_embeded !== 0 ? t('common.si') : t('common.no')"
                    :severity="item.is_convert_embeded !== 0 ? 'success' : 'danger'"></Tag>
            </template>

        </TableComponent>

    </PageBase>
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
    color: var(--text-secondary);
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
    background: rgba(0, 0, 0, 0.05);
    padding: 1rem;
    border-radius: 8px;
    font-size: 0.85rem;
    line-height: 1.6;
    max-height: 200px;
    overflow-y: auto;
    border: 1px solid var(--glass-border);
}

@media (prefers-color-scheme: dark) {
    .chunk-content {
        background: rgba(255, 255, 255, 0.05);
    }
}

.chunk-content code {
    white-space: pre-wrap;
    word-break: break-all;
    color: var(--text-primary);
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
