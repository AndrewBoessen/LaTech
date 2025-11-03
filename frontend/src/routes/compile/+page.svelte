<script lang="ts">
  import { api, type JobResp } from "$lib/api";

  let status = "";
  let pdfUrl = "";
  let jobId = "";
  let latexCode = "";
  let previewStatus = "";

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
      <pre class="panel">{latexCode}</pre>
      <span class="subtle">{previewStatus}</span>
    </div>
  {/if}
</section>
