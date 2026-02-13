<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { useAuthStore } from '../store/auth'
import Menubar from 'primevue/menubar'
import Button from 'primevue/button'

const { t, locale } = useI18n()
const auth = useAuthStore()
const router = useRouter()

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
