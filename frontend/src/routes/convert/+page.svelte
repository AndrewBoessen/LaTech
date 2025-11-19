<script lang="ts">
  import { api, type Job, type JobResp } from "$lib/api";
  import { page } from "$app/stores";
  import { onMount } from "svelte";
  import { goto } from "$app/navigation";

  let status = "";
  let jobId = "";
  let job: Job | null = null;

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
    try {
      await api<JobResp>(`/api/convert/${encodeURIComponent(jobId)}`, {
        method: "POST",
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
        status = job.status;
        if (job.status === "ready to compile") {
          clearInterval(interval);
          await goto(`/compile?id=${jobId}`);
        } else if (job.status === "failed") {
          clearInterval(interval);
        }
      } catch (e) {
        status = String(e);
        clearInterval(interval);
      }
    }, 2000);
  }
</script>

<section class="panel grid gap-4">
  <div>
    <h1 class="title mb-2">Convert to LaTeX</h1>
    <p class="subtle">
      Run OCR on the processed image and review the LaTeX output.
    </p>
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
      <button class="btn" on:click={doConvert}>Convert</button>
      <span class="subtle">{status}</span>
    </div>
  </div>
</section>
