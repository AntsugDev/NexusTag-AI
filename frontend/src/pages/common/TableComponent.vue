<template>
    <template v-for="index in rows" :key="index" v-if="loading">
        <Skeleton shape="circle" size="4rem" class="mr-2"></Skeleton>
        <div class="self-center" style="flex: 1">
            <Skeleton width="100%" class="mb-2"></Skeleton>
            <Skeleton width="75%"></Skeleton>
        </div>
    </template>
    <DataTable :value="items" paginator :rows="setRows" :rowsPerPageOptions="optionsRows" :sortOrder="sortOrder"
        :sortField="sortField" layout="list" :totalRecords="totalRecords" :loading="loading" filterDisplay="row"
        :globalFilterFields="globalFilterFields">
        <template #header>
            <div class="content-header">
            <slot name="others"></slot>
            <IconsTable v-if="isRefresh" style="justify-content: end;" :icons="[
                {
                    class: 'pi pi-refresh',
                    action: () => {
                        emit('refresh')
                    },
                    color: '#C11007',
                    tooltip: 'Reload'
                }
            ]"></IconsTable>
            <span v-else></span>
</div>
        </template>
        <Column v-for="column, index in columns" :key="index" :header="column.label" :field="column.field"
            :sortable="column.sortable">
            <template #body="slotProps">
                <slot v-if="slots['content_' + column.field]" :name="getName(column.field, false)"
                    :item="slotProps.data"></slot>
                <span v-else>{{ slotProps.data[column.field] }}</span>
            </template>
        </Column>
        <template #empty>
            <div class="flex justify-center items-center" v-if="items.length === 0">
                <span>{{ t('common.table_empty') }}</span>
            </div>
        </template>


    </DataTable>


</template>
<script lang="js" setup>

import DataView from 'primevue/dataview';
import Row from 'primevue/row';
import Column from 'primevue/column';
import Skeleton from 'primevue/skeleton';
import { computed, defineComponent, useSlots } from 'vue';
import { useI18n } from 'vue-i18n'
import DataTable from 'primevue/datatable';
import IconsTable from './IconsTable.vue';

const slots = useSlots();

const { t } = useI18n()

const emit = defineEmits([
    'refresh'
])



defineComponent({
    name: 'TableComponent',
    components: {
        DataView,
        Skeleton,
        Row,
        Column,
        DataTable,
        IconsTable
    }
})

const getName = (field, isHeader) => {
    console.log(field, isHeader)
    return isHeader ? 'header_' + field : 'content_' + field
}

const props = defineProps({
    items: {
        Array,
        required: true
    },
    columns: {
        Array,
        required: false,
        default: []
    },
    sortField: {
        String,
        required: false
    },
    sortOrder: {
        Number,
        required: false
    },
    rows: {
        Number,
        required: false,
        default: 5
    },
    totalRecords: {
        Number,
        required: true,
    },
    loading: {
        Boolean,
        required: false,
        default: false
    },
    globalFilterFields: {
        Array,
        required: false,
        default: []
    },
    isRefresh: {
        Boolean,
        required: false,
        default: true
    },
    setAllRow: {
        Boolean,
        required: false,
        default: false
    }
})

const optionsRows = computed(() => {
    let options = [5, 10, 20, 50]
    if (props.setAllRow) {
        options.push(props.items.length)
        options = options.filter(e => e <= props.items.length)
    }

    return options
})

const setRows = computed(() => {
    if (props.setAllRow)
        return props.items.length
    else return props.rows

})

</script>
<style lang="css" scoped>
.content-header {
    display: flex;
    flex-direction: row;
    gap: 1rem;
    justify-content: space-between;
    align-content: center;
}

.div-list {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    justify-content: start;
    align-content: center;
}


.header-column {
    font-weight: 800;
    padding: 6px;
    min-width: 100px;
    max-width: 300px;
    align-content: center;
    text-transform: capitalize;
    color: #ffff;
}
</style>
<style>
.p-datatable-table-container {
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
}

.p-datatable-header-cell {
    background-color: #314158 !important;
    color: #ffff !important;
}

span[data-pc-section="sort"]>svg {
    color: #ffff !important;
}

.p-dataview-header {
    background-color: #314158 !important;
    border-bottom: 1px solid #99A1AF;
}

.p-row-even {
    background-color: #E2E8F0 !important;
}

.p-row-odd {
    background-color: #BEDBFF !important;
}
</style>