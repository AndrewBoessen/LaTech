<script lang="ts">
  import { api, type PreprocessResp } from '$lib/api';
  let uploadId = '';
  let processedId: string | null = null;
  let status = '';
  let grayscale = true;
  let denoise = false;
  let threshold = 128;
  let width: number | null = null;
  let height: number | null = null;

  async function doPreprocess() {
    if (!uploadId) { status = 'Provide uploadId'; return; }
    status = 'Preprocessing…';
    try {
      const body: any = { grayscale, denoise, threshold, resize: width && height ? { width, height } : null };
      const data = await api<PreprocessResp>(`/api/preprocess/${encodeURIComponent(uploadId)}`, {
        method: 'POST',
        headers: { 'content-type': 'application/json' },
        body: JSON.stringify(body)
      });
      processedId = data.processedId;
      status = `Processed: ${processedId}`;
    } catch (e) {
      status = String(e);
    }
  }
</script>

<section class="panel grid gap-4">
  <div>
    <h1 class="title mb-2">Preprocess</h1>
    <p class="subtle">Set preprocessing options and process an uploaded image.</p>
  </div>
  <div class="grid gap-3 max-w-xl">
    <label class="flex items-center gap-2"><input type="checkbox" bind:checked={grayscale} /> Grayscale</label>
    <label class="flex items-center gap-2"><input type="checkbox" bind:checked={denoise} /> Denoise</label>
    <label>Threshold <input type="range" min="0" max="255" bind:value={threshold} /></label>
    <div class="grid grid-cols-1 sm:grid-cols-2 gap-2">
      <label>Width <input type="number" bind:value={width} min="1" placeholder="width" /></label>
      <label>Height <input type="number" bind:value={height} min="1" placeholder="height" /></label>
    </div>
    <label>Upload ID <input type="text" bind:value={uploadId} placeholder="paste uploadId" /></label>
    <div class="flex gap-2 items-center">
      <button class="btn" on:click={doPreprocess}>Apply</button>
      <span class="subtle">{status}</span>
    </div>
  </div>
</section>


