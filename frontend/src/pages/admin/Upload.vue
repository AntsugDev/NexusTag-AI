<script setup>
import { ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import FileUpload from 'primevue/fileupload'
import InputText from 'primevue/inputtext'
import Button from 'primevue/button'
import Message from 'primevue/message'
import Listbox from 'primevue/listbox'
import api from '../../api/axios'
import { useToast } from 'primevue/usetoast'
import PageBase from '../common/PageBase.vue'
import { Form } from '@primevue/forms';

const { t } = useI18n()
const router = useRouter()
const toast = useToast()

const topic = ref('')
const suggestions = ref([])
const showSuggestions = ref(false)
const selectedFile = ref(null)
const loading = ref(false)
const error = ref('')

const allowedExtensions = ['.txt', '.log', '.sql', '.csv', '.md', '.pdf', '.doc', '.docx', '.xls', '.xlsx']

const onFileSelect = (event) => {
    selectedFile.value = event.files[0]
}

const fetchSuggestions = async (val) => {
    if (val.length < 2) {
        suggestions.value = []
        showSuggestions.value = false
        return
    }

    try {
        const result = await api.get('/api/documents/suggest_topic', {
            params: { q: val }
        })
        suggestions.value = result.data.result
        showSuggestions.value = suggestions.value.length > 0
    } catch (e) {
        console.error('Error fetching suggestions', e)
    }
}

watch(topic, (newVal) => {
    fetchSuggestions(newVal)
})

const selectSuggestion = (val) => {
    topic.value = val
    showSuggestions.value = false
}

const handleUpload = async (event) => {
    if (!topic.value) {
        error.value = t('login.required')
        return
    }

    loading.value = true
    error.value = ''

    const formData = new FormData()
    formData.append('file', event.files[0])
    formData.append('argument', topic.value)

    try {
        await api.post('/api/documents/upload_file', formData, {
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        })
        toast.add({
            severity: 'success',
            summary: t('common.success'),
            detail: t('upload.successMsg'),
            life: 3000
        })
        router.push({ name: 'Admin' })
    } catch (e) {
        error.value = t('upload.errorMsg')
    } finally {
        loading.value = false
    }
}
</script>

<template>

    <PageBase :title="t('upload.title')">
        <template #default>
            <Form v-slot="$form" :initialValues :resolver @submit="handleUpload"
                class="flex flex-col gap-4 w-full sm:w-56">

                <div class="form-field">
                    <InputText v-model="topic" class="w-full p-inputtext-lg"
                        :placeholder="t('upload.topicPlaceholder')" />
                    <transition name="fade">
                        <div v-if="showSuggestions" class="suggestions-panel glass-panel">
                            <Listbox :options="suggestions" @change="e => selectSuggestion(e.value)"
                                class="border-none" />
                        </div>
                    </transition>
                </div>
                <div class="form-field">
                    <FileUpload mode="basic" name="file" :auto="false" :multiple="false"
                        :accept="allowedExtensions.join(',')"
                        :chooseLabel="t('common.search')"
                        :uploadLabel="t('upload.buttonLabel')" 
                        :cancelLabel="t('common.back')"
                         class="custom-fileupload"
                        :maxFileSize="10000000" :disabled="loading">
                        <template #empty>
                            <div class="flex flex-column align-items-center justify-content-center p-4">
                                <i class="pi pi-cloud-upload text-4xl mb-3 text-secondary"></i>
                                <p class="text-secondary">{{ t('upload.subtitle') }}</p>
                                <small class="text-secondary opacity-60">Max 10MB</small>
                            </div>
                        </template>
                    </FileUpload>
                </div>
                <div class="form-field-button">
                    <Button type="submit" :label="t('upload.buttonLabel')" severity="info" :loading="loading" />
                </div>
            </Form>
        </template>
    </PageBase>

    
</template>

<style scoped>
.admin-upload {
    padding: 1rem 0;
    max-width: 800px;
    margin: 0 auto;
}

.upload-container {
    padding: 2.5rem;
    border-radius: 20px;
}

.topic-input-wrapper {
    position: relative;
}

.suggestions-panel {
    position: absolute;
    top: 100%;
    left: 0;
    right: 0;
    z-index: 1000;
    margin-top: 0.5rem;
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
}

.custom-fileupload :deep(.p-fileupload-buttonbar) {
    background: transparent;
    border: none;
    padding: 1rem 0;
}

.custom-fileupload :deep(.p-fileupload-content) {
    background: rgba(255, 255, 255, 0.05);
    border: 2px dashed var(--glass-border);
    border-radius: 12px;
    padding: 2rem;
    text-align: center;
}

.page-header h1 {
    font-size: 2.25rem;
    font-weight: 900;
    margin-bottom: 0.5rem;
    letter-spacing: -1px;
}

.page-header p {
    color: var(--text-secondary);
    margin-bottom: 2rem;
}

.w-full {
    width: 100%;
}
</style>

<style>
.form-field {
    gap: 1rem;
    justify-content: center;
    align-items: center;
    margin-bottom: 10px;
}

.form-field-button {
    display: flex;
    flex-direction: row;
    gap: 1rem;
    justify-content: center;
    align-items: center;
    margin-bottom: 10px;
}
</style>
