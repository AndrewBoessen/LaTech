<script lang="ts">
  import { api, type ConvertResp } from '$lib/api';
  let processedId = '';
  let latexId: string | null = null;
  let latex = '';
  let status = '';

  async function doConvert() {
    if (!processedId) { status = 'Provide processedId'; return; }
    status = 'Converting…';
    try {
      const data = await api<ConvertResp>(`/api/convert/${encodeURIComponent(processedId)}`, { method: 'POST' });
      latexId = data.latexId;
      latex = data.latex;
      status = `LaTeX: ${latexId}`;
    } catch (e) {
      status = String(e);
    }
  }
</script>

<section class="panel grid gap-4">
  <div>
    <h1 class="title mb-2">Convert to LaTeX</h1>
    <p class="subtle">Run OCR on the processed image and review the LaTeX output.</p>
  </div>
  <div class="grid gap-3">
    <label>Processed ID <input type="text" bind:value={processedId} placeholder="paste processedId" /></label>
    <div class="flex gap-2 items-center">
      <button class="btn" on:click={doConvert}>Convert</button>
      <span class="subtle">{status}</span>
    </div>
    <label>LaTeX</label>
    <textarea class="w-full min-h-48" bind:value={latex} placeholder="% LaTeX will appear here…"></textarea>
  </div>
</section>


