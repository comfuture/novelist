const skills = [
  ["Create a novel project", "Start from a structured Markdown workspace."],
  ["Build the world", "Develop settings with reusable, continuity-safe sources."],
  ["Shape characters", "Turn rough briefs into complete character sheets."],
  ["Gather materials", "Capture motifs, research, dialogue, and scene seeds."],
  ["Design the plot", "Build conflicts, reversals, reveals, and payoffs."],
  ["Control the story", "Plan chapters around reader understanding and continuity."],
  ["Review analytically", "Critique outlines and manuscripts without editing source by default."],
  ["Create visuals", "Develop cover and illustration assets for the project."],
  ["Deliver the book", "Package approved Draft content as a validated EPUB."],
];

export default function Home() {
  return (
    <main>
      <nav className="nav" aria-label="Primary navigation">
        <a className="brand" href="#top" aria-label="Novelist home">
          <img src="/logo.png" alt="" width="48" height="48" />
          <span>Novelist</span>
        </a>
        <div className="navLinks">
          <a href="#workflows">Workflows</a>
          <a href="#install">Install</a>
          <a href="https://github.com/comfuture/novelist">GitHub</a>
        </div>
      </nav>

      <section className="hero" id="top">
        <div className="eyebrow">An agent-assisted plugin for long-form fiction</div>
        <h1>Keep the whole novel in view.</h1>
        <p className="lede">
          Novelist connects worldbuilding, characters, materials, plots,
          outlines, chapters, and reader knowledge in one continuity-safe
          Markdown writing system.
        </p>
        <div className="actions">
          <a className="button primary" href="#install">Install Novelist</a>
          <a className="button secondary" href="https://github.com/comfuture/novelist">
            Explore the source
          </a>
        </div>
        <div className="heroMark" aria-hidden="true">
          <img src="/logo.png" alt="" />
        </div>
      </section>

      <section className="manifesto">
        <p>Structure without rigidity.</p>
        <p>Continuity without context overload.</p>
        <p>Publishing without hidden steps.</p>
      </section>

      <section className="section" id="workflows">
        <div className="sectionHeading">
          <span>Nine focused workflows</span>
          <h2>Build the story before delivering the book.</h2>
        </div>
        <div className="skillGrid">
          {skills.map(([title, description], index) => (
            <article className="skillCard" key={title}>
              <span className="skillNumber">{String(index + 1).padStart(2, "0")}</span>
              <h3>{title}</h3>
              <p>{description}</p>
            </article>
          ))}
        </div>
      </section>

      <section className="section install" id="install">
        <div>
          <span className="kicker">Codex · Claude Code · Antigravity CLI</span>
          <h2>Use the plugin in your agent.</h2>
          <p>
            Install the shared nine-skill plugin, or create a standalone
            workspace with repository-local skills.
          </p>
        </div>
        <pre aria-label="Installation commands"><code>{`# Codex
codex plugin add novelist@openai-curated-remote

# Claude Code
claude plugin marketplace add comfuture/novelist
claude plugin install novelist@novelist

# Antigravity CLI
agy plugins install https://github.com/comfuture/novelist
# Invoke /create-character

# Standalone snapshot
sh scripts/create-scaffold.sh --destination ../my-novel --agent all`}</code></pre>
      </section>

      <section className="section responsibility">
        <div className="sectionHeading">
          <span>Built for author agency</span>
          <h2>Your story remains yours.</h2>
        </div>
        <p>
          Novelist is open-source software provided under the MIT License. It
          does not claim ownership of work created with it. You remain
          responsible for reviewing, editing, and publishing your output.
        </p>
        <p>
          Analytical review runs when you request it. Novelist adds the complete
          review, finding-disposition, revision, and regression-review loop
          automatically only when you delegate the full journey from initial
          planning through publication. Ordinary writing and publication
          requests keep their focused workflows.
        </p>
      </section>

      <footer>
        <div>
          <strong>Novelist</strong>
          <span>Created by Changkyun Kim</span>
        </div>
        <div className="footerLinks">
          <a href="/support">Support</a>
          <a href="/releases">Releases</a>
          <a href="/privacy">Privacy</a>
          <a href="/terms">Terms</a>
          <a href="mailto:comfuture@gmail.com">Contact</a>
        </div>
        <p>© 2026 Changkyun Kim. Released under the MIT License.</p>
      </footer>
    </main>
  );
}
