<script lang="ts">
  import { api, type JobResp } from "$lib/api";

  let status = "";
  let jobId = "";

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
      status = "Conversion complete!";
    } catch (e) {
      status = String(e);
    }
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

