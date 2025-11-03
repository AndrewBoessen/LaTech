<script lang="ts">
  import { api, type JobResp } from "$lib/api";

  let status = "";
  let jobId = "";
  let options = {
    grayscale: true,
    denoise: true,
    deskew: true,
  };

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
      status = "Preprocessing complete!";
    } catch (e) {
      status = String(e);
    }
  }
</script>

<section class="panel grid gap-4">
  <div>
    <h1 class="title mb-2">Preprocess Image</h1>
    <p class="subtle">Apply preprocessing options to the uploaded image.</p>
  </div>
  <div class="grid gap-3">
    <label
      >Job ID <input
        type="text"
        bind:value={jobId}
        placeholder="paste jobId"
      /></label
    >
    <label
      ><input type="checkbox" bind:checked={options.grayscale} /> Grayscale</label
    >
    <label
      ><input type="checkbox" bind:checked={options.denoise} /> Denoise</label
    >
    <label><input type="checkbox" bind:checked={options.deskew} /> Deskew</label
    >
    <div class="flex gap-2 items-center">
      <button class="btn" on:click={doPreprocess}>Preprocess</button>
      <span class="subtle">{status}</span>
    </div>
  </div>
</section>

