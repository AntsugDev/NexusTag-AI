<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import api from '../../api/axios'
import { useToast } from 'primevue/usetoast'
import PageBase from '../common/PageBase.vue'
import TableComponent from '../common/TableComponent.vue'
import Editor from 'primevue/editor';
import Badge from 'primevue/badge';
import Knob from 'primevue/knob';
import DialogCommon from '../common/DialogCommon.vue';
import Chart from 'primevue/chart';
import Tag from 'primevue/tag';
import Button from 'primevue/button';
import InputNumber from 'primevue/inputnumber';
import Fieldset from 'primevue/fieldset';

const { t } = useI18n()
const route = useRoute()
const router = useRouter()
const toast = useToast()

const documentId = route.params.id
const documentName = route.query.name || 'Document'
const chunks = ref([])
const stats = ref({})
const loading = ref(false)
const evaluations = ref({})
const showChart = ref(false)

const chartData = computed(() => {
    if (!chunks.value.length) return {}


    const barColors = chunks.value.map(chunk => {
        const deviation = chunk.deviation;
        if (deviation < 0) return '#C11007';
        if (deviation >= 10 && deviation <= 50) return '#53EAFD';
        return '#2AA63E';
    });

    return {
        labels: chunks.value.map(chunk => `#${chunk.order}`),
        datasets: [
            {
                type: 'bar',
                label: 'Tokens',
                data: chunks.value.map(chunk => chunk.deviation),
                backgroundColor: barColors,
                borderColor: barColors,
                borderWidth: 1,
                borderRadius: 1,
                order: 4,
            }
        ]
    }
})
const handleBarClick = (event) => {
    showChart.value = true
}


