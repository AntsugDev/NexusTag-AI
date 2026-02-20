<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { useAuthStore } from '../store/auth'
import { useSchedulerStore } from '../store/scheduler'
import Menubar from 'primevue/menubar'
import Button from 'primevue/button'
import { onMounted } from 'vue'

const { t, locale } = useI18n()
const auth = useAuthStore()
const schedulerStore = useSchedulerStore()
const router = useRouter()

onMounted(() => {
    schedulerStore.startPolling()
})


const items = computed(() => {
    const baseItems = [
        {
            label: t('menu.home'),
            icon: 'pi pi-home',
            command: () => router.push({ name: 'Home' })
        }
    ]

    if (auth.isAdmin) {
        baseItems.push({
            label: t('menu.upload'),
            icon: 'pi pi-upload',
            command: () => router.push({ name: 'Upload' })
        })
        baseItems.push({
            label: t('menu.list'),
            icon: 'pi pi-list',
            command: () => router.push({ name: 'Admin' })
        })
        baseItems.push({
            label: t('menu.failed'),
            icon: 'pi pi-exclamation-circle',
            command: () => router.push({ name: 'FailedJobs' })
        })
    } else {

        baseItems.push({
            label: t('menu.upload'),
            icon: 'pi pi-upload',
            command: () => router.push({ name: 'Upload' })
        })
        baseItems.push({
            label: t('menu.list'),
            icon: 'pi pi-list',
            command: () => router.push({ name: 'User' })
        })
    }

    return baseItems
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
        <Menubar :model="items" class="layout-menubar glass-panel">
            <template #start>
                <div class="logo">
                    <span class="logo-text">NexusTag <span class="ai-tag">AI</span></span>
                </div>
            </template>
            <template #end>
                <div class="user-actions">
                    <div v-if="auth.isAdmin && schedulerStore.info" class="scheduler-badge"
                        :class="{ 'is-running': schedulerStore.isRunning, 'is-waiting': !schedulerStore.isRunning }"
                        v-tooltip.bottom="schedulerStore.isRunning ? t('documents.scheduler_running') : t('documents.scheduler_remaining', { time: schedulerStore.formattedRemaining })">
                        <i v-if="schedulerStore.isRunning" class="pi pi-spin pi-spinner"></i>
                        <i v-else class="pi pi-clock"></i>
                        <span class="countdown-text">{{schedulerStore.isRunning ? t('documents.scheduler_text_running') : t('documents.scheduler_text_waiting')}}</span>
                    </div>

                    <Button :label="locale.toUpperCase()" icon="pi pi-globe" text @click="toggleLanguage"
                        class="lang-btn" />
                    <span v-if="auth.user" class="username">{{ auth.user.username }}</span>
                    <Button :label="t('common.logout')" icon="pi pi-sign-out" severity="danger" text
                        @click="handleLogout" />
                </div>
            </template>

        </Menubar>

        <main class="layout-content">
            <div class="content-container">
                <router-view />
            </div>
        </main>
    </div>
</template>

<style scoped>
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
    color: var(--text-primary);
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
