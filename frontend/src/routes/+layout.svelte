<script lang="ts">
  import "../app.css";
  import { getJobs, type Job } from "$lib/api";
  import { onMount } from "svelte";

  let showMenu = false;
  let jobs: Job[] = [];

  onMount(async () => {
    jobs = await getJobs();
  });

  function toggleMenu() {
    showMenu = !showMenu;
  }
</script>

<div class="flex min-h-screen">
  <!-- Sidebar -->
  <nav
    class="w-64 bg-panel border-r border-border flex flex-col py-10 px-8 gap-2 fixed top-0 left-0 h-full z-20 transform {showMenu
      ? 'translate-x-0'
      : '-translate-x-full'} transition-transform duration-300 ease-in-out"
  >
    <div class="flex justify-between items-center mb-8">
      <a href="/" class="text-2xl font-bold">LaTech</a>
      <button on:click={toggleMenu} aria-label="Toggle menu">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
          stroke-width="1.5"
          stroke="currentColor"
          class="w-6 h-6"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            d="M6 18L18 6M6 6l12 12"
          />
        </svg>
      </button>
    </div>
    <h2 class="text-lg font-semibold mb-2">Jobs</h2>
    <ul>
      {#each jobs as job}
        <li class="mb-2">
          <div class="text-sm">
            <p class="font-semibold">{job.name || job.job_id}</p>
            <p
              class="capitalize {job.status === 'failed' ? 'text-red-500' : ''}"
            >
              {job.status}
            </p>
            {#if job.status === "complete" && job.job_id}
              <a
                href={`/api/pdf/${job.job_id}`}
                target="_blank"
                class="text-blue-500 hover:underline"
              >
                View PDF
              </a>
            {/if}
          </div>
        </li>
      {/each}
    </ul>
  </nav>

  <!-- Main content -->
  <main class="flex-1 flex flex-col">
    <div class="container py-10 flex-1 flex flex-col">
      <button
        on:click={toggleMenu}
        aria-label="Toggle menu"
        class="fixed top-4 left-4 z-10 {showMenu ? 'hidden' : ''}"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
          stroke-width="1.5"
          stroke="currentColor"
          class="w-10 h-10"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25h16.5"
          />
        </svg>
      </button>
      <slot />
    </div>
    <footer class="mt-10 text-center subtle">
      © {new Date().getFullYear()} LaTech
    </footer>
  </main>
</div>

<!-- Overlay for mobile menu -->
{#if showMenu}
  <button
    type="button"
    class="fixed inset-0 bg-black opacity-50 z-10"
    on:click={toggleMenu}
    aria-label="Close menu"
  ></button>
{/if}
