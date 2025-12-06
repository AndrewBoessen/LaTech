<script lang="ts">
  import { api, type Job, type JobResp } from "$lib/api";
  import { page } from "$app/stores";
  import { onMount } from "svelte";
  import { goto } from "$app/navigation";

  let status = "";
  let jobId = "";
  let job: Job | null = null;
  let options = {
    grayscale: false,
    denoise: false,
    adaptive_threshold: false,
  };

  let previewUrl = "";
  let originalUrl = "";
  let loadingPreview = false;

  onMount(() => {
    jobId = $page.url.searchParams.get("id") || "";
    if (jobId) {
      originalUrl = `/api/uploads/${encodeURIComponent(jobId)}/image`;
      updatePreview();
      pollStatus();
    }
  });

  async function updatePreview() {
    if (!jobId) return;
    loadingPreview = true;
    try {
      const response = await fetch(
        `/api/preview/${encodeURIComponent(jobId)}`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(options),
        },
      );
      if (response.ok) {
        const blob = await response.blob();
        if (previewUrl) URL.revokeObjectURL(previewUrl);
        previewUrl = URL.createObjectURL(blob);
      } else {
        console.error("Failed to load preview");
      }
    } catch (e) {
      console.error(e);
    } finally {
      loadingPreview = false;
    }
  }

  function toggleOption(key: keyof typeof options) {
    options[key] = !options[key];
    updatePreview();
  }

  async function doPreprocess() {
    if (!jobId) {
      status = "jobId not found";
      return;
    }
    status = "Preprocessing…";
    try {
      await api<JobResp>(`/api/preprocess/${encodeURIComponent(jobId)}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ options }),
      });
      pollStatus();
    } catch (e) {
      status = String(e);
    }
  }

  async function pollStatus() {
    if (!jobId) return;
    const interval = setInterval(async () => {
      try {
        job = await api<Job>(`/api/status/${encodeURIComponent(jobId)}`);
        if (job.status === "ready to convert") {
          status = job.status;
          clearInterval(interval);
          await goto(`/convert?id=${jobId}`);
        } else if (job.status === "failed") {
          status = job.status;
          clearInterval(interval);
        }
      } catch (e) {
        status = String(e);
        clearInterval(interval);
      }
    }, 2000);
  }
</script>

<div class="h-full flex flex-col">
  <div class="mb-6">
    <h1 class="title mb-2">Preprocess Image</h1>
    <p class="subtle">Optimize your image for better conversion results.</p>
  </div>

  <div class="grid lg:grid-cols-[350px_1fr] gap-8 h-full min-h-0">
    <!-- Options Panel -->
    <div class="panel flex flex-col gap-6 h-fit">
      <div class="flex flex-col gap-4">
        <!-- Grayscale Option -->
        <button
          class="flex items-start gap-4 p-4 rounded-xl border-2 transition-all text-left group
          {options.grayscale
            ? 'border-black bg-gray-50'
            : 'border-transparent bg-gray-50/50 hover:border-black'}"
          on:click={() => toggleOption("grayscale")}
        >
          <div
            class="p-2 rounded-lg {options.grayscale
              ? 'bg-black/5 text-black'
              : 'bg-gray-100 text-gray-500'}"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="20"
              height="20"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
            >
              <circle cx="12" cy="12" r="10" />
              <path d="M12 2a10 10 0 0 1 0 20" />
            </svg>
          </div>
          <div>
            <div class="font-medium mb-1">Grayscale</div>
            <div class="text-sm text-gray-500">
              Converts image to black and white for better text contrast.
            </div>
          </div>
        </button>

        <!-- Denoise Option -->
        <button
          class="flex items-start gap-4 p-4 rounded-xl border-2 transition-all text-left group
          {options.denoise
            ? 'border-black bg-gray-50'
            : 'border-transparent bg-gray-50/50 hover:border-black'}"
          on:click={() => toggleOption("denoise")}
        >
          <div
            class="p-2 rounded-lg {options.denoise
              ? 'bg-black/5 text-black'
              : 'bg-gray-100 text-gray-500'}"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="20"
              height="20"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
            >
              <path d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7-10-7-10-7Z" />
              <circle cx="12" cy="12" r="3" />
            </svg>
          </div>
          <div>
            <div class="font-medium mb-1">Denoise</div>
            <div class="text-sm text-gray-500">
              Removes grain and artifacts to clean up the image.
            </div>
          </div>
        </button>

        <!-- Adaptive Threshold Option -->
        <button
          class="flex items-start gap-4 p-4 rounded-xl border-2 transition-all text-left group
          {options.adaptive_threshold
            ? 'border-black bg-gray-50'
            : 'border-transparent bg-gray-50/50 hover:border-black'}"
          on:click={() => toggleOption("adaptive_threshold")}
        >
          <div
            class="p-2 rounded-lg {options.adaptive_threshold
              ? 'bg-black/5 text-black'
              : 'bg-gray-100 text-gray-500'}"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="20"
              height="20"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
            >
              <path d="M4 22h14a2 2 0 0 0 2-2V7.5L14.5 2H6a2 2 0 0 0-2 2v4" />
              <path d="M14 2v6h6" />
              <path d="m3 15 2 2 4-4" />
            </svg>
          </div>
          <div>
            <div class="font-medium mb-1">Scanner Look</div>
            <div class="text-sm text-gray-500">
              Enhances text and removes shadows (Adaptive Threshold).
            </div>
          </div>
        </button>
      </div>

      <div class="mt-auto pt-4 border-t border-border">
        <button
          class="btn w-full !rounded-lg"
          on:click={doPreprocess}
          disabled={!jobId}
        >
          Apply & Continue
        </button>
        {#if status}
          <div class="text-center mt-2 text-sm subtle">{status}</div>
        {/if}
      </div>
    </div>

    <!-- Preview Panel -->
    <div class="panel flex flex-col min-h-0 overflow-hidden">
      <div class="flex items-center justify-between mb-4">
        <h2 class="font-medium">Preview</h2>
        {#if loadingPreview}
          <span class="text-xs subtle animate-pulse">Updating...</span>
        {/if}
      </div>

      <div class="flex-1 grid grid-cols-2 gap-4 min-h-0">
        <!-- Original -->
        <div class="flex flex-col gap-2 min-h-0">
          <span class="text-xs font-medium subtle uppercase tracking-wider"
            >Original</span
          >
          <div
            class="bg-surface-2 rounded-lg overflow-hidden h-full relative border border-border/50"
          >
            {#if originalUrl}
              <img
                src={originalUrl}
                alt="Original"
                class="absolute inset-0 w-full h-full object-contain p-4"
              />
            {:else}
              <div
                class="absolute inset-0 flex items-center justify-center subtle"
              >
                Loading...
              </div>
            {/if}
          </div>
        </div>

        <!-- Processed -->
        <div class="flex flex-col gap-2 min-h-0">
          <span class="text-xs font-medium subtle uppercase tracking-wider"
            >Processed</span
          >
          <div
            class="bg-surface-2 rounded-lg overflow-hidden h-full relative border border-border/50"
          >
            {#if previewUrl}
              <img
                src={previewUrl}
                alt="Preview"
                class="absolute inset-0 w-full h-full object-contain p-4 transition-opacity duration-200 {loadingPreview
                  ? 'opacity-50'
                  : 'opacity-100'}"
              />
            {:else}
              <div
                class="absolute inset-0 flex items-center justify-center subtle"
              >
                Generating preview...
              </div>
            {/if}
          </div>
        </div>
      </div>
    </div>
  </div>
</div>
