<script lang="ts">
  import { api, type JobResp } from "$lib/api";

  let status = "";
  let pdfUrl = "";
  let jobId = "";

  async function doCompile() {
    if (!jobId) {
      status = "jobId not found";
      return;
    }
    status = "Compiling…";
    try {
      const data = await api<JobResp>(
        `/api/compile/${encodeURIComponent(jobId)}`,
        { method: "POST" },
      );
      pdfUrl = `/api/pdf/${data.job_id}`;
      status = "Compilation complete!";
    } catch (e) {
      status = String(e);
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
        bind:value={jobId}
        placeholder="paste jobId"
      /></label
    >
    <div class="flex gap-2 items-center">
      <button class="btn" on:click={doCompile}>Compile</button>
      <span class="subtle">{status}</span>
    </div>
  </div>
  {#if pdfUrl}
    <a href={pdfUrl} target="_blank">View PDF</a>
  {/if}
</section>

