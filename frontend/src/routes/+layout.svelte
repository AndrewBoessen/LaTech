<script>
  import '../app.css';
  let showMenu = false;

  function toggleMenu() {
    showMenu = !showMenu;
  }
</script>

<div class="flex min-h-screen">
  <!-- Desktop Navbar -->
  <nav class="hidden md:flex w-1/8 min-w-50 bg-panel border-r border-border flex flex-col py-10 px-8 gap-2">
    <a href="/" class="text-2xl font-bold mb-8">LaTech</a>
    <a href="/upload" class="block py-3 px-3 text-lg font-semibold hover:bg-border">Upload</a>
    <a href="/preprocess" class="block py-3 px-3 text-lg font-semibold hover:bg-border">Preprocess</a>
    <a href="/convert" class="block py-3 px-3 text-lg font-semibold hover:bg-border">Convert</a>
    <a href="/compile" class="block py-3 px-3 text-lg font-semibold hover:bg-border">Compile</a>
    <a href="/preview" class="block py-3 px-3 text-lg font-semibold hover:bg-border">Preview</a>
  </nav>

  <main class="flex-1 flex flex-col">
    <!-- Mobile Navbar -->
    <nav class="w-full bg-panel border-b border-border flex items-center justify-between py-4 px-8 md:hidden">
      <a href="/" class="text-2xl font-bold">LaTech</a>
      <div class="relative">
        <button on:click={toggleMenu} aria-label="Toggle menu">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
            <path stroke-linecap="round" stroke-linejoin="round" d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25h16.5" />
          </svg>
        </button>
        <div class="{showMenu ? 'block' : 'hidden'} absolute right-0 w-1/4 min-w-40 origin-top-right bg-panel border border-border z-10">
          <a href="/upload" class="block px-4 py-2 text-lg font-semibold hover:bg-border">Upload</a>
          <a href="/preprocess" class="block px-4 py-2 text-lg font-semibold hover:bg-border">Preprocess</a>
          <a href="/convert" class="block px-4 py-2 text-lg font-semibold hover:bg-border">Convert</a>
          <a href="/compile" class="block px-4 py-2 text-lg font-semibold hover:bg-border">Compile</a>
          <a href="/preview" class="block px-4 py-2 text-lg font-semibold hover:bg-border">Preview</a>
        </div>
      </div>
    </nav>

    <div class="container py-10 flex-1 flex flex-col">
      <slot />
    </div>
    <footer class="mt-10 text-center subtle">© {new Date().getFullYear()} LaTech</footer>
  </main></div>


