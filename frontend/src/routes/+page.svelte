<script lang="ts">
  import LatexBackground from "../lib/components/LatexBackground.svelte";
  import { getJobs, deleteJob, type Job } from "../lib/api";
  import { onMount } from "svelte";

  let jobs: Job[] = [];

  onMount(async () => {
    jobs = await getJobs();
  });

  async function handleDelete(jobId: string) {
    try {
      await deleteJob(jobId);
      jobs = jobs.filter((job) => job.job_id !== jobId);
    } catch (error) {
      console.error("Error deleting job:", error);
      alert("Failed to delete job.");
    }
  }
</script>

<LatexBackground />

<section class="panel" style="position:relative; z-index:1;">
  <h1 class="title mb-4">Image → LaTeX → PDF</h1>
  <p class="subtle">
    Use the steps in the navigation to process an image, convert to LaTeX and
    preview a PDF.
  </p>
</section>

<section class="panel" style="position:relative; z-index:1;">
  <h2 class="title mb-4">Jobs</h2>
  <div class="overflow-x-auto">
    <table class="table-auto w-full text-left whitespace-no-wrap">
      <thead>
        <tr>
          <th
            class="px-4 py-3 title-font tracking-wider font-large text-gray-900 text-base bg-gray-100"
            >Job ID</th
          >
          <th
            class="px-4 py-3 title-font tracking-wider font-large text-gray-900 text-base bg-gray-100"
            >Status</th
          >
          <th
            class="px-4 py-3 title-font tracking-wider font-large text-gray-900 text-base bg-gray-100"
            >Upload ID</th
          >
          <th
            class="px-4 py-3 title-font tracking-wider font-large text-gray-900 text-base bg-gray-100"
            >Processed ID</th
          >
          <th
            class="px-4 py-3 title-font tracking-wider font-large text-gray-900 text-base bg-gray-100"
            >LaTeX ID</th
          >
          <th
            class="px-4 py-3 title-font tracking-wider font-large text-gray-900 text-base bg-gray-100"
            >PDF ID</th
          >
          <th
            class="px-4 py-3 title-font tracking-wider font-large text-gray-900 text-base bg-gray-100"
            >Actions</th
          >
        </tr>
      </thead>
      <tbody>
        {#each jobs as job}
          <tr>
            <td class="px-4 py-3">{job.job_id}</td>
            <td class="px-4 py-3">{job.status}</td>
            <td class="px-4 py-3">{job.upload_id}</td>
            <td class="px-4 py-3">{job.processed_id}</td>
            <td class="px-4 py-3">{job.latex_id}</td>
            <td class="px-4 py-3">{job.pdf_id}</td>
            <td class="px-4 py-3">
              <button
                on:click={() => handleDelete(job.job_id)}
                class="text-red-500 hover:text-red-700"
              >
                Delete
              </button>
            </td>
          </tr>
        {/each}
      </tbody>
    </table>
  </div>
</section>
