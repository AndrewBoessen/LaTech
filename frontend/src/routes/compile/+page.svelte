<script lang="ts">
  import { api, type CompileResp } from '$lib/api';
  let latexId = '';
  let latex = '';
  let pdfId: string | null = null;
  let status = '';

  async function doCompile() {
    status = 'Compiling…';
    try {
      const body: any = {};
      if (latex) body.latex = latex; else if (latexId) body.latexId = latexId;
      else { status = 'Provide latex or latexId'; return; }
      const data = await api<CompileResp>('/api/compile', {
        method: 'POST',
        headers: { 'content-type': 'application/json' },
        body: JSON.stringify(body)
      });
      pdfId = data.pdfId;
      status = `PDF: ${pdfId}`;
    } catch (e) {
      status = String(e);
    }
  }
</script>

<section class="panel grid gap-4">
  <div>
    <h1 class="title mb-2">Compile</h1>
    <p class="subtle">Compile LaTeX text or an existing latexId to a PDF.</p>
  </div>
  <div class="grid gap-3">
    <label>LaTeX ID <input type="text" bind:value={latexId} placeholder="optional latexId" /></label>
    <label>LaTeX</label>
    <textarea class="w-full min-h-64" bind:value={latex} placeholder="% Paste LaTeX here or use an ID"></textarea>
    <div class="flex gap-2 items-center">
      <button class="btn" on:click={doCompile}>Compile</button>
      <span class="subtle">{status}</span>
    </div>
  </div>
</section>


