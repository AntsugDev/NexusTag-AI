<template>
    <DataView :value="item" paginator :rows="rows" :sortOrder="sortOrder" :sortField="sortField" layout="list">
        <template #header>
            <div class="flex justify-content-between">
                <Fluid>
                    <div class="header-column" v-for="column, index in columns" :key="index">
                        <span>{{ column }}</span>
                    </div>
                </Fluid>
            </div>
        </template>

        <template #list>
            <div class="div-list">

                <template v-for="index in rows" :key="index">
                    <Skeleton shape="circle" size="4rem" class="mr-2"></Skeleton>
                    <div class="self-center" style="flex: 1">
                        <Skeleton width="100%" class="mb-2"></Skeleton>
                        <Skeleton width="75%"></Skeleton>
                    </div>
                </template>

                <div class="flex flex-row">
                    <slot name="content" :items="items" />
                </div>


            </div>

        </template>
    </DataView>

</template>
<script lang="js" setup>

import DataView from 'primevue/dataview';
import Skeleton from 'primevue/skeleton';
import Fluid from 'primevue/fluid';


const props = defineProps({
    items: {
        Array,
        required: true
    },
    columns: {
        Array,
        required: true
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
    }
})

</script>
<style lang="css" scoped>
.div-list {
    display: flex;
    flex-direction: column;
    gap: 1rem;
}
.header-column{
    font-weight: 800;
    padding:6px;
}
</style>