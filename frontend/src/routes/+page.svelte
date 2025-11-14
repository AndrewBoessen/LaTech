<script lang="ts">
  import LatexBackground from "../lib/components/LatexBackground.svelte";
</script>

<div class="relative z-10 flex-1 flex flex-col">
  <LatexBackground />

  <section class="flex-1 flex flex-col items-center justify-center text-center">
    <h1 class="text-8xl font-bold">LaTech</h1>
    <p class="my-4 text-3xl text-gray-800">
      Convert images of equations to LaTeX PDFs.
    </p>
    <a
      href="/upload"
      class="bg-black hover:bg-gray-800 text-white font-bold py-4 px-8 text-xl"
    >
      Upload Image
    </a>
  </section>
</div>
