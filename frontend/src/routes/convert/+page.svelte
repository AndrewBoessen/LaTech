<script lang="ts">
  import { api, type Job, type JobResp } from "$lib/api";
  import { page } from "$app/stores";
  import { onMount } from "svelte";
  import { goto } from "$app/navigation";
  import CodeMirror from "svelte-codemirror-editor";
  import { StreamLanguage } from "@codemirror/language";
  import { stex } from "@codemirror/legacy-modes/mode/stex";

  let status = "";
  let jobId = "";
  let job: Job | null = null;
  let latexContent = "";
  let isConverting = false;
  let isSaving = false;

  onMount(() => {
    jobId = $page.url.searchParams.get("id") || "";
    if (jobId) {
      pollStatus();
    }
  });

  async function doConvert() {
    if (!jobId) {
      status = "jobId not found";
      return;
    }
    status = "Converting…";
    isConverting = true;
    try {
      await api<JobResp>(`/api/convert/${encodeURIComponent(jobId)}`, {
        method: "POST",
      });
      pollStatus();
    } catch (e) {
      status = String(e);
      isConverting = false;
    }
  }

  async function fetchLatex() {
    try {
      const res = await fetch(`/api/latex/${encodeURIComponent(jobId)}`);
      if (res.ok) {
        latexContent = await res.text();
      } else {
        console.error("Failed to fetch LaTeX");
      }
    } catch (e) {
      console.error(e);
    }
  }

  async function saveAndContinue() {
    if (!jobId) return;
    isSaving = true;
    try {
      // Save LaTeX
      await fetch(`/api/latex/${encodeURIComponent(jobId)}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ content: latexContent }),
      });

      // Navigate to compile
      await goto(`/compile?id=${jobId}`);
    } catch (e) {
      status = "Failed to save: " + String(e);
    } finally {
      isSaving = false;
    }
  }

  async function pollStatus() {
    if (!jobId) return;
    const interval = setInterval(async () => {
      try {
        job = await api<Job>(`/api/status/${encodeURIComponent(jobId)}`);
        status = job.status;

        if (job.status === "ready to compile") {
          clearInterval(interval);
          isConverting = false;
          await fetchLatex();
        } else if (job.status === "failed") {
          clearInterval(interval);
          isConverting = false;
        } else if (job.status === "converting") {
          isConverting = true;
        }
      } catch (e) {
        status = String(e);
        clearInterval(interval);
        isConverting = false;
      }
    }, 2000);
  }
</script>

<div class="h-full flex flex-col">
  <div class="mb-6">
    <h1 class="title mb-2">Convert to LaTeX</h1>
    <p class="subtle">
      Run OCR to generate LaTeX code, then review and edit the result.
    </p>
  </div>

  <div class="grid lg:grid-cols-[350px_1fr] gap-8 h-full min-h-0">
    <!-- Control Panel -->
    <div class="panel flex flex-col gap-6 h-fit">
      <div class="grid gap-4">
        <div class="p-4 rounded-xl bg-surface-2 border border-border/50">
          <h3 class="font-medium mb-2">Status</h3>
          <div class="flex items-center gap-2">
            {#if isConverting}
              <div class="w-2 h-2 rounded-full bg-yellow-500"></div>
              <span class="text-yellow-600 font-medium">Processing</span>
            {:else if job?.status === "ready to compile"}
              <div class="w-2 h-2 rounded-full bg-green-500"></div>
              <span class="text-green-600 font-medium">Conversion Complete</span
              >
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
        {#if !latexContent}
          <button
            class="btn w-full !rounded-lg"
            on:click={doConvert}
            disabled={!jobId || isConverting}
          >
            {isConverting ? "Converting..." : "Start Conversion"}
          </button>
        {:else}
          <button
            class="btn w-full !rounded-lg"
            on:click={saveAndContinue}
            disabled={isSaving}
          >
            {isSaving ? "Saving..." : "Save & Compile PDF"}
          </button>
          <button
            class="btn variant-ghost w-full !rounded-lg"
            on:click={doConvert}
          >
            Re-run Conversion
          </button>
        {/if}
      </div>
    </div>

    <!-- Editor/Preview Panel -->
    <div class="panel flex flex-col min-h-0 overflow-hidden p-0">
      <div
        class="p-4 border-b border-border bg-surface-1 flex justify-between items-center"
      >
        <h2 class="font-medium">LaTeX Editor</h2>
        <span class="text-xs subtle"
          >Edit the code below to fix any OCR errors</span
        >
      </div>
      <div class="flex-1 min-h-0 relative bg-surface-2">
        {#if latexContent}
          <div class="absolute inset-0 overflow-auto">
            <CodeMirror
              bind:value={latexContent}
              lang={StreamLanguage.define(stex)}
              styles={{
                "&": { height: "100%", fontSize: "14px" },
                ".cm-scroller": { fontFamily: "monospace" },
              }}
            />
          </div>
        {:else if isConverting}
          <div
            class="absolute inset-0 flex flex-col items-center justify-center text-subtle gap-4"
          >
            <div
              class="w-8 h-8 border-2 border-primary border-t-transparent rounded-full animate-spin"
            ></div>
            <p>Analyzing image and generating LaTeX...</p>
          </div>
        {:else}
          <div
            class="absolute inset-0 flex flex-col items-center justify-center text-subtle gap-2"
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
                d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"
              ></path>
              <polyline points="14 2 14 8 20 8"></polyline>
              <line x1="16" y1="13" x2="8" y2="13"></line>
              <line x1="16" y1="17" x2="8" y2="17"></line>
              <polyline points="10 9 9 9 8 9"></polyline>
            </svg>
            <p>Ready to convert</p>
          </div>
        {/if}
      </div>
    </div>
  </div>
</div>
