<script setup>
import { computed, ref, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { useAuthStore } from '../store/auth'
import { useSchedulerStore } from '../store/scheduler'
import Dock from 'primevue/dock'
import { onMounted } from 'vue'
import { useToast } from "primevue/usetoast";
import Badge from 'primevue/badge'

const { t, locale } = useI18n()
const auth = useAuthStore()
const schedulerStore = useSchedulerStore()
const router = useRouter()
const route = useRoute()

onMounted(() => {
    console.log(route)
    schedulerStore.startPolling()
})



const items = computed(() => {
    const baseItems = [];
    const lang = t('common.switch',{lang:locale.value === 'it' ? 'Inglese' : 'Italian'})
    baseItems.push({
        label: lang,
        icon: 'pi pi-globe',
        action: () => {
            toggleLanguage()
        }
    })

    baseItems.push({
        label: t('menu.scheduler'),
        icon: 'pi pi-clock',
    })

    baseItems.push({
        label: t('menu.home'),
        icon: 'pi pi-home',
        command: 'Home'
    })
    baseItems.push({
        label: t('menu.upload'),
        icon: 'pi pi-upload',
        command: 'Upload'
    })
    baseItems.push({
        label: t('menu.list'),
        icon: 'pi pi-list',
        command: 'Admin'
    })
    baseItems.push({
        label: t('menu.failed'),
        icon: 'pi pi-exclamation-circle',
        command: 'FailedJobs'
    })
    baseItems.push({
        label: t('menu.logout'),
        icon: 'pi pi-sign-out',
        command: null,
        action: () => {
            handleLogout()
        }
    })
    const switch_route_name = {
        'Home': t('menu.home'),
        'Upload': t('menu.upload'),
        'Admin': t('menu.list'),
        'FailedJobs': t('menu.failed'),
    }

    const filter = baseItems.filter(item => item.label !== switch_route_name[route.name] ?? null)
    return filter
})

const messageComputed = computed(() => {
    let message = {
        text: null,
        severity: 'warn'
    }
    if (!schedulerStore.isRunning) {
        message = {
            text: t('documents.scheduler_text_waiting'),
            severity: 'warn'
        }
    } else {
        message = {
            text: t('documents.scheduler_text_running'),
            severity: 'success'
        }
    }
    return message
})


const toggleLanguage = () => {
    locale.value = locale.value === 'it' ? 'en' : 'it'
}

const handleLogout = () => {
    auth.logout()
    router.push({ name: 'Login' })
}

</script>

<template>
    <div class="layout-wrapper">
        <Dock :model="items" position="left" class="dock">
            <template #itemicon="{ item }">
                <router-link :to="{ name: item.command }" v-tooltip="item.label" v-if="item.command">
                    <i :class="item.icon"></i>
                </router-link>
                <i :class="item.icon + (item.label === 'Logout' ? ' i-logout' : ' i-globe')" v-tooltip="item.label"
                    v-else-if="item.action" @click="item.action"></i>
                <i :class="item.icon + (messageComputed.severity === 'warn' ? ' btn_wait' : ' btn_running')" v-else
                    v-tooltip="messageComputed.text"></i>
            </template>

        </Dock>

        <main class="layout-content">
            <div class="content-container">
                <router-view />
            </div>
        </main>
    </div>
</template>

<style scoped>
a>button {
    width: 78%;
    height: 80%;
    border-radius: 30px;
}

.i-logout{
    color: #C11007!important;
    cursor: pointer;
}
.i-globe{
    color: #155DFC!important;
    cursor: pointer;
}

.btn_wait {
    background-color: #FE9A37;
    border-color: #FE9A37;
}

.btn_running {
    background-color: #31C950;
    border-color: #31C950;
}

.layout-wrapper {
    display: flex;
    flex-direction: column;
    min-height: 100vh;
    background-color: var(--light-color);
}

.layout-menubar {
    margin: 1rem;
    border-radius: 12px;
    padding: 0.5rem 1rem;
    border: none;
}

.logo {
    display: flex;
    align-items: center;
    margin-right: 1rem;
}

.logo-text {
    font-size: 1.25rem;
    font-weight: 800;
    letter-spacing: -0.5px;
    white-space: nowrap;
}

.ai-tag {
    color: var(--primary-color);
}

.user-actions {
    display: flex;
    align-items: center;
    gap: 0.75rem;
}

.scheduler-badge {
    display: flex;
    align-items: center;
    gap: 0.4rem;
    padding: 0.3rem 0.6rem;
    background: rgba(var(--primary-color-rgb, 0, 123, 255), 0.1);
    border-radius: 20px;
    font-size: 0.85rem;
    color: var(--text-secondary);
    border: 1px solid rgba(var(--primary-color-rgb, 0, 123, 255), 0.1);
}

.scheduler-badge.is-running {
    color: #fff;
    background: #31C950;
    border-color: #31C950;
}

.countdown-text {
    font-weight: 700;
    font-family: monospace;
}

.scheduler-badge.is-waiting {
    color: #fff;
    background: #F54927;
    border-color: #F54927;
}

.username {

    font-weight: 600;
    color: var(--text-secondary);
    font-size: 0.9rem;
    max-width: 100px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.layout-content {
    flex: 1;
    padding-bottom: 2rem;
}

.dock {
    margin-left: 10px;
    margin-right: 10px;
    background-color: #ffffff;
}

/* Mobile specific overrides */
@media (max-width: 768px) {
    .layout-menubar {
        margin: 0.5rem;
        padding: 0.25rem 0.5rem;
    }

    .username {
        display: none;
    }

    .logo-text {
        font-size: 1.1rem;
    }
}
</style>
