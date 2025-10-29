<script>
  import '../app.css';
</script>

<div class="container py-6">
  <header class="mb-6 flex items-center justify-between">
    <a href="/" class="text-2xl font-semibold">LaTech</a>
    <nav class="flex gap-4 text-sm">
      <a href="/upload" class="underline">Upload</a>
      <a href="/preprocess" class="underline">Preprocess</a>
      <a href="/convert" class="underline">Convert</a>
      <a href="/compile" class="underline">Compile</a>
      <a href="/preview" class="underline">Preview</a>
    </nav>
  </header>
  <slot />
  <footer class="mt-10 text-center subtle">© {new Date().getFullYear()} LaTech</footer>
  
</div>


