<script lang="ts">
  let pdfId = '';
  $: src = pdfId ? `/api/pdf/${encodeURIComponent(pdfId)}` : '';
</script>

<section class="panel grid gap-8">
  <div>
    <h1 class="title mb-4">Preview PDF</h1>
    <p class="subtle">Enter a pdfId to preview the compiled PDF.</p>
  </div>
  <div class="grid gap-5">
    <label>PDF ID <input type="text" bind:value={pdfId} placeholder="paste pdfId" /></label>
    <div class="border border-border overflow-hidden h-[70vh] bg-white">
      {#if src}
        <iframe src={src} title="PDF preview" class="w-full h-full" />
      {:else}
        <div class="h-full grid place-items-center subtle">No PDF selected</div>
      {/if}
    </div>
  </div>
</section>