const chartOptions = computed(() => {
    return {
        indexAxis: 'x',
        maintainAspectRatio: false,
        aspectRatio: 0.8,
        plugins: {
            legend: {
                labels: {
                    usePointStyle: true,
                    font: {
                        family: 'Outfit, sans-serif',
                        weight: '700'
                    },
                    color: '#000'
                }
            },
            tooltip: {
                mode: 'index',
                intersect: false,
                padding: 12,
                backgroundColor: 'rgba(255, 255, 255, 0.9)',
                titleColor: '#1e293b',
                bodyColor: '#1e293b',
                borderColor: '#e2e8f0',
                borderWidth: 1,
                bodyFont: {
                    family: 'Outfit, sans-serif'
                },
                titleFont: {
                    family: 'Outfit, sans-serif',
                    weight: 'bold'
                }
            }
        },
        scales: {
            x: {
                ticks: {
                    font: {
                        family: 'Outfit, sans-serif'
                    }
                },
                grid: {
                    color: '#F1F5F9'
                }
            },
            y: {
                ticks: {
                    font: {
                        family: 'Outfit, sans-serif'
                    }
                },
                grid: {
                    display: true
                }
            }
        }
    }
})
const isReadonly = ref(false)
const evaluationsData = ref({})
const loadEvaluationData = async () => {
    loading.value = true
    try {
        const result = await api.get(`/api/valutazione/${documentId}`)
        const data = result.data.result
        chunks.value = data.chunks
        stats.value = data.stats
        evaluationsData.value = data.evaluations
        isReadonly.value = Object.entries(evaluationsData.value).length > 0
        chunks.value.forEach(chunk => {
            evaluations.value[chunk.id] = chunk.rating ?? 0
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
        chunks.value.every(chunk => evaluations.value[chunk.id] !== undefined && evaluations.value[chunk.id] !== null)
})

const canSubmit = computed(() => {
    return chunks.value.length >= 10 && isEvaluationComplete.value
})

const getMarginSeverity = (deviation) => {
    const absDev = parseInt(deviation)
    if (absDev < 0) return 'danger'
    else if (absDev > 0 && absDev < 50) return 'success'
    else if (absDev > 50) return 'warning'
    return 'info'
}

const getRangeTokenLabel = (deviation) => {
    if (deviation) return 'success'
    return 'danger'
}

const totalEvaluation = computed(() => {
    let sum = 0;
    for (const [key, value] of Object.entries(evaluations.value)) {
        let data_value = value ?? 0;
        sum += parseFloat(data_value);
    }
    return sum.toFixed(2)
})

const clearEvaluation = () => {
    Object.entries(evaluations.value).forEach(([key, value]) => {
        evaluations.value[key] = 0
    })
}

const setPonderato = (item) => {
    const token = item.token_count
    const ponderato = stats.value.total_tokens / parseInt(token)
    return {
        value: ponderato.toFixed(2)
    }

}
const showConfirm = ref(false)
const openDialogConfirm = () => {
    showConfirm.value = true
}
const submitEvaluation = async () => {

    try {
        const evalutation_for_row = []
        chunks.value.forEach(chunk => {
            evalutation_for_row.push({
                "chunk_id": chunk.id,
                "rating": evaluations.value[chunk.id] ?? 0
            })
        })

        const result = await api.post(`/api/valutazione`, {
            "document_id": parseInt(documentId),
            "total_chunks": parseInt(stats.value.total_chunks),
            "avg_tokens": parseInt(stats.value.avg_tokens),
            "total_token": parseInt(stats.value.total_tokens),
            "evalutation_for_row": evalutation_for_row,
            "total_evaluation": parseFloat(totalEvaluation.value).toFixed(2)
        })
        if (result.status === 201) {
            toast.add({
                severity: 'success',
                summary: t('common.success'),
                detail: t('valutazione.success'),
                life: 3000
            })
        }
    } catch (e) {
        console.error(e)
    }
}

const buildingEvaluation =async  () => {
        try {
            const response = await api.post('/api/valutazione/ask',{
                chunks:chunks.value
            });
            const data = response.data.result
            router.push({ name: 'ValutazioneEmbed', params: { id: documentId }, query: { d: btoa(JSON.stringify(data)) } })
        } catch (e) {
        }
}

const getColorScore = (score) => {
    if (parseFloat(score) >= 80) return 'color-score-high'
    else if (parseFloat(score) >= 50 && parseFloat(score) <= 79) return 'color-score-medium'
    else return 'color-score-low'
}
</script>

<template>
    <DialogCommon v-model:visible="showConfirm" :header="t('valutazione.confirm')">
        <template #default>
            <p>{{ t('valutazione.confirm_msg', { fileName: documentName }) }}</p>
        </template>
        <template #footer>
            <div style="display: flex; justify-content: flex-end; gap: 10px;">
                <Button :label="t('common.no')" severity="primary" @click="showConfirm = false" />
                <Button :label="t('common.si')" severity="danger" @click="submitEvaluation" />
            </div>
        </template>
    </DialogCommon>
    <PageBase :title="t('valutazione.title', { fileName: documentName || `Document #${documentId}` })"
        :backRoute="documentId ? { name: t('documents.title'), to: 'Admin' } : null">

        <DialogCommon :header="t('valutazione.chart_title')" v-model:visible="showChart">
            <template #default>
                <Chart type="bar" :data="chartData" :options="chartOptions" class="w-full h-full" />
            </template>

        </DialogCommon>
        <div class="fieldset">
            <div class="stat-mini">
                <span class="label">{{ t('valutazione.total_chunks') }}</span>
                <span class="value">{{ stats.total_chunks }}</span>
            </div>
            <div class="stat-mini">
                <span class="label">{{ t('valutazione.avg_tokens') }}</span>
                <span class="value">{{ stats.avg_tokens }}</span>
            </div>
            <div class="stat-mini">
                <span class="label">{{ t('valutazione.min_token', { min_token: stats.min_token }) }}</span>
                <span class="value">{{ stats.min_token }}</span>
            </div>
            <div class="stat-mini">
                <span class="label">{{ t('valutazione.max_token', { max_token: stats.max_token }) }}</span>
                <span class="value">{{ stats.max_token }}</span>
            </div>
            <div class="stat-mini">
                <span class="label">{{ t('valutazione.total_tokens') }}</span>
                <span class="value">{{ stats.total_tokens }}</span>
            </div>
            <div class="stat-mini" v-if="isReadonly">
                <span class="label">{{ t('listValutazioni.score') }}</span>
                <span :class="'value ' + getColorScore(evaluationsData.score)">{{ evaluationsData.score.toFixed(2)
                }}</span>
            </div>
        </div>
        <TableComponent @refresh="loadEvaluationData" :setAllRow="true" :items="chunks" :columns="[
            {
                field: 'order',
                label: t('chunks.order'),
                sortable: false
            },
            {
                field: 'content',
                label: t('chunks.content'),
                sortable: false
            },
            {
                field: 'deviation',
                label: t('valutazione.deviation'),
                sortable: true
            },
            {
                field: 'range_token',
                label: t('valutazione.range_token'),
                sortable: false
            },
            {
                field: 'token_count',
                label: t('chunks.tokens'),
                sortable: true
            },
            {
                field: 'rating',
                label: t('valutazione.rating'),
                sortable: true
            },

        ]">
            <template #changed>
                <div class="footer">
                    <span><strong>{{ t('valutazione.valutation_total') }}</strong>:</span>
                    <Tag :value="totalEvaluation" severity="info" icon="pi pi-calculator"></Tag>
                    <template v-if="!isReadonly">
                        <i class="pi pi-send" @click="openDialogConfirm"
                            v-tooltip.bottom="t('valutazione.submit_evaluation')"
                            style="color: #05DF72;margin-top:10px"></i>
                        <i class="pi pi-trash" @click="clearEvaluation"
                            v-tooltip.bottom="t('valutazione.clear_evaluation')"
                            style="color: #E7180B;margin-top:10px;margin-left: 10px;"></i>
                    </template>
                </div>
            </template>
            <template #others>
                <i class="pi pi-chart-bar" style="font-size: 1rem;cursor: pointer;"
                    v-tooltip.bottom="t('valutazione.view_chart')" @click="handleBarClick"></i>
                <i class="pi pi-building" style="font-size: 1rem;cursor: pointer;"
                    v-tooltip.bottom="t('listValutazioni.building')" @click="buildingEvaluation"></i>
            </template>
            <template #content_content="{ item }">
                <Editor :modelValue="item.content" :readonly="true">
                    <template v-slot:toolbar>
                        <span class="ql-formats">
                        </span>
                    </template>

                </Editor>
            </template>
            <template #content_deviation="{ item }">
                <Badge :value="item.deviation" :severity="getMarginSeverity(item.deviation)"></Badge>
            </template>
            <template #content_token_count="{ item }">
                {{ item.token_count }}
            </template>
            <template #content_rating="{ item }">

                <InputNumber v-if="!isReadonly" v-model="evaluations[item.id]" :min="0" :max="5" :maxFractionDigits="5"
                    fluid showButtons buttonLayout="vertical" size="small"></InputNumber>
                <Tag v-else :value="evaluations[item.id]" severity="info"></Tag>
            </template>
            <template #content_range_token="{ item }">
                <Badge value=" " :severity="getRangeTokenLabel(item.range_token)"></Badge>
            </template>
            <template #content_ponderato="{ item }">
                <Button icon="pi pi-percentage" disabled iconPos="right" :label="setPonderato(item)?.value ?? 0"
                    severity="info"></Button>
            </template>
        </TableComponent>

    </PageBase>

</template>
<style>
.fieldset {
    border: 1px solid #99A1AF;
    border-radius: 5px;
    padding: 10px;
    margin-bottom: 15px;
    background-color: #eee;
    display: flex;
    flex-direction: row;
    gap: 10px;
    justify-content: space-between;
}
</style>

<style scoped>
.h-full {
    min-height: 400px;
}

.footer {
    display: flex;
    flex-direction: row;
    justify-content: flex-end;
    align-content: center;
}

.footer span {
    margin-top: 4px;
    margin-right: 19px;
}



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

.p-dialog-content-cust {
    background-color: #fff !important;
}

.color-score-low {
    color: #E7180B !important;
}

.color-score-medium {
    color: #FE9A37 !important;
}

.color-score-high {
    color: #2AA63E !important;
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
