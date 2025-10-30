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

<section class="panel grid gap-8">
  <div>
    <h1 class="title mb-4">Compile</h1>
    <p class="subtle">Compile LaTeX text or an existing latexId to a PDF.</p>
  </div>
  <div class="grid gap-5">
    <label for="latexId">LaTeX ID <input type="text" id="latexId" bind:value={latexId} placeholder="optional latexId" /></label>
    <label for="latex">LaTeX</label>
    <textarea id="latex" class="w-full min-h-64" bind:value={latex} placeholder="% Paste LaTeX here or use an ID"></textarea>
    <div class="flex gap-4 items-center">
      <button class="btn" on:click={doCompile}>Compile</button>
      <span class="subtle">{status}</span>
    </div>
  </div>
</section>


