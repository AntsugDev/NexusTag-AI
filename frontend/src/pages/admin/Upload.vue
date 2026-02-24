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
import { yupResolver } from '@primevue/forms/resolvers/yup';
import * as yup from 'yup';
import InputForm from '../common/FormField.vue';

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

const schema = yup.object({
    topic: yup.string().required(t('upload.required', { field: t('upload.topicLabel') })),
    file_upload: yup.mixed().
        test(
            'fileRequired',
            t('upload.required', { field: t('upload.fileLabel') }),
            value => {
                return value && value.length > 0;
            }
        )
    // required(t('upload.required', { field: t('upload.fileLabel') }))
});

const resolver = yupResolver(schema);

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

const onClear = () => {
    selectedFile.value = null
    isErrorFile.value.view = false
    isErrorFile.value.message = null
}

const isErrorFile = ref({
    view: false,
    message: null
})

const handleUpload = async ({ valid }) => {
    if (!selectedFile.value) {
        isErrorFile.value.view = true
        isErrorFile.value.message = t('upload.required', { field: t('upload.fileLabel') })
        return
    }
    else {
        isErrorFile.value.view = false
        isErrorFile.value.message = null
    }

    if (valid && !isErrorFile.value.view) {
        error.value = null
        loading.value = true
        const formData = new FormData()
        formData.append('file', selectedFile.value)
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
    else return
}
</script>

<template>

    <PageBase :title="t('upload.title')">
        <template #default>
            <Form v-slot="$form" :initialValues :resolver @submit="handleUpload"
                class="flex flex-col gap-4 w-full sm:w-56">

                <InputForm v-model:model="topic" name="topic" class="w-full p-inputtext-lg"
                    :placeholder="t('upload.topicPlaceholder')" :form="$form" key="topic">
                    <template #append>
                        <transition name="fade">
                            <div v-if="showSuggestions" class="suggestions-panel glass-panel">
                                <Listbox :options="suggestions" @change="e => selectSuggestion(e.value)"
                                    class="border-none" />
                            </div>
                        </transition>
                    </template>
                </InputForm>
                
                <div class="form-field">
                    <FileUpload mode="basic" customUpload name="file_upload" :auto="false" :multiple="false"
                        :accept="allowedExtensions.join(',')" :chooseLabel="t('common.search')"
                        :uploadLabel="t('upload.buttonLabel')" :cancelLabel="t('common.back')" class="custom-fileupload"
                        :maxFileSize="10000000" :disabled="loading" @select="e => onFileSelect(e)"
                        @clear="() => onClear()">
                        <template #empty>
                            <div class="flex flex-column align-items-center justify-content-center p-4">
                                <i class="pi pi-cloud-upload text-4xl mb-3 text-secondary"></i>
                                <p class="text-secondary">{{ t('upload.subtitle') }}</p>
                                <small class="text-secondary opacity-60">Max 10MB</small>
                            </div>
                        </template>
                    </FileUpload>
                    <Message v-if="isErrorFile.view" severity="error" size="small" variant="simple">{{
                        isErrorFile.message }}</Message>
                </div>
                <div class="form-field-button">
                    <Button class="btn-upload" type="submit" :label="t('upload.buttonLabel')" :loading="loading" />
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



.btn-upload {
    background-color: var(--p-cyan-700);
    color: white;
    border: none;
}
</style>

<style>

.form-field-button {
    display: flex;
    flex-direction: row;
    gap: 1rem;
    justify-content: center;
    align-items: center;
    margin-bottom: 10px;
}
</style>
