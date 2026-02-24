<template>
    <template v-for="index in rows" :key="index" v-if="loading">
        <Skeleton shape="circle" size="4rem" class="mr-2"></Skeleton>
        <div class="self-center" style="flex: 1">
            <Skeleton width="100%" class="mb-2"></Skeleton>
            <Skeleton width="75%"></Skeleton>
        </div>
    </template>
    <DataView :value="item" paginator :rows="rows" :rowsPerPageOptions="[3, 10, 20, 50]" :sortOrder="sortOrder"
        :sortField="sortField" layout="list" :totalRecords="totalRecords" :loading="loading">
        <template #header>
            <div class="header">
                <div class="header-column" v-for="column, index in columns" :key="index">
                    <span v-if="column?.label">{{ column?.label }}</span>
                    <i v-if="column?.sortable" class="pi pi-sort-alt"></i>
                </div>
            </div>
        </template>
        <template #empty="slotProps">
            <div class="div-list">
               {{ t('common.table_empty') }}
            </div>
        </template>

        <template #list>
            <div class="div-list">
                <slot name="content" :items="items" />
            </div>

        </template>
    </DataView>

</template>
<script lang="js" setup>

import DataView from 'primevue/dataview';
import Skeleton from 'primevue/skeleton';
import { defineComponent } from 'vue';
import { useI18n } from 'vue-i18n'

const { t } = useI18n()

defineComponent({
    name: 'TableComponent',
    components: {
        DataView,
        Skeleton
    }
})

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
        default: 3
    },
    totalRecords: {
        Number,
        required: true,
    },
    loading: {
        Boolean,
        required: false,
        default: false
    }
})

</script>
<style lang="css" scoped>
.div-list {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    justify-content: start;
    align-content: center;
}

.header {
    display: flex;
    justify-content: space-between;
    flex: 1;

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
.p-dataview-header {
    background-color: #314158!important;
    border-bottom: 1px solid #99A1AF;
}
</style>