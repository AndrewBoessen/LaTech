<script lang="ts">
  import { api, type Job, type JobResp } from "$lib/api";
  import { page } from "$app/stores";
  import { onMount } from "svelte";
  import { goto } from "$app/navigation";

  let status = "";
  let jobId = "";
  let job: Job | null = null;
  let isCompiling = false;
  let pdfUrl = "";
  let originalUrl = "";
  let showComparison = true;

  onMount(() => {
    jobId = $page.url.searchParams.get("id") || "";
    if (jobId) {
      originalUrl = `/api/uploads/${encodeURIComponent(jobId)}/image`;
      pollStatus();
    }
  });

  async function doCompile() {
    if (!jobId) {
      status = "jobId not found";
      return;
    }
    status = "Compiling…";
    isCompiling = true;
    try {
      await api<JobResp>(`/api/compile/${encodeURIComponent(jobId)}`, {
        method: "POST",
      });
      pollStatus();
    } catch (e) {
      status = String(e);
      isCompiling = false;
    }
  }

  async function pollStatus() {
    if (!jobId) return;
    const interval = setInterval(async () => {
      try {
        job = await api<Job>(`/api/status/${encodeURIComponent(jobId)}`);
        status = job.status;

        if (job.status === "complete") {
          clearInterval(interval);
          isCompiling = false;
          pdfUrl = `/api/pdf/${encodeURIComponent(jobId)}`;
        } else if (job.status === "failed") {
          clearInterval(interval);
          isCompiling = false;
        } else if (job.status === "compiling") {
          isCompiling = true;
        }
      } catch (e) {
        status = String(e);
        clearInterval(interval);
        isCompiling = false;
      }
    }, 2000);
  }
</script>

<div class="h-full flex flex-col">
  <div class="mb-6">
    <h1 class="title mb-2">Compile to PDF</h1>
    <p class="subtle">Generate your final PDF document.</p>
  </div>

  <div class="grid lg:grid-cols-[350px_1fr] gap-8 h-full min-h-0">
    <!-- Control Panel -->
    <div class="panel flex flex-col gap-6 h-fit">
      <div class="grid gap-4">
        <div class="p-4 rounded-xl bg-surface-2 border border-border/50">
          <h3 class="font-medium mb-2">Status</h3>
          <div class="flex items-center gap-2">
            {#if isCompiling}
              <div class="w-2 h-2 rounded-full bg-yelllow-500"></div>
              <span class="text-yellow-600 font-medium">Processing</span>
            {:else if job?.status === "complete"}
              <div class="w-2 h-2 rounded-full bg-green-500"></div>
              <span class="text-green-600 font-medium">Complete</span>
            {:else if job?.status === "failed"}
              <div class="w-2 h-2 rounded-full bg-red-500"></div>
              <span class="text-red-600 font-medium">Failed</span>
            {:else}
              <div class="w-2 h-2 rounded-full bg-subtle"></div>
              <span class="text-subtle capitalize">{status || "Ready"}</span>
            {/if}
          </div>
        </div>
      </div>

      <div class="mt-auto pt-4 border-t border-border flex flex-col gap-3">
        {#if !pdfUrl}
          <button
            class="btn w-full !rounded-full"
            on:click={doCompile}
            disabled={!jobId || isCompiling}
          >
            {isCompiling ? "Compiling..." : "Compile PDF"}
          </button>
        {:else}
          <a
            href={pdfUrl}
            download="output.pdf"
            class="btn w-full !rounded-full text-center flex items-center justify-center gap-2"
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
              <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
              <polyline points="7 10 12 15 17 10"></polyline>
              <line x1="12" y1="15" x2="12" y2="3"></line>
            </svg>
            Download PDF
          </a>
        {/if}
      </div>
    </div>

    <!-- Preview Panel -->
    <div class="panel flex flex-col min-h-0 overflow-hidden p-0">
      <div
        class="p-4 border-b border-border bg-surface-1 flex justify-between items-center"
      >
        <h2 class="font-medium">Preview</h2>
        <button
          on:click={() => (showComparison = !showComparison)}
          class="text-xs px-3 py-1.5 rounded-lg bg-surface-2 hover:bg-surface-3 transition-colors flex items-center gap-2"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="14"
            height="14"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
          >
            <rect x="3" y="3" width="18" height="18" rx="2" />
            <line x1="9" y1="3" x2="9" y2="21" />
          </svg>
          {showComparison ? "Hide Comparison" : "Show Comparison"}
        </button>
      </div>

      <div
        class="flex-1 {showComparison
          ? 'grid grid-cols-2'
          : 'flex'} gap-0 min-h-0"
      >
        {#if showComparison}
          <!-- Original Image -->
          <div class="border-r border-border bg-surface-2 relative">
            <div
              class="absolute top-2 left-2 z-10 bg-black/50 text-white text-xs px-2 py-1 rounded"
            >
              Original
            </div>
            {#if originalUrl}
              <img
                src={originalUrl}
                alt="Original"
                class="w-full h-full object-contain p-4"
              />
            {:else}
              <div
                class="w-full h-full flex items-center justify-center text-subtle"
              >
                Loading image...
              </div>
            {/if}
          </div>
        {/if}

        <!-- PDF Preview -->
        <div class="bg-white relative {showComparison ? '' : 'flex-1'}">
          <div
            class="absolute top-2 left-2 z-10 bg-black/50 text-white text-xs px-2 py-1 rounded"
          >
            PDF
          </div>
          {#if pdfUrl}
            <iframe
              src={pdfUrl}
              title="PDF Preview"
              class="w-full h-full border-none"
            ></iframe>
          {:else if isCompiling}
            <div
              class="w-full h-full flex flex-col items-center justify-center text-subtle gap-4"
            >
              <div
                class="w-8 h-8 border-2 border-primary border-t-transparent rounded-full animate-spin"
              ></div>
              <p>Compiling PDF...</p>
            </div>
          {:else}
            <div
              class="w-full h-full flex flex-col items-center justify-center text-subtle gap-2"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="48"
                height="48"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="1"
                stroke-linecap="round"
                stroke-linejoin="round"
                class="opacity-20"
              >
                <path
                  d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z"
                ></path>
                <polyline points="14 2 14 8 20 8"></polyline>
              </svg>
              <p>Ready to compile</p>
            </div>
          {/if}
        </div>
      </div>
    </div>
  </div>
</div>
