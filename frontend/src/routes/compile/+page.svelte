<script lang="ts">
  import { api, type Job, type JobResp } from "$lib/api";
  import { page } from "$app/stores";
  import { onMount } from "svelte";
  import { goto } from "$app/navigation";

  let status = "";
  let pdfUrl = "";
  let jobId = "";
  let job: Job | null = null;
  let latexCode = "";
  let previewStatus = "";

  onMount(() => {
    jobId = $page.url.searchParams.get("id") || "";
    if (jobId) {
      pollStatus();
    }
  });

  async function doCompile() {
    if (!jobId) {
      status = "jobId not found";
      return;
    }
    status = "Compiling…";
    try {
      await api<JobResp>(
        `/api/compile/${encodeURIComponent(jobId)}`,
        { method: "POST" },
      );
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
        status = job.status;
        if (job.status === "complete") {
          clearInterval(interval);
          await goto(`/preview?id=${jobId}`);
        } else if (job.status === "failed") {
          clearInterval(interval);
        }
      } catch (e) {
        status = String(e);
        clearInterval(interval);
      }
    }, 2000);
  }

  async function previewLatex() {
    if (!jobId) {
      previewStatus = "jobId not found";
      return;
    }
    previewStatus = "Fetching LaTeX…";
    try {
      const resp = await fetch(`/api/latex/${encodeURIComponent(jobId)}`);
      if (!resp.ok) {
        throw new Error(await resp.text());
      }
      latexCode = await resp.text();
      previewStatus = "LaTeX loaded.";
    } catch (e) {
      previewStatus = String(e);
    }
  }
</script>

<section class="panel grid gap-4">
  <div>
    <h1 class="title mb-2">Compile to PDF</h1>
    <p class="subtle">Compile the LaTeX source to a PDF.</p>
  </div>
  <div class="grid gap-2">
    <label
      >Job ID <input
        type="text"
        readonly
        bind:value={jobId}
        placeholder="paste jobId"
      /></label
    >
    <div class="flex gap-2 items-center">
      <button class="btn" on:click={doCompile}>Compile</button>
      <button class="btn" on:click={previewLatex}>Preview LaTeX</button>
      <span class="subtle">{status}</span>
    </div>
  </div>
  {#if pdfUrl}
    <a href={pdfUrl} target="_blank">View PDF</a>
  {/if}
  {#if latexCode}
    <div class="grid gap-2">
      <h2 class="title">LaTeX Preview</h2>
      <pre class="panel" style="overflow-x: auto;">{latexCode}</pre>
      <span class="subtle">{previewStatus}</span>
    </div>
  {/if}
</section>
