<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../store/auth'
import { useI18n } from 'vue-i18n'
import Card from 'primevue/card'
import InputText from 'primevue/inputtext'
import Password from 'primevue/password'
import Button from 'primevue/button'
import Message from 'primevue/message'

import api from '../api/axios'

const { t, locale } = useI18n()
const router = useRouter()
const auth = useAuthStore()

const username = ref('')
const password = ref('')
const loading = ref(false)
const error = ref('')

const toggleLanguage = () => {
    locale.value = locale.value === 'it' ? 'en' : 'it'
}

const handleLogin = async () => {
    if (!username.value || !password.value) {
        error.value = t('login.required')
        return
    }

    loading.value = true
    error.value = ''

    try {
        const result = await api.post('/api/user/login', {
            username: username.value,
            password: password.value
        })

        const data = result.data.result
        auth.setAuth(data.access_token, { username: username.value })
        router.push({ name: 'Home' })
    } catch (e) {
        error.value = t('login.invalid')
    } finally {
        loading.value = false
    }
}
</script>

<template>
    <div class="login-page">
        <div class="lang-switcher-login">
            <Button :label="locale.toUpperCase()" icon="pi pi-globe" text @click="toggleLanguage"
                severity="secondary" />
        </div>
        <div class="background-decor"></div>
        <Card class="login-card glass-panel">
            <template #header>
                <div class="login-header">
                    <h1>NexusTag <span class="primary">AI</span></h1>
                    <p>{{ t('login.subtitle') }}</p>
                </div>
            </template>
            <template #content>
                <form @submit.prevent="handleLogin" class="login-form">
                    <div class="field">
                        <label for="username">{{ t('login.username') }}</label>
                        <InputText id="username" v-model="username" class="w-full"
                            :class="{ 'p-invalid': error && !username }" placeholder="admin" />
                    </div>
                    <div class="field">
                        <label for="password">{{ t('login.password') }}</label>
                        <Password id="password" v-model="password" class="w-full" :toggleMask="true" :feedback="false"
                            :class="{ 'p-invalid': error && !password }" placeholder="••••••••" />
                    </div>

                    <transition name="fade">
                        <Message v-if="error" severity="error" class="mb-3">{{ error }}</Message>
                    </transition>

                    <Button type="submit" :label="t('login.submit')" icon="pi pi-sign-in" :loading="loading"
                        class="w-full mt-2" />
                </form>
            </template>
        </Card>
    </div>
</template>

<style scoped>
.lang-switcher-login {
    position: absolute;
    top: 1rem;
    right: 1rem;
    z-index: 10;
}

.login-page {
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    background: var(--light-color);
    position: relative;
    padding: 1.5rem;
    overflow-y: auto;
}

.login-page::before {
    content: '';
    position: absolute;
    inset: 0;
    background: linear-gradient(135deg, var(--primary-color) 0%, transparent 100%);
    opacity: 0.1;
    z-index: 0;
}

@media (prefers-color-scheme: dark) {
    .login-page::before {
        opacity: 0.2;
    }
}

.background-decor {
    position: absolute;
    top: -25%;
    left: -25%;
    width: 150%;
    height: 150%;
    background: radial-gradient(circle at center, var(--primary-color) 0%, transparent 70%);
    opacity: 0.12;
    z-index: 0;
    animation: rotate 30s linear infinite;
    pointer-events: none;
}

@keyframes rotate {
    from {
        transform: rotate(0deg);
    }

    to {
        transform: rotate(360deg);
    }
}

.login-card {
    width: 100%;
    max-width: 420px;
    z-index: 1;
    border-radius: 20px;
    border: none;
}

.login-header {
    padding: 2.5rem 2rem 1rem;
    text-align: center;
}

.login-header h1 {
    margin: 0;
    font-size: 2.25rem;
    font-weight: 900;
    letter-spacing: -1px;
    color: var(--text-primary);
}

.login-header .primary {
    color: var(--primary-color);
}

.login-header p {
    color: var(--text-secondary);
    margin-top: 0.75rem;
    font-size: 1rem;
}

.login-form {
    padding: 1.5rem 2rem 2.5rem;
}

.field {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    margin-bottom: 1.5rem;
}

.field label {
    font-weight: 700;
    color: var(--text-primary);
    font-size: 0.9rem;
}

.w-full {
    width: 100%;
}

@media (max-width: 480px) {
    .login-page {
        padding: 1rem;
    }

    .login-header h1 {
        font-size: 1.75rem;
    }

    .login-form {
        padding: 1rem 1.5rem 2rem;
    }
}
</style>
