<script lang="ts">
  import { api, type UploadResp } from '$lib/api';
  let file: File | null = null;
  let status = '';
  let preview: string | null = null;
  let uploadId: string | null = null;

  function onFile(e: Event) {
    const input = e.target as HTMLInputElement;
    file = input.files?.[0] ?? null;
    status = '';
    uploadId = null;
    if (file) {
      const reader = new FileReader();
      reader.onload = () => (preview = String(reader.result));
      reader.readAsDataURL(file);
    } else {
      preview = null;
    }
  }

  async function doUpload() {
    if (!file) { status = 'Select an image'; return; }
    status = 'Uploading…';
    const form = new FormData();
    form.append('file', file);
    try {
      const data = await api<UploadResp>('/api/uploads', { method: 'POST', body: form });
      uploadId = data.uploadId;
      status = `Uploaded: ${uploadId}`;
    } catch (e) {
      status = String(e);
    }
  }
</script>

<section class="panel grid gap-4">
  <div>
    <h1 class="title mb-2">Upload</h1>
    <p class="subtle">Upload an image to begin the workflow.</p>
  </div>
  <div class="grid gap-2">
    <input type="file" accept="image/*" on:change={onFile} />
    <div class="flex gap-2 items-center">
      <button class="btn" on:click={doUpload}>Upload</button>
      <span class="subtle">{status}</span>
    </div>
    {#if preview}
    <div class="border border-border rounded-xl overflow-hidden">
      <img src={preview} alt="preview" class="w-full h-64 object-contain bg-white" />
    </div>
    {/if}
  </div>
</section>


