<script lang="ts">
  import { onMount } from "svelte";
  // Small bank of LaTeX code snippets for cycling
  const snippets = [
    `\\frac{a}{b} + c = d`,
    `e^{i\\pi} + 1 = 0`,
    `\\int_{a}^{b} f(x) dx`,
    `\\sum_{n=1}^{\\infty} \\frac{1}{n^2} = \\frac{\\pi^2}{6}`,
    `\\lim_{x \\to 0} \\frac{\\sin x}{x} = 1`,
    `\\alpha, \\beta, \\gamma, \\delta, \\epsilon`,
    `\\vec{F} = m\\vec{a}`,
    `\\begin{pmatrix} a & b \\\\ c & d \\end{pmatrix}`,
    `\\nabla \\cdot \\vec{E} = \\frac{\\rho}{\\epsilon_0}`,
    `y = mx+b`,
    `x = \\frac{-b \\pm \\sqrt{b^2-4ac}}{2a}`,
    `i\\hbar\\frac{\\partial}{\\partial t}\\Psi = \\hat{H}\\Psi`,
    `f'(x) = \\lim_{h \\to 0} \\frac{f(x+h)-f(x)}{h}`,
    `\\int_{-\\infty}^{\\infty} e^{-x^2} dx = \\sqrt{\\pi}`,
    `P(A|B) = \\frac{P(B|A)P(A)}{P(B)}`,
    `\\zeta(s) = \\sum_{n=1}^{\\infty} \\frac{1}{n^s}`,
    `\\sigma = \\sqrt{\\frac{1}{N} \\sum_{i=1}^N (x_i - \\mu)^2}`,
    `\\sin^2\\theta + \\cos^2\\theta = 1`,
  ];

  type LatexLine = {
    key: string;
    top: number;
    left: number;
    snippet: string;
    progress: number;
    speed: number;
  };

  const minDistance = 3; // Minimum distance in viewport units (vw/vh)

  // Helper function to check distance between two points
  function isTooClose(
    pos1: { top: number; left: number },
    pos2: { top: number; left: number },
    distance: number,
  ) {
    const dx = Math.abs(pos1.left - pos2.left);
    const dy = Math.abs(pos1.top - pos2.top);
    return dy < distance || dx < distance;
  }

  // Generates a new position that doesn't overlap with existing lines
  function getNewPosition(existingLines: LatexLine[]) {
    let newPos;
    let attempts = 0;
    const maxAttempts = 500; // Prevent infinite loops

    do {
      newPos = { top: Math.random() * 100, left: Math.random() * 100 };
      attempts++;
      if (attempts > maxAttempts) {
        console.log("BREAKING LOOP");
        break;
      } // Fallback if we can't find a spot
    } while (
      existingLines.some((line) => isTooClose(newPos, line, minDistance))
    );

    return newPos;
  }

  // Initialize lines with non-overlapping positions
  let lines: LatexLine[] = (() => {
    const initialLines: LatexLine[] = [];
    for (let i = 0; i < 10; i++) {
      const { top, left } = getNewPosition(initialLines);
      initialLines.push({
        key: i + "-" + Math.random(),
        top,
        left,
        snippet: snippets[Math.floor(Math.random() * snippets.length)],
        progress: 0,
        speed: 20 + Math.random() * 50,
      });
    }
    return initialLines;
  })();

  let interval: ReturnType<typeof setInterval>;

  function randomSnippetNot(snippet: string) {
    let idx;
    do {
      idx = Math.floor(Math.random() * snippets.length);
    } while (snippets[idx] === snippet);
    return snippets[idx];
  }

  onMount(() => {
    interval = setInterval(() => {
      lines = lines.map((line) => {
        if (line.progress < line.snippet.length) {
          return { ...line, progress: line.progress + 1 };
        } else {
          // reset to a new snippet
          const otherLines = lines.filter((l) => l.key !== line.key);
          const { top, left } = getNewPosition(otherLines);
          return {
            ...line,
            snippet: randomSnippetNot(line.snippet),
            progress: 0,
            top,
            left,
            speed: 25 + Math.random() * 50,
          };
        }
      });
    }, 80);
    return () => clearInterval(interval);
  });
</script>

<div class="bg-latex">
  {#each lines as line (line.key)}
    <span
      class="latex-line"
      style="top: {line.top}vh; left: {line.left}vw; animation-duration: {line.speed}s;"
      aria-hidden="true">{line.snippet.slice(0, line.progress)}</span
    >
  {/each}
</div>

<style>
  .bg-latex {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    overflow: hidden;
    pointer-events: none;
    z-index: 0;
  }
  .latex-line {
    position: absolute;
    white-space: pre;
    font-family: "Berkeley Mono", "Fira Mono", "Menlo", "monospace";
    font-size: 1.2rem;
    color: rgba(111, 120, 170, 0.32);
    text-shadow: 0 1px 10px rgba(55, 60, 80, 0.21);
    user-select: none;
    letter-spacing: 1px;
    transition: color 1s;
  }
  .latex-line:nth-child(odd) {
    font-size: 1.8rem;
    color: rgba(131, 120, 200, 0.32);
  }
</style>
