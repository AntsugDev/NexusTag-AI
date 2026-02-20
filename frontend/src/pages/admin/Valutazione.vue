<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import Button from 'primevue/button'
import Rating from 'primevue/rating'
import Tag from 'primevue/tag'
import Fieldset from 'primevue/fieldset'
import api from '../../api/axios'
import { useToast } from 'primevue/usetoast'

const { t } = useI18n()
const route = useRoute()
const router = useRouter()
const toast = useToast()

const documentId = route.params.id
const documentName = route.query.name || 'Document'
const chunks = ref([])
const stats = ref({})
const loading = ref(false)
const evaluations = ref({}) // key: order, value: rating

const loadEvaluationData = async () => {
    loading.value = true
    try {
        const result = await api.get(`/api/valutazione/${documentId}`)
        const data = result.data.result
        chunks.value = data.chunks
        stats.value = data.stats

        // Initialize evaluations
        chunks.value.forEach(chunk => {
            evaluations.value[chunk.order] = null
        })
    } catch (error) {
        console.error('Error fetching evaluation data:', error)
        toast.add({
            severity: 'error',
            summary: t('common.error'),
            detail: 'Impossibile recuperare i dati per la valutazione',
            life: 3000
        })
    } finally {
        loading.value = false
    }
}

onMounted(() => {
    loadEvaluationData()
})

const isEvaluationComplete = computed(() => {
    return chunks.value.length > 0 &&
        chunks.value.every(chunk => evaluations.value[chunk.order] !== null)
})

const canSubmit = computed(() => {
    return chunks.value.length >= 10 && isEvaluationComplete.value
})

const getMarginSeverity = (deviation) => {
    const absDev = Math.abs(deviation)
    if (absDev < 50) return 'success'
    if (absDev < 150) return 'warning'
    return 'danger'
}

const getMarginLabel = (deviation) => {
    if (deviation > 0) return '+' + deviation
    return deviation
}

const submitEvaluation = () => {
    // This will be implemented later as requested
    toast.add({
        severity: 'info',
        summary: 'Info',
        detail: 'Funzionalità di invio valutazione non ancora implementata',
        life: 3000
    })
}

</script>

<template>
    <div class="admin-valutazione">
        <div class="page-header glass-panel p-4 flex justify-content-between align-items-center mb-5">
            <div class="flex align-items-center gap-4">
                <Button icon="pi pi-arrow-left" text rounded @click="router.back()" severity="secondary" />
                <h1 class="m-0 text-3xl font-black">{{ t('valutazione.title') }}</h1>
            </div>
            <div class="text-primary font-bold">File: {{ documentName }}</div>
        </div>

        <div v-if="Object.keys(stats).length > 0" class="flex flex-row align-items-center gap-4 data_general">
            <div class="stat-mini">
                <span class="label">{{ t('valutazione.total_chunks') }}</span>
                <span class="value">{{ stats.total_chunks }}</span>
            </div>
            <div class="stat-mini">
                <span class="label">{{ t('valutazione.avg_tokens') }}</span>
                <span class="value">{{ stats.avg_tokens }}</span>
            </div>
            <div class="stat-mini">
                <span class="label">{{ t('valutazione.total_tokens') }}</span>
                <span class="value">{{ stats.total_tokens }}</span>
            </div>
        </div>

        <div v-if="loading" class="flex justify-content-center p-8">
            <i class="pi pi-spin pi-spinner text-5xl text-primary"></i>
        </div>

        <div v-else class="evaluation-container pb-8">
            <Fieldset v-for="chunk in chunks" :key="chunk.order"
                class="evaluation-fieldset bg-white mb-6 shadow-2 border-2 border-200">
                <template #legend>
                    <div class="flex align-items-center gap-3 px-2">
                        <span class="order-badge">#{{ chunk.order }}</span>
                        <Tag :value="t('valutazione.tokens') + ': ' + chunk.token_count" severity="contrast" rounded
                            class="px-3 tag_token" />
                        <Tag :value="t('valutazione.deviation') + ': ' + getMarginLabel(chunk.deviation)"
                            :severity="chunk.deviation < 0 ? 'contrast' : getMarginSeverity(chunk.deviation)" rounded
                            :class="chunk.deviation < 0 ? ' px-3 tag_token_dev_red' : 'px-3 tag_token_dev_succ'" />
                    </div>
                </template>

                <div class="card-row flex gap-4 align-items-stretch">
                    <!-- Text Area (Full width) -->
                    <div class="flex-1">
                        <div class="content-text bg-gray-50 p-4 border-round-lg border-1 border-200 h-full">
                            <code>
                {{ chunk.content }}
            </code>
                        </div>
                    </div>

                    <!-- Evaluation Sidebar -->
                    <div
                        class="evaluation-sidebar flex flex-column align-items-center justify-content-center p-4 border-left-1 border-200 min-w-max bg-gray-50 border-round-right-lg">
                        <span class="text-xs font-bold text-500 mb-3 uppercase letter-spacing-2">{{
                            t('valutazione.rating') }}</span>
                        <div
                            class="rating-box p-3 border-round-xl bg-white border-2 border-200 shadow-1 hover:border-primary transition-colors">
                            <Rating v-model="evaluations[chunk.order]" :stars="5" :cancel="false">
                                <template #onicon>
                                    <i class="pi pi-star-fill text-yellow-500 text-3xl" />
                                </template>
                                <template #officon>
                                    <i class="pi pi-star text-300 text-3xl" />
                                </template>
                            </Rating>
                        </div>
                        <div class="mt-4 flex flex-column align-items-center">
                            <span v-if="evaluations[chunk.order]" class="text-2xl font-black text-primary">{{
                                evaluations[chunk.order]
                            }} <small class="text-400">/ 5</small></span>
                        </div>
                    </div>
                </div>
            </Fieldset>

            <!-- Detached Footer Summary (No background/border as requested) -->
            <div
                class="summary-footer-detached mt-8 p-4 flex justify-content-between align-items-center sticky bottom-2 z-5">
                <div
                    class="flex align-items-center gap-5 bg-white-transparent p-4 border-round-xl shadow-4 backdrop-blur">
                    <div class="footer-stat text-center">
                        <span class="text-500 text-xs font-bold uppercase block mb-1">{{ t('valutazione.rating')
                        }}</span>
                        <div class="flex align-items-baseline gap-1 " style="margin-bottom: 6px;">
                            <span class="text-4xl font-black text-primary ">
                                {{Object.values(evaluations).filter(v => v !== null).length}}
                            </span>
                            <span class="text-600 font-bold">/</span>
                            <span class="text-500 text-xl">{{ chunks.length }}</span>
                        </div>
                    </div>

                    <div v-if="isEvaluationComplete" style="margin-bottom: 15px;"
                        class="status-badge mb-4 flex align-items-center bg-green-500 text-white px-4 py-3 border-round-xl shadow-2">
                        <i class="pi pi-check-circle text-2xl mr-2" style="margin-right: 5px;margin-top:2px"></i>
                        <span class="font-bold text-lg">{{ t('valutazione.evaluation_ready') }}</span>
                    </div>

                    <div v-else style="margin-bottom: 15px;"
                        class="status-badge mb-4 flex align-items-center bg-gray-200 text-700 px-4 py-3 border-round-xl">
                        <i class="pi pi-info-circle text-xl mr-2" style="margin-right: 4px;margin-top:2px"></i>
                        <span class="font-medium">{{ t('valutazione.rating') }} (min. 10)</span>
                    </div>
                    <div class="flex gap-3">
                        <Button v-if="canSubmit" :label="t('valutazione.submit_evaluation')" icon="pi pi-send"
                            severity="success" raised class="p-submit-btn" @click="submitEvaluation" size="small" />
                    </div>
                </div>


            </div>
        </div>
    </div>
