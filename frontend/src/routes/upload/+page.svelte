<script lang="ts">
  import { api, type JobResp } from "$lib/api";
  let file: File | null = null;
  let status = "";
  let preview: string | null = null;
  let jobId: string | null = null;

  function onFile(e: Event) {
    const input = e.target as HTMLInputElement;
    file = input.files?.[0] ?? null;
    status = "";
    jobId = null;
    if (file) {
      const reader = new FileReader();
      reader.onload = () => (preview = String(reader.result));
      reader.readAsDataURL(file);
    } else {
      preview = null;
    }
  }

  async function doUpload() {
    if (!file) {
      status = "Select an image";
      return;
    }
    status = "Uploading…";
    const form = new FormData();
    form.append("file", file);
    try {
      const data = await api<JobResp>("/api/uploads", {
        method: "POST",
        body: form,
      });
      jobId = data.job_id;
      status = `Uploaded: ${jobId}`;
    } catch (e) {
      status = String(e);
    }
  }
</script>

<section class="panel grid gap-8">
  <div>
    <h1 class="title mb-4">Upload</h1>
    <p class="subtle">Upload an image to begin the workflow.</p>
  </div>
  <div class="grid gap-4">
    <input type="file" accept="image/*" on:change={onFile} />
    <div class="flex gap-4 items-center">
      <button class="btn" on:click={doUpload}>Upload</button>
      <span class="subtle">{status}</span>
    </div>
    {#if jobId}
      <label>Job ID <input type="text" readonly bind:value={jobId} /></label>
    {/if}
    {#if preview}
      <div class="border border-border overflow-hidden">
        <img
          src={preview}
          alt="preview"
          class="w-full max-h-64 object-contain bg-white"
        />
      </div>
    {/if}
  </div>
</section>
