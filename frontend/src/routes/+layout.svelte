<script>
  import '../app.css';
</script>

<div class="flex min-h-screen">
  <nav class="w-64 bg-panel border-r border-border flex flex-col py-10 px-8 gap-2">
    <a href="/" class="text-2xl font-bold mb-8">LaTech</a>
    <a href="/upload" class="block py-3 px-3 text-lg font-semibold hover:bg-border">Upload</a>
    <a href="/preprocess" class="block py-3 px-3 text-lg font-semibold hover:bg-border">Preprocess</a>
    <a href="/convert" class="block py-3 px-3 text-lg font-semibold hover:bg-border">Convert</a>
    <a href="/compile" class="block py-3 px-3 text-lg font-semibold hover:bg-border">Compile</a>
    <a href="/preview" class="block py-3 px-3 text-lg font-semibold hover:bg-border">Preview</a>
  </nav>
  <main class="flex-1 flex flex-col">
    <div class="container py-10 flex-1 flex flex-col">
      <slot />
    </div>
    <footer class="mt-10 text-center subtle">© {new Date().getFullYear()} LaTech</footer>
  </main>
</div>