</template>

<style scoped>
.data_general {
    flex-direction: row;
    justify-content: space-between;
    display: flex;
    margin-bottom: 15px;
    padding: 10px;
    border-radius: 10px;
    background-color: #f5f5f5;
    color: #000;
}

code {
    font-size: 12px;
    text-align: justify;
    flex-wrap: wrap;
}

.admin-valutazione {
    padding: 1rem 0 2rem 0;
}

.page-header {
    border-radius: 16px;
    border: 1px solid rgba(var(--primary-rgb), 0.1);
    padding: 5px;
    gap: 10px;
    margin-bottom: 15px;
}

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

/* Fieldset Evaluation */
.evaluation-fieldset {
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    border: 2px solid #e2e8f0 !important;
    border-radius: 5px !important;
    overflow: visible;
    /* Legend needs to overflow slightly */
    padding: 0 !important;
    /* Content will have its own padding */
    margin-top: 30px;
    margin-bottom: 30px;
    background-color: #eee !important;
}

.tag_token {
    background-color: #1447E6 !important;
    color: #fff !important;
    padding: 5px;
}

.tag_token_dev_red {
    background-color: #EC253F !important;
    color: #fff !important;
    padding: 5px;
}

.tag_token_dev_succ {
    background-color: #178236 !important;
    color: #fff !important;
    padding: 5px;
}


.evaluation-fieldset:hover {
    border-color: var(--primary-color) !important;
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15) !important;
}

:deep(.p-fieldset-legend) {
    background: transparent !important;
    border: none !important;
    padding: 0 0.5rem !important;
}

:deep(.p-fieldset-content) {
    padding: 0 !important;
}

.order-badge {
    background-color: #62748E;
    color: white;
    padding: 5px;
    border-radius: 10px;
    font-weight: 800;
    font-size: 1.1rem;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    margin-right: 5px;
}

.content-text {
    line-height: 1.7;
    color: #334155;
    font-size: 1.1rem;
    word-break: break-word;
    border-bottom: 1px solid #000 !important;
    padding: 10px;
    margin-bottom: 20px;
}

.evaluation-sidebar {
    color: #fff;
    margin: 5px 5px;
    background-color: #62748E;
    padding: 10px;
    text-align: center;
}

.rating-box {
    transition: all 0.3s ease;
}

.min-w-max {
    min-width: 320px;
}

/* Detached Footer Summary */
.summary-footer-detached {
    pointer-events: none;
    padding: 10px;
}

.summary-footer-detached>* {
    pointer-events: auto;
}

.bg-white-transparent {
    background: rgba(255, 255, 255, 0.7);
}

.backdrop-blur {
    backdrop-filter: blur(16px);
    border: 1px solid rgba(255, 255, 255, 0.4);
    padding: 10px;
}

.p-submit-btn {
    padding: 1rem 3rem !important;
    font-size: 1.25rem !important;
    font-weight: 800 !important;
    border-radius: 16px !important;
    box-shadow: 0 10px 20px rgba(34, 197, 94, 0.3) !important;
}

.letter-spacing-2 {
    letter-spacing: 0.1em;
}

@media (max-width: 1200px) {
    .card-row {
        flex-direction: column;
    }

    .evaluation-sidebar {
        width: 100%;
        border-left: none !important;
        border-top: 2px solid #f1f5f9 !important;
        min-width: 100%;
        padding: 2rem !important;
    }

    .page-header {
        flex-direction: column;
        align-items: flex-start !important;
        gap: 1.5rem;
    }

    .page-header .flex.gap-4 {
        border-left: none !important;
        padding-left: 0 !important;
        width: 100%;
        justify-content: space-between;
    }
}
</style>
