<script lang="ts">
  import { api, type JobResp } from "$lib/api";
  import { goto } from "$app/navigation";

  let file: File | null = null;
  let status = "";
  let preview: string | null = null;
  let jobId: string | null = null;
  let fileInput: HTMLInputElement;

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

  function triggerFileInput() {
    fileInput.click();
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
      await goto(`/preprocess?id=${jobId}`);
    } catch (e) {
      status = String(e);
    }
  }
</script>

<div class="min-h-90 flex flex-col items-center justify-center p-8 bg-gray-50">
  <div class="w-full max-w-4xl flex flex-col items-center gap-8">
    <div class="text-center space-y-2">
      <h1 class="text-4xl font-bold text-gray-900">Upload Image</h1>
      <p class="text-lg text-gray-600">
        Upload an image (PNG or JPG) to preview.
      </p>
    </div>

    <!-- Upload Placeholder / Preview Area -->
    <div
      class="w-full aspect-video bg-white rounded-xl border-4 border-dashed border-gray-300 flex flex-col items-center justify-center relative overflow-hidden transition-colors hover:border-gray-400"
      class:border-solid={!!preview}
      class:border-transparent={!!preview}
    >
      {#if preview}
        <img src={preview} alt="preview" class="w-full h-full object-contain" />
        <button
          class="absolute top-4 right-4 bg-white/80 hover:bg-white text-gray-800 p-2 rounded-full shadow-sm transition-all"
          on:click={() => {
            file = null;
            preview = null;
          }}
          title="Remove image"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            stroke-width="1.5"
            stroke="currentColor"
            class="w-6 h-6"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              d="M6 18L18 6M6 6l12 12"
            />
          </svg>
        </button>
      {:else}
        <div class="text-center p-8">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            stroke-width="1.5"
            stroke="currentColor"
            class="w-16 h-16 mx-auto text-gray-400 mb-4"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              d="M2.25 15.75l5.159-5.159a2.25 2.25 0 013.182 0l5.159 5.159m-1.5-1.5l1.409-1.409a2.25 2.25 0 013.182 0l2.909 2.909m-18 3.75h16.5a1.5 1.5 0 001.5-1.5V6a1.5 1.5 0 00-1.5-1.5H3.75A1.5 1.5 0 002.25 6v12a1.5 1.5 0 001.5 1.5zm10.5-11.25h.008v.008h-.008V8.25zm.375 0a.375.375 0 11-.75 0 .375.375 0 01.75 0z"
            />
          </svg>
          <button
            class="bg-black hover:bg-gray-800 text-white font-bold py-3 px-8 rounded-lg text-lg transition-colors"
            on:click={triggerFileInput}
          >
            Select Image
          </button>
          <p class="mt-2 text-sm text-gray-500">Supported formats: PNG, JPG</p>
        </div>
      {/if}
    </div>

    <!-- Hidden Input -->
    <input
      type="file"
      accept="image/png, image/jpeg, image/jpg"
      class="hidden"
      bind:this={fileInput}
      on:change={onFile}
    />

    <!-- Action Bar -->
    {#if file}
      <div
        class="flex flex-col items-center gap-4 animate-in fade-in slide-in-from-bottom-4 duration-300"
      >
        <button
          class="bg-blue-600 hover:bg-blue-700 text-white font-bold py-4 px-12 rounded-full text-xl shadow-lg transition-all transform hover:scale-105"
          on:click={doUpload}
        >
          Upload & Process
        </button>
        {#if status}
          <p class="text-gray-600 font-medium">{status}</p>
        {/if}
      </div>
    {/if}
  </div>
</div>
