<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../store/auth'
import Card from 'primevue/card'
import InputText from 'primevue/inputtext'
import Password from 'primevue/password'
import Button from 'primevue/button'
import Message from 'primevue/message'

import api from '../api/axios'

const router = useRouter()
const auth = useAuthStore()

const username = ref('')
const password = ref('')
const loading = ref(false)
const error = ref('')

const handleLogin = async () => {
    if (!username.value || !password.value) {
        error.value = 'Username e password sono obbligatori'
        return
    }

    loading.value = true
    error.value = ''

    try {
        const result = await api.post('/api/user/login', {
            username: username.value,
            password: password.value
        })

        // result.data contains the response from server (which has message, time, result)
        const data = result.data.result
        auth.setAuth(data.access_token, { username: username.value })
        router.push({ name: 'Home' })
    } catch (e) {
        // Errors are already handled by interceptor (showing toast)
        // but we might want to show local feedback too
        error.value = 'Credenziali non valide o errore di connessione'
    } finally {
        loading.value = false
    }
}
</script>

<template>
    <div class="login-page">
        <div class="background-decor"></div>
        <Card class="login-card glass-panel">
            <template #header>
                <div class="login-header">
                    <h1>NexusTag <span class="primary">AI</span></h1>
                    <p>Inserisci le tue credenziali per accedere</p>
                </div>
            </template>
            <template #content>
                <form @submit.prevent="handleLogin" class="login-form">
                    <div class="field">
                        <label for="username">Username</label>
                        <InputText id="username" v-model="username" class="w-full"
                            :class="{ 'p-invalid': error && !username }" placeholder="admin" />
                    </div>
                    <div class="field">
                        <label for="password">Password</label>
                        <Password id="password" v-model="password" class="w-full" :toggleMask="true" :feedback="false"
                            :class="{ 'p-invalid': error && !password }" placeholder="••••••••" />
                    </div>

                    <transition name="fade">
                        <Message v-if="error" severity="error" class="mb-3">{{ error }}</Message>
                    </transition>

                    <Button type="submit" label="Login" icon="pi pi-sign-in" :loading="loading" class="w-full mt-2" />
                </form>
            </template>
        </Card>
    </div>
</template>

<style scoped>
.login-page {
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    position: relative;
    padding: 1.5rem;
    overflow-y: auto;
}

.background-decor {
    position: absolute;
    top: -25%;
    left: -25%;
    width: 150%;
    height: 150%;
    background: radial-gradient(circle at center, var(--primary-color) 0%, transparent 70%);
    opacity: 0.08;
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
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
    border-radius: 16px;
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
}

.login-header .primary {
    color: var(--primary-color);
}

.login-header p {
    color: var(--secondary-color);
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
    color: var(--dark-color);
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
