<script setup>
import { useAuthStore } from '../store/auth'
import { useI18n } from 'vue-i18n'
import Card from 'primevue/card'

const { t } = useI18n()
const auth = useAuthStore()
</script>

<template>
    <div class="home-page">
        <Card class="welcome-card glass-panel">
            <template #content>
                <div class="welcome-content">
                    <i class="pi pi-sparkles welcome-icon"></i>
                    <h2>
                        {{ t('common.welcome') }} -
                        <span :class="auth.isAdmin ? 'role-admin' : 'role-user'">
                            {{ auth.isAdmin ? t('common.admin').toUpperCase() : t('common.user').toUpperCase() }}
                        </span>
                    </h2>
                    <p v-if="auth.isAdmin">
                        {{ t('home.admin_msg') }}
                    </p>
                    <p v-else>
                        {{ t('home.user_msg') }}
                    </p>
                </div>
            </template>
        </Card>
    </div>
</template>

<style scoped>
.home-page {
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 4rem 0;
}

.welcome-card {
    width: 100%;
    max-width: 800px;
    text-align: center;
    padding: 2rem;
}

.welcome-icon {
    font-size: 3rem;
    color: var(--primary-color);
    margin-bottom: 1.5rem;
}

.welcome-content h2 {
    font-size: 2.5rem;
    font-weight: 800;
    margin-bottom: 1rem;
}

.role-admin {
    color: var(--danger-color);
}

.role-user {
    color: var(--success-color);
}

.welcome-content p {
    font-size: 1.2rem;
    color: var(--secondary-color);
}
</style>
