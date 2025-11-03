<script lang="ts">
  let jobId = "";
  $: src = jobId ? `/api/pdf/${encodeURIComponent(jobId)}` : "";
</script>

<section class="panel grid gap-8">
  <div>
    <h1 class="title mb-4">Preview PDF</h1>
    <p class="subtle">Enter a jobId to preview the compiled PDF.</p>
  </div>
  <div class="grid gap-5">
    <label
      >Job ID <input
        type="text"
        bind:value={jobId}
        placeholder="paste jobId"
      /></label
    >
    <div
      class="border border-border overflow-hidden h-screen max-h-screen bg-white"
    >
      {#if src}
        <iframe {src} title="PDF preview" class="w-full h-full" />
      {:else}
        <div class="h-full grid place-items-center subtle">No PDF selected</div>
      {/if}
    </div>
  </div>
</section>
